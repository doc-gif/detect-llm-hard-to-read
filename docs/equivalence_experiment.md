# 等価変換の前後比較実験

この実験では、処理内容を変えずにソースコードの書き方だけを変え、SU 数とトークンのエントロピーが
どう変わるかを調べる。回答精度も、後から同じ対象で評価できるようにしてある。
最初に実装した変換は、「条件を否定して、if ブロックと else ブロックを入れ替える」変換である。

この実験の出力から分かるのは、動作と LOC を保つ変換によって、エントロピーと SU がどこでどう変わったかである。
SU が回答精度に因果的な影響を与えるかどうかは、この出力だけでは結論できない。

## 既存の計測方法 (コードと設定から確認できたこと)

| 項目 | 内容 | 根拠 |
|---|---|---|
| エントロピーを計測するモデル | `codellama/CodeLlama-7b-hf` (トークナイザーも同じモデルのもの) | `out/` の `meta_model_name`, `scripts/batch_runner.py` |
| 計測時の device / dtype | `mps` / `float16` | `scripts/batch_runner.py` の設定 (`out/` のメタデータには記録されていない) |
| トークン化 | `add_special_tokens=False` で全文をトークン化し、先頭に BOS を付けて1回だけ推論する | `model/hf_causal_lm.py` |
| エントロピー | 各位置の予測分布について `-Σ p ln p` [nats] を計算する | 同上 |
| SU | コードを改行トークンで行に分け、先頭以外のトークンのエントロピーが閾値以上になる行の前に境界を置く。SU 数は境界の数に 1 を足した値である | `lm_cc_helper/calculate_code_with_boundaries.py` (lm-cc から移植) |
| 閾値 | p67 = 0.6813, p80 = 1.2515 (全トークンのエントロピー分布のパーセンタイルから決めた固定値) | `pipeline.py`, `run_threshold_experiments.py` |
| LOC | トークンが存在する最大の行番号 (空行とコメント行も数える) | `macro/loc.py` |
| トークン数 | surprisal が null でないトークンの数 | `pipeline.process_file` |
| 回答モデル | deepseek-v3 (OpenAI 互換 API を使う。実際に使われるモデルは環境変数 `OPENAI_MODEL_NAME` で決まる) | lm-cc `scripts/tasks/ier/prompt.py`, `generate_apr.py` |
| HumanEval の課題と採点 | 実行結果を推論させる課題 (IER)。`main.py` と `input.txt` からプロンプトを作り、temperature 0 で 5 回回答させる。回答は `output.txt` と文字列で比較する (空白と引用符は正規化する)。pass@1 は正解した回数を 5 で割った値である | lm-cc `tasks/ier/` |
| xcodeeval の課題と採点 | APR (バグ修正) と CT (Python から C への翻訳)。temperature 0.316 で 5 サンプルを生成し、`hidden_unit_tests` で実行して確かめる (CT は gcc でコンパイルする) | lm-cc `generate_*.py`, `evaluate_*.py` |
| 対応言語 | 計測 (Phase 1) は Python・Java・C に対応している。SU を数える処理 (Tree-sitter) は Python にしか対応していない。現在のデータはすべて `.py` である | `language/`, `lm_cc_helper/tree_sitter_config.py` |

### 確認できていないこと

- LOC を統制しても低下傾向が残ったのがどのデータセットか、そのときにどちらの閾値 (p67 / p80) を使ったかは確認できていない。
- `out/` を作ったときの dtype と device は確認できていない。メタデータに記録されていないため、上の表の値は batch_runner の現在の設定から推測したものである。
- deepseek-v3 の実際のバージョンは確認できていない。バージョンは API 側の設定で決まる。

### 今回見つかったデータの食い違い (既存の結果にも関係する)

- **HumanEval では、計測に使ったソースと、先行研究の pass@1 でプロンプトに入れたコードが一致しない問題がある。**
  lm-cc には、pass@1 に使う接尾辞なしのケース (`dataset/humaneval/<ID>/main.py`) と、
  `<ID>__0`・`<ID>__1` のケースがあり、両者の `main.py` は書き方が違う。`data/humaneval/` のファイルは、
  lm-cc の `extract_datasets.py` がこのどちらかをコピーしたものである。162 問のうち 83 問は `__0`/`__1` 側と同じで、
  接尾辞なしの `main.py` とは空行や空白が異なる。そのうち 4 問 (HumanEval_1, 105, 124, 150) は AST も異なる。
  この実験では、計測したコードをそのままプロンプトに入れて元コードも評価し直すので、この食い違いの影響は受けない。
  一方、既存の「SU 数と pass@1 の相関」はこの食い違いを含んだまま計算されている。
  問題ごとの状況は、`transforms.csv` の `task_code_matches_source` 列と `lm_cc_cases_with_same_code` 列で確認できる。
- HumanEval_10 と HumanEval_33 では、計測に使ったソースを `input.txt` で実行しても、結果が `output.txt` と一致しない。
  HumanEval_10 は再帰が止まらず、HumanEval_33 は list と tuple の違いで結果がずれる。
  回答精度の評価では、このような問題は正解をそのまま使えないので、採点の対象から外す。

## if/else 入れ替え変換 (`if_else_swap`)

この変換は `if C: A else: B` を `if not (C): B else: A` に書き換える。実装は `src/equivalence/transforms/if_else_swap.py` にある。

- **対応言語**: Python 3 に対応している。実行中の Python の `ast` で構文解析できるコードだけを変換する。
- **適用条件**: `else` 節がちょうど 1 つあり、`elif` が無い `if` 文を変換する。さらに、if ブロックと else ブロックの
  中身が、どちらも次の行から始まっている必要がある (`if c: x` や `else: y` のように 1 行に書いたものは変換しない)。
  条件を満たさない候補は、理由とともに `not_applicable` として記録する。
- **条件の否定**: 比較演算子の置き換え (`<` を `>=` にするなど) はしない。NaN や独自に定義された比較では意味が変わるためである。
  - 条件が `not X` の形なら、`not` を取り除いて `X` にする (`unwrap_not = true`)。`if` も `not` も `bool(X)` を 1 回評価するだけなので、意味は変わらない。
  - それ以外の条件には `not` を付ける。識別子・関数呼び出し・括弧で囲んだ式などの単純な式には `not X` の形で付け、それ以外の式には `not (X)` の形で付ける。
    `negation_style = "always_paren"` を指定すると、常に括弧を付ける。
  - `if(x):` のように `if` の後に空白が無い場合は、`if not (x):` になるように空白を補う。
- **変更する範囲**: 変換で変わるのは、条件式の前後に `not (` と `)` を挿入する (または `not` を削除する) 部分と、
  ブロックの中身を行単位で入れ替える部分だけである。ブロック内の各行の文字列 (インデントとコメントを含む) は変えない。
  ブロックの外にある行 (`else:` の行や、ブロックの前後にある空行・コメント行) は元の位置に残す。
- **変換後のチェック**: 変換後のコードについて、構文解析できること、AST が「元の AST の条件を否定し、body と orelse を
  入れ替えたもの」と一致すること、行数が変わらないことを確かめる。どれか 1 つでも満たさない場合は `failed` とする。
- **候補が複数ある場合**: 1 つのファイルに候補が複数あっても、それぞれの候補について、元コードの 1 か所だけを変換した
  別のバージョン (`<uid>__ifelse_L<行番号>`) を作る。

現在のデータに適用した結果は次のとおりである (候補はすべての if 文である)。

| dataset | ok | not_applicable | failed |
|---|---|---|---|
| humaneval | 28 (27 ファイル) | 148 | 0 |
| xcodeeval_apr | 369 (157 ファイル) | 1499 | 2 (Python 2 の構文) |
| xcodeeval_code_translation | 424 (217 ファイル) | 1001 | 0 |

## 処理の流れ

| 段階 | 内容 | 実行環境 |
|---|---|---|
| `scan` | 変換の候補を一覧表示する。ファイルは書き出さない | CPU |
| `transform` | 変換の候補を探して変換し、構文・AST・行数をチェックする | CPU |
| `behavior` | 既存のテストで元コードと変換後のコードを実行し、結果を比べる | CPU |
| `measure` | Phase 1 (`collect_metrics.collect`) で元コードと変換後のコードを計測する | モデルが必要 (Mac) |
| `compare` | Phase 2 と同じ関数で LOC・トークン数・SU などを計算し、変換の前後で比べる | CPU |
| `accuracy-*` | 回答精度を評価する (後から別に実行する) | API |

```bash
CFG=configs/equivalence/if_else_swap_humaneval_sample.toml
python scripts/equivalence_experiment.py all --config $CFG       # transform → behavior → measure → compare を順に実行する
python scripts/equivalence_experiment.py status --config $CFG    # 段階ごとの件数を表示する

# 段階ごとに実行する場合 (例: Windows で transform と behavior、Mac で measure、どちらかで compare を実行する)
python scripts/equivalence_experiment.py transform --config $CFG
python scripts/equivalence_experiment.py behavior  --config $CFG
python scripts/equivalence_experiment.py measure   --config $CFG
python scripts/equivalence_experiment.py compare   --config $CFG

# 対象を絞る場合
python scripts/equivalence_experiment.py all --config $CFG --ids HumanEval_123
python scripts/equivalence_experiment.py all --config $CFG --targets HumanEval_123:ifelse_L8
```

モデルを使わずにすべての段階を試したいときは、ダミーモデルの設定を使う (この場合のエントロピーの値には意味が無い)。

```bash
python scripts/equivalence_experiment.py all --config configs/equivalence/if_else_swap_humaneval_sample_dummy.toml
```

### 変換候補の一覧 (`scan`)

`scan` は、変換をどのデータセットに適用するかを決める前に、適用できる候補の数と、適用できない理由の内訳を表示する。
候補ごとに変換まで行うので、変換後のチェックで失敗する候補 (`failed`) も分かる。動作確認と計測は行わない。
実験ディレクトリは作らない。`--out` を指定したときだけ、候補ごとの一覧を CSV に書き出す。

```bash
python scripts/equivalence_experiment.py scan --dataset all --transform if_else_swap
python scripts/equivalence_experiment.py scan --dataset humaneval xcodeeval_apr --out /tmp/candidates.csv
python scripts/equivalence_experiment.py scan --config $CFG          # 設定ファイルの dataset・ids・変換のオプションを使う
```

出力には 2 つの表がある。1 つ目の表は、データセットと変換の組ごとに、次の件数を示す。

| 列 | 意味 |
|---|---|
| `files` | 対象のファイル数 |
| `files_with_candidates` | 候補が 1 つ以上あるファイルの数 |
| `files_with_ok` | 変換できた候補が 1 つ以上あるファイルの数 |
| `candidates` | 候補の総数 |
| `ok` / `not_applicable` / `failed` | 変換できた候補、適用条件を満たさない候補、変換後のチェックで失敗した候補の数 |

2 つ目の表は、適用できなかった理由ごとの件数を示す。理由に含まれる行番号などの個別の情報は、集計の前に取り除いている。

### データセットと変換の組み合わせをまとめて実行する (`--dataset` / `--transform` / `--name`)

1 つの設定ファイル (またはデフォルトの設定) を使い、データセットや変換だけを差し替えて実行できる。
`--dataset` と `--transform` には複数の値を指定でき、`all` を指定すると登録済みのものをすべて対象にする。
実験ディレクトリは、データセットと変換の組み合わせごとに別々に作られる。

```bash
# テンプレートの設定 (CodeLlama / MPS) で、すべてのデータセットを処理する
python scripts/equivalence_experiment.py all --config configs/equivalence/template.toml --dataset all
# 設定ファイルを指定しない場合は、デフォルトの設定 (DEFAULT_CONFIG) を使う
python scripts/equivalence_experiment.py transform --dataset xcodeeval_apr --transform if_else_swap
python scripts/equivalence_experiment.py status    --dataset xcodeeval_apr --transform if_else_swap
```

- 実験名 (`experiment.name`) に `{transform}` や `{dataset}` を書くと、それぞれ変換名とデータセット名に置き換わる。
  デフォルトの実験名は `"{transform}_{dataset}"` である。実験名は `--name` で変更できる (例: `--name "ifelse_v2_{dataset}"`)。
- `--dataset` や `--transform` で設定ファイルと異なる値を指定したにもかかわらず、実験名に `{dataset}` や `{transform}` が
  含まれていない場合は、デフォルトの `"{transform}_{dataset}"` を実験名に使う。条件の異なる結果が同じディレクトリに
  混ざらないようにするためである。組み合わせによって実験名が重複する場合は、エラーにする。
- データセットを差し替えた場合は、`ids` を `"all"` に、`targets` を空に戻す。設定ファイルに書かれた ID は、
  元のデータセットの ID だからである。`--ids`・`--targets`・`--limit` を指定した場合は、その値を使う。
- 変換を差し替えた場合は、`transform.options` を空に戻す (つまり、その変換のデフォルトのオプションを使う)。
- 後の段階 (measure, compare, status など) を実行するときも、同じ `--config`・`--dataset`・`--transform`・`--name` を指定する。

### 計測結果の再利用 (キャッシュ)

measure 段階では、計測したトークンの表を `<output_root>/_cache/measure/` にも保存する。同じ条件で同じコードを
計測するときは、モデルを使わずに、保存しておいた結果をコピーする。元コードは変換の種類が違っても同じなので、
2 つ目以降の変換では元コードを計測しなくて済む。すべての結果がキャッシュにある場合は、モデルの読み込みも行わない。

- キャッシュのキーは、次の値から作る。どれか 1 つでも違えば別のキーになり、改めて計測する。
  これにより、dtype や device が異なる結果が混ざらないようにしている。
  - コードのバイト列の SHA-256
  - `[measure]` の `model`・`model_kind`・`revision`・`device`・`dtype`・`context_strategy`
  - collector のバージョン (`COLLECTOR_VERSION`)
  - torch と transformers のバージョン
- キャッシュからコピーするときは、`meta_project` 列と `meta_file` 列だけを、その実験の値に書き換える。
  それ以外の列 (エントロピーや `meta_created_at` など) は、最初に計測したときの値のままである。
- キャッシュを使ったかどうかは、`status/measure.json` の `cache_hit` と `cache_key` に記録する。
  キャッシュの各ファイルの隣にある `<key>.json` には、キーを作るのに使った値が記録されている。
- `measure.cache = false` を指定すると、キャッシュを使わない。`measure.cache_dir` で保存場所を変更できる
  (相対パスは `output_root` を基準にする)。この 2 つの設定は、同じ実験ディレクトリで途中から変更してもよい。
- 実験ディレクトリを別のマシンに渡すときは、キャッシュを一緒に渡す必要は無い。計測結果の実体は各実験の `measure/` にある。

### Windows と Mac で作業を分担する場合

すべての段階が同じ実験ディレクトリを使うので、`results/equivalence/<name>/` をそのままマシン間で受け渡せばよい。
パスはすべて相対パスで扱い、改行は `\n` で保存している。

## 動作確認の判定

動作確認には、lm-cc にある既存のテストだけを使う。

- HumanEval では、`<ID>`・`<ID>__0`・`<ID>__1` の `input.txt` に書かれた式の返り値 (str と repr) と、
  `asserts.txt` の `check(candidate)` に含まれる各 assert の真偽と左辺の値を比べる。
- xcodeeval では、`hidden_unit_tests` の各入力を標準入力に与え、標準出力・終了コード・例外を比べる。

| status | 意味 |
|---|---|
| `match` | すべてのテストで、変換の前後の結果が一致した (テストの範囲で一致を確認できた) |
| `mismatch` | 1 つ以上のテストで、変換の前後の結果が異なった |
| `unverified` | テストが無い、タイムアウトしたなどの理由で確認できなかった (理由を記録する) |
| `not_run` | まだ実行していない |

`match` は、用意されたテストの入力で同じ結果になったことを示すだけであり、あらゆる入力で等価であることを証明するものではない。
デフォルトでは、判定が `match` になった変換後のコードだけを計測する (`measure.allowed_behavior`)。
LOC は 2 回確認する。変換時には行数が変わらないことを確かめ、計測後には既存と同じ定義 (`macro/loc.py`) で
変換の前後の LOC を比べて、結果を `loc_equal` 列に記録する。

## 出力 (`results/equivalence/<experiment.name>/`)

| パス | 内容 |
|---|---|
| `config.json`, `manifest.json`, `runs.jsonl` | 使用した設定、作成時のコードのバージョン (git の commit と未コミットの変更の有無)・Python とパッケージのバージョン、実行ごとの記録 |
| `status/<stage>.json` | 対象ごとの状態 (ok / failed / skipped とその理由) |
| `codes/<uid>/original.py`, `<variant>.py` | 元コードと変換後のコード |
| `transforms.csv`, `transforms/<uid>.json` | すべての候補の状態・理由・変換箇所・変換内容 (変換前後の条件式、ブロックの移動先の行)・行の対応 |
| `behavior.csv`, `behavior/<uid>/*.json` | 動作確認の判定と、テストケースごとの実行結果 |
| `measure/<uid>/*.parquet` | Phase 1 と同じ形式のトークンの表 (キャッシュから再利用した場合も同じ形式) |
| `compare/summary.csv` | 変換 1 件につき 1 行。LOC・トークン数・平均エントロピー・PPL・SU 数・LM-CC について、変換前・変換後・差分を記録する。`su_change_<閾値>` 列には SU 数が減ったか (decreased)、増えたか (increased)、変わらなかったか (unchanged) を記録する |
| `compare/regions.csv` | 変換箇所との位置関係 (before / if_header / then_body / between / else_body / after) ごとの集計。`after` は変換箇所より後の部分を指す |
| `compare/<uid>/<variant>/tokens_before.csv`, `tokens_after.csv` | 各トークンの文字列・行・列・エントロピー、閾値ごとに境界を作るトークンかどうか、SU 番号、region、もう一方のコードで対応する行 |
| `compare/<uid>/<variant>/lines.csv` | 元コードの行の順に、対応する変換後の行、行ごとのエントロピー (平均・最大・合計)、SU 境界の有無とその変化 |
| `compare/<uid>/<variant>/token_alignment.csv` | 対応する行どうしでトークンの文字列を照合した結果 (equal / only_before / only_after) |
| `compare/<uid>/<variant>/summary.json` | SU ごとの開始行・終了行、トークンの範囲、境界を作ったトークン |
| `compare/<uid>/<variant>/report.html`, `report.md` | 変換前後のコード・エントロピー・SU 境界を並べて表示するレポート |

SU 番号についての注意: 既存の `get_code_with_boundaries` は、1 行目 (先頭のトークンを除く) に閾値以上のトークンがあると、
1 行目の前にも境界を置き、それも SU 数に数える。この場合、SU0 はトークンを 1 つも含まない空の SU になる。
`summary.json` ではこの SU の `start_line` が null になり、レポートでは「空: 先頭行の前の境界」と表示される。
また、`tokens_*.csv` と `lines.csv` の `su_<閾値>` 列は 1 から始まる。SU 数を既存の分析と揃えるため、この挙動は変えていない。

変換の前後でトークン列が変わるので、トークンの番号どうしでは対応づけない。変換時に記録した行の対応
(移動したブロックの行は移動先の行に対応させる) の範囲で、トークンの文字列が一致する部分だけを対応づける。

## 回答精度の評価 (後から実行する)

回答精度の評価は、エントロピーと SU の計測とは独立していて、後から実行できる。元コードと変換後のコードを、同じ回答モデル・
同じプロンプト・同じ試行回数・同じ採点方法で評価し、同じ uid どうしで比べる (`accuracy/comparison.csv`)。

```bash
python scripts/equivalence_experiment.py accuracy-prepare --config $CFG   # プロンプトと lm-cc 用の入力を作る
```

`accuracy/items.csv` には、評価の対象と、対象から外した理由 (`skip_reason`) が出力される。
正解をそのまま使えることを確認できなかったものは採点しない。

- HumanEval では、元コード (計測に使ったソース) の返り値が `output.txt` と一致し、さらに変換後のコードの返り値が
  元コードと一致したケースだけを評価する。プロンプトは lm-cc の `create_prompt` を読み込んで作り、
  計測したコードがプロンプトにちょうど 1 回含まれていることを確かめる。
- xcodeeval では、動作確認の判定が `match` のものだけを評価する。正解は問題ごとの hidden tests で判定するので、
  変換後のコードにもそのまま使える。

### HumanEval (このリポジトリで実行する)

```bash
export OPENAI_API_KEY=... OPENAI_BASE_URL=... OPENAI_MODEL_NAME=deepseek-v3   # lm-cc と同じ環境変数を使う
python scripts/equivalence_experiment.py accuracy-run   --config $CFG [--max-calls 10]
python scripts/equivalence_experiment.py accuracy-score --config $CFG
```

回答は 1 回の試行ごとに 1 ファイルとして `accuracy/responses/` に保存し、成功した試行は再実行しない。
採点の結果として、`accuracy/answers.csv` (個々の回答・予測値・正誤)、`accuracy.csv` (試行回数・正解数・pass@1)、
`comparison.csv` (元コードとの差) を出力する。実行には `openai` パッケージが必要である。

### xcodeeval (lm-cc のスクリプトで実行する)

`accuracy-prepare` は、コードの欄を変換後のコードに、uid を `<uid>__<variant>` に置き換えた
`accuracy/lmcc_input.jsonl` を作る。このファイルを lm-cc の生成スクリプトと評価スクリプトにそのまま渡す。

```bash
cd ../lm-cc/scripts
python tasks/generate_apr.py --dataset-path <実験dir>/accuracy/lmcc_input.jsonl --output-dir <実験dir>/accuracy/lmcc --nsample 5
python tasks/evaluate_apr.py --task apr --output-dir <実験dir>/accuracy/lmcc
cd -
python scripts/equivalence_experiment.py accuracy-score --config $CFG \
    --details <実験dir>/accuracy/lmcc/xcodeeval/apr/python_test_filtered_results_details.jsonl
```

CT の場合は `generate_ct.py` と `evaluate_ct.py` を使い (`--task code_translation`)、details には
`python2c_test_filtered_results_details.jsonl` を指定する。

## 再計測と追加の実験

- 設定は TOML ファイル (`configs/equivalence/`) に書く。対象の ID、変換箇所、変換の設定、モデル、閾値、試行回数、出力先を指定できる。
  新しく設定を作るときは `configs/equivalence/template.toml` をもとにするとよい。
- 同じコマンドを再実行すると、成功した対象は飛ばし、未実行の対象と失敗した対象だけを処理する。
  `--only-failed` を指定すると、失敗した対象だけを処理する。
- 計測条件 (変換・モデル・閾値・動作確認・回答評価の設定) を変えた設定で同じ `experiment.name` を使うと、エラーになる。
  既存の結果を上書きしないためである。条件を変えるときは、実験名を変えて別のディレクトリに出力する。
  対象の ID を追加するだけなら、同じディレクトリを使ってよい。
- 閾値には設定ファイルで固定した値を使い、変換の結果を見てから変えることはしない。SU 数が減った場合も、増えた場合も、
  変わらなかった場合も、すべての結果を保存する。
- 元コード・変換後のコード・問題 (lm-cc のケース)・結果は、`item_id` (`<uid>` または `<uid>__<variant>`) で
  対応づけている。そのため、「正しい途中状態を提示する実験」などの別の実験でも、これらの結果を再利用できる。

### 新しい等価変換を追加する手順

1. `src/equivalence/transforms/` に、`Transformation` を継承したクラスを作る。
   `find_candidates` では候補を理由とともに列挙し、`apply` では 1 つの候補だけを変換して、`line_map` とチェックの結果を返す。
2. `transforms/__init__.py` で `register_transformation` を呼び、変換を登録する。
3. `scan --transform <変換名> --dataset all` を実行し、候補の数と適用できない理由を確認する。
4. 設定ファイルの `transform.name` と `transform.options` (または `--transform`) で、追加した変換を指定する。

`line_map` の `region` は、比較とレポートでそのまま使われる。if/else 以外の名前を使ってもよい。

## 制約と未対応の事項

- 変換は Python にしか対応していない。Java と C のデータは現在存在しない。
- Python 2 の構文で書かれたコード (xcodeeval に少数含まれる) は変換できず、`failed` になる。
- 構文解析の結果は、実行中の Python の `ast` に依存する (Python のバージョンは `manifest.json` に記録している)。
- 動作確認は、既存のテストの範囲でしか行えない。xcodeeval の一部の問題はテストが多く、1 ファイルの確認に数十秒かかる。
- 回答精度を評価するための API 呼び出しは、まだ実行していない (偽の回答関数を使ったテストだけを行っている)。
