# LOC変更9組の計測・比較

`loc_variation_9pairs.zip`は、処理を変えずに書式とLOCを変えた合成コード9組である。セミコロンで文を結合した3組、`if`本体を同じ行に置いた3組、ループ本体を同じ行に置いた3組を含む。条件の否定や分岐順序の交換はない。[if-else入れ替え実験](if_else_swap_translation.md)とは別の実験として扱う。

この文書はコードの仕様である。モデルによる計測は未実行で、SU数やエントロピーの結果は含まない。

## 入口

| 場所 | 役割 |
| --- | --- |
| `scripts/run_loc_variation.py` | 段階を明示して実行する入口 |
| `configs/equivalence/loc_variation_9pairs.toml` | 入力、出力先、モデル、閾値 |
| `src/equivalence/loc_variation.py` | 取り込み、動作検証、計測、比較、一覧、再開 |
| `src/equivalence/statement_alignment.py` | 処理文の対応と、トークンの所属文 |
| `src/equivalence/_run_cases.py` | `tests.json`を実行する子プロセス |
| `tests/test_loc_variation.py` | モデル不要のテスト |

再利用した既存の処理は次のとおりである。SUの定義とエントロピー計算は変更していない。

- `collect_metrics.collect`と`ParquetWriter`は、`equivalence.measure.measure_file`経由で呼ぶ。
- `compare.file_metrics`と`compare.semantic_units`は、LOC、トークン数、SU数、境界、範囲、原因トークンを求める。
- `compare.token_table`は、トークン表の土台にする。

`compare.token_alignment`は使わない。行の対応を使い、多対一の行対応では変換後のトークンを複数の変換前トークンの相手に重複して使う。LOCが変わる変換では、行の対応そのものが成り立たない。

## 入力の取り込み

zipまたは展開済みディレクトリを直接読む。`manifest.json`の配列の各項目から、`original`と`transformed`のパスを引く。同じディレクトリの`tests.json`と、あれば`change.diff`も読む。

- `case_id`、`category`、`title`は、manifestの値をそのまま保存する。
- `original_sha256`と`transformed_sha256`が実ファイルと違えばエラーにする。`..`や絶対パスもエラーにする。
- `test_count`と`tests.json`の件数が違えばエラーにする。
- manifestのLOCと`splitlines()`の行数の差、変換前後のLOCの差はエラーにしない。記録する。
- 呼び出す関数名は、既定で`run`である。設定の`experiment.entry`か、manifest項目の`entry`で変える。

## 動作検証

`tests.json`の各要素の`args`を`entry(*args)`へ渡し、JSONへ往復した結果を`expected`と比べる。子プロセスで実行し、時間切れは`behavior.timeout_sec`で打ち切る。`list`と`tuple`は同じ表現になる。

- 変換前と変換後の両方が全件一致したときだけ成功とする。
- LOCが変わることは失敗にしない。
- 位置を除いたASTが等しいかを記録する。等しくなくても失敗にはしない。
- 構文エラー、例外、関数名の欠落、時間切れは失敗にする。失敗した組は計測しない。

## 処理文の対応

`token_alignment`の代わりに、位置情報を除いたASTの一致を使う。

1. `ast.parse`で得た`ast.stmt`を、出現順に並べる。
2. 各文から「位置属性を除き、入れ子の文の並びを`[S*]`に置き換えた`ast.dump`」(`head_key`)を作る。`if`なら条件式、`def`なら名前と引数になる。子の文の個数は含めない。
3. 変換前後の`(head_key, 入れ子の深さ)`の列を、difflibの最長一致で突き合わせる。結果は1対1で、同じ文を2回使わない。一致しない文は片側だけの行に残す。
4. 部分木まで含めた`ast.dump`が等しければ`same_subtree`、見出しだけ等しければ`same_head`とする。

`lineno`などの位置は、対応づけに使わない。9組はすべて文の数が一致し、全てが`same_subtree`になる。`;`、`else`、`:`は文ではないため、囲む文の所有になる。

## トークンの所属とまたぎ

各トークンは、ちょうど1つの文に割り当てる。

- トークンの文字範囲は、開始位置から次のトークンの開始位置までとする。最後のトークンはソース末尾までとする。
- 所有者は、範囲内の最初の非空白文字を含む最も内側の文とする。どの文にも入らなければ`OUTSIDE`(-1)とする。`collect_metrics`がAST情報を引く位置と同じ規則である。
- 空白だけのトークン(インデント、改行)は、先頭の文字の所有者に割り当てる。`is_whitespace`で区別できる。

トークンが文の境界をまたぐ場合は、次のとおり扱う。

- 範囲内の非空白文字が2つ以上の所有者にまたがるトークンは、`crosses_boundary=True`にする。関係する所有者を`spanned_owners`に残す。
- 割り当ては先頭の非空白文字の所有者だけである。トークンを分割も複製もしない。したがって、各側のトークン数の合計は、総トークン数と一致する。
- 例として`a = 1; b = 2`で`; b`が1トークンなら、所有者は`;`の位置の`OUTSIDE`になる。`b = 2`のトークン数はその分少なくなる。文ごとの数値を読むときは、`n_crossing_tokens`も見る。

## 実行

リポジトリ直下で、既存の`.venv`を使う。

```sh
# 入力の検証と一覧。出力ディレクトリは作らない。
.venv/bin/python scripts/run_loc_variation.py check --cases all

# tests.jsonによる動作検証。モデル不要。
.venv/bin/python scripts/run_loc_variation.py behavior --cases all

# 初回の計測。モデルを読み込むので--run-modelが必要。セミコロン、if、ループから1組ずつ選ぶ。
.venv/bin/python scripts/run_loc_variation.py measure --cases s01_invoice,i01_absolute,l01_sum --run-model

# 比較と一覧。モデル不要。
.venv/bin/python scripts/run_loc_variation.py compare --cases s01_invoice,i01_absolute,l01_sum
.venv/bin/python scripts/run_loc_variation.py summary
```

- `--cases`は`first3`(既定、manifestの先頭3組)、`all`(全9組)、`first:N`、`id1,id2`から選ぶ。`first3`はセミコロンの3組(`s01_invoice`、`s02_time`、`s03_sales_report`)だけで、`if`とループを含まない。初回の実行例は3種類から1組ずつ選ぶため、IDで指定する。
- `--repetition K`は反復ID Kだけ、`--repeat N`は反復ID 1〜Nを対象にする。既定は反復ID 1である。
- 設定の`measure`を`dummy`に変えると、モデルなしで流れを確認できる。研究の計測には使わない。
- モデルのダウンロードとLLM計測は、今回は実行していない。

## 保存先と再開

出力先は、設定の`experiment.output`(`results/loc_variation_9pairs`)である。既存の`data/`、`out/`、`results/`の既存ディレクトリ、`experiments/`、入力パッケージと重なる場合はエラーにする。印のないままファイルがある出力先も使わない。

```text
<output>/loc_variation_run.json
<output>/<条件キー>/condition.json
<output>/<条件キー>/inputs/<case_id>/{original,transformed}.py
<output>/<条件キー>/behavior/<case_id>.json
<output>/<条件キー>/rep_NNN/measure/<case_id>/{original,transformed}.{parquet,json}
<output>/<条件キー>/rep_NNN/compare/<case_id>/…
<output>/<条件キー>/{summary_all.csv,summary_all.md,repeatability.csv}
```

- 条件キーは、モデル、revision、device、dtype、文脈戦略、閾値、収集器の版、入力のmanifestのSHA-256から決める。対象ケースの選択は含めない。
- 同じ条件キーと反復IDで、成功済みかつ出力のハッシュが一致する項目は、計測し直さない。3組の後に全9組へ広げると、3組は再開される。
- 動作検証の成功を再利用する条件は、manifestのSHA-256に加えて、ケースごとの`tests_sha256`(`tests.json`全文のSHA-256)と実効的な`entry`である。`entry`は、manifestの行に`entry`があればそれ、なければ設定の`experiment.entry`である。`test_count`が同じまま`args`や`expected`を変えた場合と、`entry`を変えた場合は、古い成功を使わずに検証し直す。直前の結果は上書きせず、`behavior/superseded/<case_id>.<ハッシュ先頭12桁>.json`に残す。`tests_sha256`と`entry`を持たない古い保存値も、再検証の対象になる。
- 反復IDが違えば、別の`rep_NNN`に計測する。条件が違えば、別の条件キーのディレクトリになる。
- 保存済みの出力や入力のハッシュが違う場合は、上書きせずにエラーにする。失敗した項目だけを再実行する。
- 反復どうしの再現性は、`repeatability.csv`に最初の反復との差として出る。

## 計測結果の検査

計測のたびに、Parquetのトークン表を次の規則で検査する。1つでも違反すれば、その項目は失敗にし、成功済みとして保存しない。

- トークン表が空でないこと。モデル名とrevisionが設定と一致すること。
- `entropy`は、全件が有限値であること。一部欠損、全件欠損、非有限値(`inf`)を、それぞれ別のエラーにする。例外は設けない。
- `surprisal`は、既定では`entropy`と同じ規則とする。
- 設定の`validation.allow_leading_surprisal_missing = true`のときだけ、`surprisal`の先頭トークン(`idx`が最小の行)の欠損を許す。これは`entropy`の規則とは別である。2番目以降の欠損と非有限値は許さず、全件欠損は先頭だけの欠損とは区別して拒否する。
- BOSを持たないモデルは、先頭トークンの`surprisal`と`entropy`が両方欠損する。`entropy`は例外なしなので、この場合は検査に通らない。使用予定のCodeLlamaはBOSを持つため、既定のままでよい。

適用した規則は、`measure/<case_id>/<version>.json`の`validation`に保存する。

## 保存する内容

計測ごとの`measure/<case_id>/<version>.json`には、次を保存する。

- 実入力の全文、バイト数、SHA-256、入力の複製のパス
- モデル名、revision、トークナイザ、設定のdeviceとdtype、実際に解決されたdeviceと読み込んだdtype
- 反復ID、条件キー、閾値、開始・終了時刻、所要時間、Pythonと主要パッケージの版、コードのGit情報

比較ごとの`compare/<case_id>/`には、次を保存する。

- `summary.json`は、前後の指標、閾値、閾値ごとのSU数、SUの範囲、境界、原因トークン、文の対応を持つ。
- `statements.csv`は、対応づけた文ごとの行数、トークン数、エントロピー、原因トークン数の前後と差を持つ。
- `su_units.csv`と`trigger_tokens.csv`は、SUの範囲と、境界を作ったトークン(所有する文と対応IDを含む)を持つ。
- `tokens_original.csv`と`tokens_transformed.csv`は、トークンごとの値、所有者、またぎの有無、SU番号を持つ。

`summary_all.csv`と`summary_all.md`は、LOC、トークン数、閾値ごとのSU数、平均エントロピー、PPL、LM-CCの前後と差を、反復とケースごとに並べる。LOCは`loc.calculate`(トークンが存在する最大の行番号)で、`loc_source_*`は`splitlines()`の行数である。閾値は`p67`が`0.6813`、`p80_saved`が`1.3238`である。

## 確認したこと

- 9組すべてで、manifestのSHA-256と`tests.json`の5件が両方の版で一致し、ASTが等しい。
- 9組すべてで、文が1対1で対応し、対応なしの文がない。
- ダミーモデルで、動作検証から一覧までを通し、再開、別反復、上書き防止、出力先の重なりの拒否を確認した。
- `pytest tests`の107件(今回の17件を含む)が通る。`unittest discover`が拾うのは従来どおりunittest形式の31件で、今回のテストはpytest形式である。

```sh
PYTHONPATH=.:src:src/analysis .venv/bin/python -m pytest tests
PYTHONPATH=.:src:src/analysis .venv/bin/python -m pytest tests/test_loc_variation.py
```
