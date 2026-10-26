# 等価変換の前後比較実験

同じ処理をするソースコードの書き方を変え、SU 数・トークンエントロピー (と後から回答精度) が
どう変わるかを追跡するための実験コード。最初の変換は「条件を否定して if 側と else 側を入れ替える」。

この実験で分かるのは「動作と LOC を保つ変換で、エントロピーと SU がどこでどう変わったか」まで。
SU が回答精度に因果的な影響を持つかどうかは、このコードの出力だけでは結論できない。

## 既存の計測方法 (コード・設定で確認できたこと)

| 項目 | 内容 | 根拠 |
|---|---|---|
| エントロピー計測モデル | `codellama/CodeLlama-7b-hf` (トークナイザーも同じ) | `out/` の `meta_model_name`, `scripts/batch_runner.py` |
| 計測時の device / dtype | `mps` / `float16` | `scripts/batch_runner.py` の設定 (`out/` のメタデータには記録されていない) |
| トークン化 | `add_special_tokens=False` で全文をトークン化し、先頭に BOS を付けて1回推論 | `model/hf_causal_lm.py` |
| エントロピー | 各位置の予測分布の `-Σ p ln p` [nats] | 同上 |
| SU | 改行トークンで区切った「行」のうち、先頭以外のトークンでエントロピー ≥ 閾値のものを含む行の前に境界。SU 数 = 境界数 + 1 | `lm_cc_helper/calculate_code_with_boundaries.py` (lm-cc から移植) |
| 閾値 | p67 = 0.6813, p80 = 1.2515 (全トークンのエントロピー分布のパーセンタイル。固定値) | `pipeline.py`, `run_threshold_experiments.py` |
| LOC | トークンがある最大の行番号 (空行・コメント行を含む) | `macro/loc.py` |
| トークン数 | surprisal が null でないトークン数 | `pipeline.process_file` |
| 回答モデル | deepseek-v3 (OpenAI 互換 API。実際のモデルは環境変数 `OPENAI_MODEL_NAME` 次第) | lm-cc `scripts/tasks/ier/prompt.py`, `generate_apr.py` |
| HumanEval の課題・採点 | 実行結果の推論 (IER)。`main.py` と `input.txt` からプロンプトを作り temperature 0 で5回、`output.txt` と文字列比較 (空白・引用符を正規化)。pass@1 = 正解回数 / 5 | lm-cc `tasks/ier/` |
| xcodeeval の課題・採点 | APR (修正) / CT (Python→C)。temperature 0.316 で5サンプル、`hidden_unit_tests` を実行 (CT は gcc) | lm-cc `generate_*.py`, `evaluate_*.py` |
| 対応言語 | 計測 (Phase 1) は Python / Java / C。SU を数える処理 (Tree-sitter) は Python のみ。データは全て `.py` | `language/`, `lm_cc_helper/tree_sitter_config.py` |

### 確認できていないこと

- LOC を統制しても低下傾向が残ったデータセットはどれか、そのとき使った閾値 (p67 / p80)
- `out/` 作成時の dtype・device (メタデータに無い。batch_runner の現在の設定からの推測)
- deepseek-v3 の実際の版 (API 側の設定で決まる)

### 今回見つかったデータの食い違い (既存の結果にも関係する)

- **HumanEval の計測用ソースと、先行研究の pass@1 のプロンプトに入ったコードが一致しないものがある。**
  lm-cc の `dataset/humaneval/<ID>/main.py` (pass@1 に使う接尾辞なしのケース) と
  `<ID>__0`, `<ID>__1` の `main.py` は書き方が違い、`data/humaneval/` は lm-cc の
  `extract_datasets.py` がどちらかをコピーしたもの。162 問中 83 問は `__0`/`__1` 側と同じで、
  接尾辞なしの `main.py` とは空行や空白が異なる。うち 4 問 (HumanEval_1, 105, 124, 150) は AST も異なる。
  この実験では、計測したコードをそのままプロンプトに入れて元コードも評価し直すので影響しないが、
  既存の「SU 数 × pass@1」の相関はこの食い違いを含んでいる。
  `transforms.csv` の `task_code_matches_source` / `lm_cc_cases_with_same_code` で問題ごとに確認できる。
- HumanEval_10 と HumanEval_33 は、計測用ソースを `input.txt` で実行した結果が `output.txt` と一致しない
  (HumanEval_10 は再帰が止まらない、HumanEval_33 は list と tuple の違い)。
  回答精度の評価では、このような問題は「正解を流用できない」として採点対象から外す。

## if/else 入れ替え変換 (`if_else_swap`)

`if C: A else: B` → `if not (C): B else: A`。実装は `src/equivalence/transforms/if_else_swap.py`。

- **対応言語**: Python 3 (実行中の Python の `ast` で構文解析できるコード)
- **適用条件**: `else` 節がちょうど1つで `elif` が無い `if` 文。if 側・else 側とも本体が次の行以降の
  ブロック (`if c: x` / `else: y` の1行形式は対象外)。満たさない候補は理由付きで `not_applicable`。
- **条件の否定**: 比較演算子の置き換え (`<` → `>=`) はしない (NaN や独自の比較で意味が変わるため)。
  - 条件が `not X` なら `X` にする (`unwrap_not = true`)。`if` も `not` も `bool(X)` を1回評価するだけなので同じ
  - それ以外は `not` を付ける。識別子・呼び出し・括弧式などは `not X`、それ以外は `not (X)`
    (`negation_style = "always_paren"` で常に括弧)
  - `if(x):` のように空白が無い場合は `if not (x):` になるよう空白を足す
- **変更範囲**: 条件式の前後への `not (` `)` の挿入 (または `not` の削除) と、本体の行単位の入れ替えだけ。
  本体の各行の文字列 (インデント・コメントを含む) は変えない。本体の外の行
  (`else:` の行、本体の前後の空行・コメント行) は元の位置に残す
- **検査** (外れたら `failed`): 変換後が構文解析できる / AST が「元の AST で条件を否定し body と orelse を
  交換したもの」と一致する / 行数が変わらない
- **複数候補**: 1つのファイルに候補が複数あっても、それぞれ元コードに対して1か所だけ変換した別の
  バージョン (`<uid>__ifelse_L<行>`) を作る

現在のデータでの適用状況 (候補 = 全 if 文):

| dataset | ok | not_applicable | failed |
|---|---|---|---|
| humaneval | 28 (27 ファイル) | 148 | 0 |
| xcodeeval_apr | 369 (157 ファイル) | 1499 | 2 (Python 2 の構文) |
| xcodeeval_code_translation | 424 (217 ファイル) | 1001 | 0 |

## 処理の流れ

```
scan       候補の一覧だけを見る (dry-run。実験ディレクトリを作らない)      (CPU)
transform  変換候補の列挙と適用、構文・AST・行数の検査               (CPU)
behavior   既存テストで元コードと変換後コードを実行して比較           (CPU)
measure    Phase 1 (collect_metrics.collect) で元・変換後を計測      (要モデル: Mac)
compare    Phase 2 と同じ関数で LOC・トークン数・SU などを算出し比較  (CPU)
accuracy-* 回答精度の評価 (後から別に実行)
```

```bash
CFG=configs/equivalence/if_else_swap_humaneval_sample.toml
python scripts/equivalence_experiment.py all --config $CFG       # transform → behavior → measure → compare
python scripts/equivalence_experiment.py status --config $CFG    # 段階ごとの件数

# 段階ごとに実行する場合 (例: Windows で transform / behavior、Mac で measure、どちらかで compare)
python scripts/equivalence_experiment.py transform --config $CFG
python scripts/equivalence_experiment.py behavior  --config $CFG
python scripts/equivalence_experiment.py measure   --config $CFG
python scripts/equivalence_experiment.py compare   --config $CFG

# 対象を絞る
python scripts/equivalence_experiment.py all --config $CFG --ids HumanEval_123
python scripts/equivalence_experiment.py all --config $CFG --targets HumanEval_123:ifelse_L8
```

モデル無しで全段階を試すときはダミーモデルの設定を使う (エントロピーの値に意味は無い):
`python scripts/equivalence_experiment.py all --config configs/equivalence/if_else_swap_humaneval_sample_dummy.toml`

### 候補の一覧 (scan)

変換をどのデータセットに試すか決める前に、適用できる候補の数と、適用できない理由の内訳を見る。
候補ごとに `apply` まで行うので、変換後の検査で落ちるもの (`failed`) も分かる。動作確認・計測はしない。
実験ディレクトリは作らず、`--out` を付けたときだけ候補ごとの CSV を書く。

```bash
python scripts/equivalence_experiment.py scan --dataset all --transform if_else_swap
python scripts/equivalence_experiment.py scan --dataset humaneval xcodeeval_apr --out /tmp/candidates.csv
python scripts/equivalence_experiment.py scan --config $CFG          # 設定の dataset・ids・変換オプションで
```

表示はデータセット × 変換ごとの `files` (ファイル数) / `files_with_candidates` / `files_with_ok` /
`candidates` / `ok` / `not_applicable` / `failed` と、理由ごとの件数 (理由の行番号などの部分は落として集計)。

### データセット × 変換をまとめて回す (`--dataset` / `--transform` / `--name`)

1つの設定ファイル (または既定値) を、データセット・変換を差し替えて回せる。どちらも複数指定でき、
`all` は登録済みの全部。組み合わせごとに別の実験ディレクトリになる。

```bash
# テンプレートの設定 (CodeLlama / MPS) を全データセットに
python scripts/equivalence_experiment.py all --config configs/equivalence/template.toml --dataset all
# 設定ファイルなし (DEFAULT_CONFIG) でも動く
python scripts/equivalence_experiment.py transform --dataset xcodeeval_apr --transform if_else_swap
python scripts/equivalence_experiment.py status    --dataset xcodeeval_apr --transform if_else_swap
```

- 実験名 (`experiment.name`) の `{transform}` / `{dataset}` は変換名・データセット名に置き換わる。
  既定は `"{transform}_{dataset}"`。`--name` で上書きできる (例: `--name "ifelse_v2_{dataset}"`)
- `--dataset` / `--transform` で設定ファイルと違う値にしたのに名前にその置き換え (`{dataset}` / `{transform}`) が
  無いときは、既定の `"{transform}_{dataset}"` を使う (条件の違う結果が同じディレクトリに入らないように)。
  組み合わせで名前が重複するときはエラー
- データセットを差し替えたときは `ids` を `"all"`、`targets` を空に戻す (ID は元の設定のデータセットのもの)。
  `--ids` / `--targets` / `--limit` を付ければそちらを使う
- 変換を差し替えたときは `transform.options` を空 (その変換の既定値) に戻す
- 後の段階 (measure, compare, status など) も、同じ `--config` / `--dataset` / `--transform` / `--name` で実行する

### 計測結果の再利用 (キャッシュ)

measure 段階は、計測したトークン表を `<output_root>/_cache/measure/` にも保存し、同じ条件で同じコードを
計測するときはモデルを使わずにそこからコピーする。元コードは変換の種類が違っても同じなので、
2つ目以降の変換では元コードの計測が省ける (全部キャッシュにあればモデルも読み込まない)。

- キャッシュキー: コードのバイト列の SHA-256、`[measure]` の `model` / `model_kind` / `revision` / `device` /
  `dtype` / `context_strategy`、collector の版 (`COLLECTOR_VERSION`)、torch / transformers の版。
  どれかが違えば別キーになり、計測し直す (dtype や device が違う結果を混ぜない)
- コピー時に `meta_project` / `meta_file` だけはその実験の値に書き換える。それ以外 (エントロピー、
  `meta_created_at` など) は最初に計測したときの値のまま
- `status/measure.json` に `cache_hit` / `cache_key` を記録する。キャッシュの各ファイルの隣の `<key>.json` に
  キーの元になった値がある
- `measure.cache = false` で使わない。`measure.cache_dir` で場所を変えられる (相対パスは `output_root` から)。
  この2つは同じ実験ディレクトリの途中で変えてもよい
- 実験ディレクトリを別のマシンに渡すときはキャッシュは無くてもよい (各実験の `measure/` に実体がある)

段階をまたいで同じ実験ディレクトリを使うので、Windows と Mac で分担するときは
`results/equivalence/<name>/` をそのまま受け渡す (パスはすべて相対で扱い、改行は `\n` で保存している)。

## 動作確認の判定

使うテストはすべて lm-cc の既存データ:

- HumanEval: `<ID>`, `<ID>__0`, `<ID>__1` の `input.txt` の式の返り値 (str と repr)、
  `asserts.txt` の `check(candidate)` の各 assert の真偽と左辺の値
- xcodeeval: `hidden_unit_tests` の各入力を stdin に与えたときの stdout・終了コード・例外

| status | 意味 |
|---|---|
| `match` | 全テストで変換前後の観測結果が一致した (= テストで一致を確認できた) |
| `mismatch` | 1つ以上のテストで結果が違った |
| `unverified` | テストが無い・タイムアウトした等で確認できなかった (理由を記録) |
| `not_run` | 未実行 |

`match` は用意されたテスト入力で同じ結果になったことだけを意味し、あらゆる入力での等価性の証明ではない。
既定では `match` の変換後コードだけを計測する (`measure.allowed_behavior`)。
LOC は変換時に行数で、計測後に既存と同じ定義 (`macro/loc.py`) で確認し、`loc_equal` に記録する。

## 出力 (`results/equivalence/<experiment.name>/`)

| パス | 内容 |
|---|---|
| `config.json`, `manifest.json`, `runs.jsonl` | 使用設定、作成時のコードの版 (git commit / dirty)・Python・パッケージの版、実行ごとの記録 |
| `status/<stage>.json` | 対象ごとの状態 (ok / failed / skipped と理由) |
| `codes/<uid>/original.py`, `<variant>.py` | 元コードと変換後コード |
| `transforms.csv`, `transforms/<uid>.json` | 全候補の状態・理由・変換箇所・変換内容 (条件の前後、本体の移動先の行)・行対応 |
| `behavior.csv`, `behavior/<uid>/*.json` | 判定と、ケースごとの観測結果 |
| `measure/<uid>/*.parquet` | Phase 1 と同じ形式のトークン表 (キャッシュから再利用した場合も同じ形式) |
| `compare/summary.csv` | 変換1件 = 1行。LOC・トークン数・平均エントロピー・PPL・SU 数・LM-CC の 変換前 / 変換後 / 差分、`su_change_<閾値>` (decreased / increased / unchanged) |
| `compare/regions.csv` | 変換箇所との位置関係 (before / if_header / then_body / between / else_body / after) ごとの集計。`after` が変換箇所より後に続く部分 |
| `compare/<uid>/<variant>/tokens_before.csv`, `tokens_after.csv` | 各トークンの文字列・行・列・エントロピー・閾値ごとの境界トークンか・SU 番号・region・相手側の対応行 |
| `compare/<uid>/<variant>/lines.csv` | 元コードの行順に、対応する変換後の行と、行ごとのエントロピー (平均・最大・合計)・SU 境界の有無と変化 |
| `compare/<uid>/<variant>/token_alignment.csv` | 対応する行どうしでトークン文字列を突き合わせた結果 (equal / only_before / only_after) |
| `compare/<uid>/<variant>/summary.json` | SU ごとの開始・終了行、トークン範囲、境界を作ったトークン |
| `compare/<uid>/<variant>/report.html`, `report.md` | 変換前後のコード・エントロピー・SU 境界を並べたレポート |

SU 番号の注意: 既存の `get_code_with_boundaries` は1行目 (先頭トークン以外) に閾値以上のトークンがあると
1行目の前にも境界を入れて SU 数に数える。このとき SU0 はトークンを含まない空の SU になり
(`summary.json` の `start_line` が null、レポートでは「空: 先頭行の前の境界」)、`tokens_*.csv` / `lines.csv` の
`su_<閾値>` 列は 1 から始まる。SU 数を既存の分析と揃えるため、この挙動はそのまま残している。

変換前後でトークン列が変わるので、トークン番号どうしは対応づけない。変換が記録した行の対応
(移動した本体の行は移動先の行) の中で、トークン文字列が一致した部分だけを対にする。

## 回答精度の評価 (後から実行)

エントロピー・SU の計測とは独立に、後から実行できる。元コードと変換後コードを同じ回答モデル・
プロンプト・試行回数・採点方法で評価し、同じ uid で比較する (`accuracy/comparison.csv`)。

```bash
python scripts/equivalence_experiment.py accuracy-prepare --config $CFG   # プロンプト / lm-cc 用入力を作る
```

`accuracy/items.csv` に評価対象と、対象外にした理由 (`skip_reason`) が出る。
正解を流用できると確認できないものは採点しない:

- HumanEval: 元コード (計測用ソース) の返り値が `output.txt` と一致し、かつ変換後コードの返り値が
  元コードと一致したケースだけ。プロンプトは lm-cc の `create_prompt` を読み込んで作り、
  計測したコードがプロンプトにちょうど1回入っていることを確認する
- xcodeeval: 動作確認が `match` のものだけ。正解は問題ごとの hidden tests なので変換後もそのまま使える

### HumanEval (このリポジトリで実行)

```bash
export OPENAI_API_KEY=... OPENAI_BASE_URL=... OPENAI_MODEL_NAME=deepseek-v3   # lm-cc と同じ環境変数
python scripts/equivalence_experiment.py accuracy-run   --config $CFG [--max-calls 10]
python scripts/equivalence_experiment.py accuracy-score --config $CFG
```

1試行 = 1ファイル (`accuracy/responses/`) で保存し、成功済みの試行は再実行しない。
`accuracy/answers.csv` (個々の回答・予測値・正誤)、`accuracy.csv` (試行回数・正解数・pass@1)、
`comparison.csv` (元コードとの差) を出力する。`openai` パッケージが必要。

### xcodeeval (lm-cc のスクリプトで実行)

`accuracy-prepare` がコード欄を変換後コードに、uid を `<uid>__<variant>` に置き換えた
`accuracy/lmcc_input.jsonl` を作る。これを lm-cc の生成・評価スクリプトにそのまま渡す:

```bash
cd ../lm-cc/scripts
python tasks/generate_apr.py --dataset-path <実験dir>/accuracy/lmcc_input.jsonl --output-dir <実験dir>/accuracy/lmcc --nsample 5
python tasks/evaluate_apr.py --task apr --output-dir <実験dir>/accuracy/lmcc
cd -
python scripts/equivalence_experiment.py accuracy-score --config $CFG \
    --details <実験dir>/accuracy/lmcc/xcodeeval/apr/python_test_filtered_results_details.jsonl
```

CT は `generate_ct.py` / `evaluate_ct.py` (`--task code_translation`、details は
`python2c_test_filtered_results_details.jsonl`)。

## 再計測・追加実験

- 設定は TOML (`configs/equivalence/`)。対象 ID・変換箇所・変換の設定・モデル・閾値・試行回数・出力先を書く
- 同じコマンドを再実行すると、成功済みの対象は飛ばして未実行・失敗分だけを処理する。
  `--only-failed` で失敗分だけに絞れる
- 計測条件 (変換・モデル・閾値・動作確認・回答評価の設定) を変えた設定で同じ `experiment.name` を
  使うとエラーにする。条件を変えるときは名前を変えて別ディレクトリにする (既存結果を上書きしない)。
  対象 ID の追加は同じディレクトリでよい
- 閾値は設定で固定した値を使い、変換結果を見て変えない。SU 数が減った場合も増えた場合も
  変わらなかった場合もすべて保存する
- 元コード・変換後コード・問題 (lm-cc のケース)・結果は `item_id` (`<uid>` / `<uid>__<variant>`) で
  対応づけているので、「正しい途中状態を提示する実験」などで再利用できる

### 新しい等価変換を追加するには

1. `src/equivalence/transforms/` に `Transformation` を継承したクラスを作る
   (`find_candidates` で候補を理由付きで列挙、`apply` で1候補だけ適用して `line_map` と検査結果を返す)
2. `transforms/__init__.py` で `register_transformation` する
3. `scan --transform <名前> --dataset all` で候補数と適用できない理由を確認する
4. 設定の `transform.name` / `transform.options` (または `--transform`) で指定する

`line_map` の `region` は比較・レポートでそのまま使われる (if/else 以外の名前でもよい)。

## 制約・未対応

- 変換は Python のみ。Java / C のデータは現在無い
- Python 2 の構文のコード (xcodeeval に少数) は変換できず `failed` になる
- 構文解析は実行中の Python の `ast` に依存する (版は `manifest.json` に記録)
- 動作確認は既存テストの範囲だけ。xcodeeval の一部の問題はテストが多く、1ファイル数十秒かかる
- 回答精度の API 呼び出しは今回実行していない (偽の回答関数でのテストのみ)
