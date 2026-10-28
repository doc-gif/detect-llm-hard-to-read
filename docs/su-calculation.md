# SU・LM-CC・LOCの調査結果

保存したSU値は、木のノード数ではなく境界数に1を足した値である。`p67` は0.6813 nats、現存する `p80` は1.3238 natsで再現する。`p80` の名前から現在の80パーセンタイル値を推測してはいけない。

## 調査対象と状態

- detectのHEADは `2476ee6bfad24e217c0baf465b7709d21608b8c7` だった。
- remoteは `git@github.com:doc-gif/detect-llm-hard-to-read.git` だった。
- 作業前の未追跡ファイルは `.DS_Store`、`results/.DS_Store`、`scripts/inference.log` の3件だった。
- repo内と親ディレクトリにAGENTS.mdはなかった。元データと過去の出力を変更していない。

## 入力から指標まで

`lm-cc/extract_datasets.py` がdatasetから物理コードを抽出する。HumanEvalでは `extract_humaneval()` がIDの `__` 以降を落とす。同じ基底IDのうち、`glob()`で先に見つかった `main.py` をコピーする。並び順は固定していない。

`detect/scripts/batch_runner.py` は `data/` 配下のコードを列挙する。`collect_metrics.py` へファイルごとに渡す。保存済みのParquetがあれば再計測を省く。現行設定は `codellama/CodeLlama-7b-hf`、MPS、float16である。これはコード上の設定であり、全履歴の条件を保証する記録ではない。

`src/collect_metrics.py:collect()` はソースをそのまま読む。コメントやdocstringの除去は呼ばない。`HFCausalLMAdapter.tokenize()` は `add_special_tokens=False` でトークンと位置を作る。現行 `infer()` はモデル入力だけにBOSを付け、各トークンの直前分布からsurprisalとentropyを求める。surprisalは `-ln p(token)`、entropyは `-Σp ln p` で、単位はnatsである。BOSがないモデルでは先頭の値を欠損にする。

`src/analysis/pipeline.py:process_file()` はsurprisalが欠損した行を除く。その後にLM-CC・SU・LOCを計算する。`lm_cc.calculate()` が失敗して `None` を返すと、呼び出し側のunpackも失敗する。`run_pipeline()` は失敗したファイルをCSVに含めず、エラー件数を記録する。今回は保存outの1562件すべてでsurprisalとentropyに欠損がなく、summaryも1562件だった。

`src/analysis/macro/lm_cc_helper/calculate_code_with_boudaries.py:get_code_with_boundaries()` は次の規則を使う。

1. `<0x0A>` を改行に、`▁` を空白に置換する。
2. 先頭トークンを除き、entropyが閾値以上なら分割フラグを立てる。
3. 改行を含むトークンか末尾トークンに達したら、その行の前に境界を挿入する。
4. 境界を1回挿入するごとに、初期値1の `semantic_unit_count` を1増やす。

同じ行に高entropyのトークンが複数あっても加算は1である。先頭行の前の境界も数える。木のroot・内部ノード・葉を数える処理ではない。

`code_block_processor.py:CodeBlockProcessor.parse_code_blocks()` は空行と境界行を取り除く。Tree-sitterのPythonパーサーで階層を作り、関数・制御構文・複数行式の範囲を使ってブロックを入れ子にする。rootは全コードを表す。

`get_lm_cc.py:get_lmcc()` はrootを含めて全ノードを数える。rootの深さを1とし、`LM-CC = 0.2 × 深さの合計 + 0.8 × (ノード数 − 1)` を返す。`lm_cc_density.py` は別の指標である。statementとして印を付けたトークンの `(1 + nesting_depth) × entropy` を関数内で合計し、関数間の平均を返す。LM-CCをLOCで割った値ではない。

`macro/loc.py:calculate()` は残ったトークンの `line` の最大値を返す。空行とコメントを除いた行数ではない。末尾にトークンのない空行は数えない。

## 小さな例

tokensを `['x', '=', '1', '<0x0A>']`、entropyを `[0, 0.8, 0, 0]`、閾値を0.67とする。SU列は2、木はrootだけの1ノード、葉は1、LM-CCは0.2となる。SU数と木のノード数はこの例でも異なる。

`humaneval/HumanEval_0` を0.6813で再計算すると、SUは9、木は8ノード、葉は3、深さの合計は30である。LM-CCは11.6、LOCは10で、保存 `analysis_summary_p67.csv` と一致した。

## 保存値と履歴の照合

- `out/` は9データセット、1562ファイルだった。内訳はHumanEval162、simplified63、top6060、APR271、CT535、simplified APR116、CT198、top50 APR58、CT99である。
- `results/enriched/` の1562件は、tokensとentropyが現outと全件一致した。
- 20個のsummaryでSU・LM-CC・LOCを全件再計算した。`p80` を1.3238へ合わせると、3指標とも20閾値×1562件、計31240件で一致した。再計算時のsummaryとParquetのSHA-256も記録した。
- `p80` を旧表記1.2515で再計算すると、SUは976件一致、586件不一致だった。LM-CCは1044件一致、518件不一致だった。
- 保存p80のSUから許される閾値を求めると `(1.3236970901489258, 1.3238165378570557]` だった。1.3238でSUとLM-CCが1562件すべて一致する。
- コミット `12c12a9` は `pipeline.py:run_pipeline()` の既定値を1.3238、suffixを `_p80` に変更している。ただし同コミットの対象globは `result_HumanEval_2.parquet` だけである。全件生成の実行コマンドは未確認である。
- 現行 `semantic_unit_threshold_analysis.py` の冒頭コメントも1.3238と記していた。
- 無印 `analysis_summary.csv` はSU・LM-CCが `analysis_summary_p10.csv` と1562件すべて一致する。無印を0.67と見なす根拠はない。
- 保存 `semantic_unit_binning/analysis_summary_p80_with_score.csv` は968行である。現outと旧閾値1.2515からSUとLM-CCが968行すべて再現した。`fbfc5c3` のp80 summaryとも一致する。現存p80 summaryの1.3238と世代が異なる。

`calculate_entoropy_thresholds.py` はenrichedのoriginal3データセットをまとめる。968ファイル、329534トークンの非欠損entropyから、現在の67パーセンタイルは0.6812911409、80パーセンタイルは1.2514934778となった。1.3238をどの集合から求めたかは未確認である。

`results/block_trees/` の1562JSONは現outとtokensがすべて一致する。entropyは全件で異なる。JSON内のtokensとentropy、閾値0.67から木を再計算すると、1562件すべて完全一致した。保存JSONは旧entropyを使う木である。現outの木と混ぜてはいけない。

JSONの `code` は1562件すべて `"\n".join(clean_code_lines)` と一致した。各行に元の改行が残るため、1559件で改行を余計に挿入していた。木の `block_code` とは別の文字列である。

BOSの追加は `710d41b`（2026-06-19）の変更である。保存木は先頭entropyがNaNの旧方式と整合する。現outの `meta_created_at` はUTCで2026-06-19 08:21:17から2026-06-20 16:13:32までだった。全件でmodel revisionは未記録、collector_versionは1.0.0だった。モデルを再実行してentropyを検証してはいない。

`scripts/batch.log` は1563件を対象とし、1件で `Invalid buffer size: 188.75 GiB` を記録している。現在CTのParquetは535件で、コードは536件である。`inference.log` にも同種の失敗が残る。ログの日付は6月15日で、現Parquetのメタデータより古い。このログだけで現在のファイルを作った実行回は確定できない。summaryや図を作った時刻・commitも記録していない。

## ソースコードの一致

全1562Parquetのtokensで、SentencePieceの `▁` と `<0xHH>` の全バイト表記を復元した。1561件は先頭の補助空白を1文字除くと現在 `meta_file` のソースと一致した。残る1件は空白を除かずに一致した。元コードとtoken列の対応は確認できた。

ただし現在のSU helperは改行以外のバイト表記を復元しない。109ファイルに `<0x09>` やUTF-8のバイト表記が残る。105ファイルにタブの `<0x09>` がある。木を作る前のソースが元ファイルと変わる制約である。字下げやASTに影響し得るため、次のSU抽出規則の検討で扱う。今回の修正では変えていない。

HumanEvalのdetect dataとlm-cc datasetを比較した。比較式は `ast.dump(ast.parse(text), include_attributes=False)` である。

- original162本は、同じ基底IDのいずれかのvariantと文字列が一致する。
- 基底 `main.py` と文字列が一致するのは79本、ASTが一致するのは158本である。
- ID 1・105・124・150はdetectが派生版を使い、基底ASTと異なる。ID 1は重複したimportの差であり、実処理の違いと断定しない。ID 150は `else` の所属が変わる。
- ID 156はdetectと基底が一致するが、`__1` には末尾の関数呼出しがある。全variantのASTが一致するのは157群である。
- simplified63本とtop6060本は、すべて基底main.pyと文字列が一致した。

## 修正内容とテスト

`generate_block_tree.py` の存在しないimport先を現helperに直した。戻り値も3値から4値へ合わせた。`code` の復元には `"".join(clean_code_lines)` を使い、改行の二重挿入を止めた。出力には数値閾値とSU列を記録する。既定の保存先を `results/block_trees_recomputed/` に変更し、既存ファイルを `open(..., "x")` で保護する。過去JSONは変えない。

`src/analysis/thresholds.py` に保存CSVと照合した閾値を置いた。`run_threshold_experiments.py` はこの表を読む。p80のメタデータを1.2515から1.3238へ直した。過去の `threshold_correlation_results.csv` は変えない。再実行は `--output-dir` の新規ディレクトリへ保存する。省略時は既存の共通処理が時刻とUUIDを含む新しい保存先を作る。

`scripts/audit_saved_semantic_metrics.py` はモデルを読まずにoutからSU・LM-CC・LOCを再計算する。入力summaryとParquetのSHA-256を記録する。出力先は新しいディレクトリだけを受け付ける。

テストは4件成功、0件失敗だった。小例、明示閾値、旧ファイルの保護、実データのp80再現を確認した。

```sh
cd /Users/hyoishitobi/PycharmProjects/detect-llm-hard-to-read
.venv/bin/python -m unittest discover -s tests -p 'test_block_tree_export.py'
.venv/bin/python scripts/audit_saved_semantic_metrics.py --labels p67 p80 --output-dir results/audit-new-run
```

`audit-new-run` が存在する場合は、新しい保存先を指定する。全20閾値を調べるときは `--labels p67 p80` を外す。SU抽出規則とLM-CC式は変更していない。
