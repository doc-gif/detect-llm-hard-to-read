# if-else入れ替え実験の手順

## 1. スクリプトの使い方

13組の実験には `scripts/run_if_else_samples.py` を使う。操作はすべてM4から始める。

```sh
cd /Users/hyoishitobi/PycharmProjects/detect-llm-hard-to-read
.venv/bin/python scripts/run_if_else_samples.py <段階>
```

| 段階 | 実行すること |
|---|---|
| `behavior` | M4で13組の入出力を比較する。 |
| `stage` | 入力・コード・設定・動作テストの結果をM2へコピーして検証する。 |
| `measure` | M2のCodeLlamaで26本のPythonコードを計測する。 |
| `compare` | M2で13組のSU数・境界・エントロピーを比較する。 |
| `fetch` | 結果をM4へ受け取り、M2で作った一覧と全ファイルのハッシュを照合する。 |
| `status` | M4側の状態を表示する。`--remote` を付けるとM2側を確認する。 |

設定は `configs/equivalence/if_else_samples.toml` にある。`--config` で別の設定も指定できる。
成功済みの対象は、出力のハッシュを確認してからスキップする。失敗分は同じコマンドで再試行する。
複数の端末から同じ出力先へ同時実行することはできない。

抽出をやり直す場合だけ `scripts/prepare_if_else_samples.py` を使う。
`--output-dir` には新規ディレクトリを指定する。既存の入力は上書きしない。

```sh
.venv/bin/python scripts/prepare_if_else_samples.py --verify
```

この確認は入力のハッシュ・構文・行数だけを調べる。
準備時の `manifest.json` とその `not_run` 表示は更新しない。実行後の状態は `status` で確認する。

### 現在の状態

- xCodeEvalの10件と最小例3件は、元コード・入れ替えコード・テストを保存済みである。
- 13組・962ケースで、既存テストに対する出力一致と正常終了を確認した。
- 2件には保存正解との厳密な文字列比較で不一致がある。詳細は後述する。
- M2への配置と、動作確認結果15ファイルの受信・ハッシュ検証は完了した。
- エントロピーとSU数は未計測である。今回の13組にCodeLlamaは使っていない。
- スクリプトのテストは90件成功、失敗は0件だった。計測の経路は一時ディレクトリのダミーモデルで検証した。

過去の `scripts/m2_experiment.sh` はHumanEval用であり、今回は使わない。
Cへの翻訳と回答精度の評価も、今回のスクリプトには含めない。

## 2. 対象を選ぶ

目的：エントロピーやSU数を見ずに対象を固定し、選んだ過程を再現できるようにする。

今回採用したルールは次のとおりである。

1. `lm-cc/dataset/xcodeeval/code_translation/xcodeeval_codetranslation_test_filtered.jsonl` を読む。
2. `source_code` がPythonとして構文解析でき、変換可能な複数行形式のif-elseを持つものを候補にする。
3. 各コードの先頭の変換可能なif-elseを1か所だけ選ぶ。`elif`を含む箇所は使わない。
4. 選んだ箇所の変換が構文・AST・行数の検査に通り、既存の入出力テストがあることを確かめる。
5. 空行・コメントを含む物理行数 `len(source_code.splitlines())` で、候補を3群に分ける。
6. 各群をID順に並べ、`random.Random(20261026)` で短・中・長の順にシャッフルする。
7. 各群の先頭から3・4・3件を採用する。残りの順序も補充候補として記録する。

群の境界には、候補のLOCを昇順に並べた三分位点を使う。
位置 `(件数−1) × p` を線形補間し、計算には有理数を使う。
第1境界以下を短い群、第2境界以下を中程度、残りを長い群に入れる。
同じLOCを別群に分けない。候補不足なら処理を止め、群の件数を報告する。

今回は536件中217件が候補となり、319件には条件に合うif-elseがなかった。
境界は19行と32行だった。群ごとの候補数と抽出数は次のとおりである。

| 群 | 選定用LOC | 候補数 | 抽出数 |
|---|---|---:|---:|
| 短い群 | 19行以下である。 | 75 | 3 |
| 中程度 | 20〜32行である。 | 70 | 4 |
| 長い群 | 33行以上である。 | 72 | 3 |

`candidates.csv` に全536件の採否と理由を保存した。
`selection.json` に境界、シード、抽出順、採用IDを保存した。補充はしていない。
動作テストで問題が見つかっても、理由を残さず対象を差し替えない。
選定用LOCは、後でトークン表から求めるLOCとは区別する。

## 3. コピーと変換を確認する

目的：元データを保持し、各変更を単独で確認できるようにする。

元コードはタスクJSONLの `source_code` をUTF-8のバイト列として保存した。
改行・空白・コメントは正規化していない。元JSONLの行番号とハッシュも記録した。
自作の最小例は、大小比較・剰余・複数条件の3件で、いずれも5行である。

```text
experiments/if_else_swap_translation_20261026/
  candidates.csv               全入力の採否と理由を記録する。
  selection.json               群の境界と抽出順を記録する。
  samples.csv                  13組の場所と選定用LOCを記録する。
  manifest.json                入力元、検査結果、ハッシュ、未実行の段階を記録する。
  xcodeeval/<問題ID>/           翻訳タスクから選んだコードを置く。
  minimal/<例の名前>/           自作の最小例を置く。
```

各サンプルのディレクトリには次のファイルがある。

| ファイル | 内容 |
|---|---|
| `original.py` | 元コードを保存する。 |
| `swapped.py` | 条件を否定して本体を交換したコードを保存する。 |
| `diff.patch` | 元コードとの差分を保存する。 |
| `transform.json` | 対象行、編集内容、行対応、構文・AST・行数の検査結果を保存する。 |
| `tests.json` | 入出力テストを保存する。パッケージ内の実行状態は `not_run` とする。 |
| `source_record.json` | xCodeEvalだけに置き、元の問題レコードを保存する。 |

確認コマンドは次のとおりである。

```sh
.venv/bin/python scripts/prepare_if_else_samples.py --verify
```

期待する出力：`samples` が13、`verified_files` が78となる。
`behavior_status` と `measurement_status` は `not_run` のままである。
サンプル別のリンクは [用意したコードの一覧](if_else_swap_samples.md)にある。

困ったとき：`Hash mismatch` は準備後にファイルが変わったことを示す。
書き換えて合わせず、対象パスとエラー全文を報告する。
`Output already exists` は再抽出で既存の出力先を指定した場合に出る。
既存の結果を確認するなら `--verify`、再現確認なら別の `--output-dir` を使う。
入力がなければ兄弟の `lm-cc` または `--source-jsonl` を確認する。

## 4. 実験を進める

### 4.1 動作を比較する

目的：同じエラーで落ちたコードを成功扱いせず、変換前後の動作一致を確認する。

```sh
.venv/bin/python scripts/run_if_else_samples.py behavior
```

期待する出力：`behavior` が `expected: 13, ok: 13` になる。
各テストで両方が正常終了し、stdoutが完全に一致し、例外やタイムアウトがないことを条件とする。
`behavior/summary.csv` と対象別のJSONに出力・終了コード・保存正解との比較を残す。
この一致は用意した入力での確認であり、全入力での等価性の証明ではない。

保存正解との比較は、既存の採点関数を使った厳密な文字列比較である。
今回は `require_expected_output = false` とし、動作一致の判定とは分けて記録する。
同じ出力でも保存正解と異なる場合があるため、正解性の確認済みとは扱わない。
`true` にすると保存正解との一致も計測の条件になる。変更時は出力先も変える。

現在、次の2件に保存正解との不一致がある。サンプルは差し替えていない。

- `0469a415b73c86652f520eaf69bd7311` は45ケース中38ケースで不一致だった。
- `0709e40ee49b6439d328de121380ddcb` は59ケース中59ケースで不一致だった。

両方とも元コードと入れ替えコードの出力は全ケースで一致した。
後者には `['No', 'NO', 'no']` のような正解表現が含まれ、既存の厳密比較だけでは正解性を判断できない。
回答精度の評価へ進む前に、この2件の正解判定を別途確認する。

困ったとき：`failed` なら計測へ進まない。
対象ID、`behavior/<データセット>/<ID>.json`、`logs/behavior.log` を報告する。
タイムアウトの制限は設定の `timeout_sec` で確認する。変更する場合は別の出力先を使う。

### 4.2 M2へ配置する

目的：固定した13組と実装をM2に置き、同じ入力を使う。

```sh
.venv/bin/python scripts/run_if_else_samples.py stage
```

期待する出力：入力78ファイルを検証し、13組の動作確認が成功した状態を表示する。
M2の配置先は `/Users/hyoishitobi/experiments/if-else-translation-20261026` である。
既存のM2用Python環境を `.venv` から参照する。モデルの読み込みと計測は始めない。

困ったとき：SSH失敗ならM2の起動とネットワークを確認する。
`Remote file was modified` は配置後にM2のコードや入力が変わったことを示す。
上書きして合わせず、パスとエラー全文を報告する。
Python環境が見つからない場合は設定の `remote.venv_source` を確認する。

### 4.3 M2で計測する

目的：同じモデルと設定で、元コードと入れ替えコードのエントロピーを得る。
このコマンドを実行すると、初めてCodeLlamaを読み込む。

```sh
.venv/bin/python scripts/run_if_else_samples.py measure
```

期待する出力：`measure` が `expected: 26, ok: 26` になる。
入力のハッシュと13組の動作確認を検査し、成功している場合だけM2で計測する。
計測中は端末を開いておく。中断後は同じコマンドで再開する。

モデルは `codellama/CodeLlama-7b-hf`、revisionは `6c284d1468fe6c413cf56183e69b194dcfa27fe6` とする。
デバイスは `mps`、dtypeは `float16`、文脈は `function_scope` とする。
オフラインで読み込み、欠けたモデルのダウンロードはしない。

困ったとき：モデル不足ならM2のキャッシュとrevisionを確認する。
メモリ不足なら不要なモデルを終了し、同じ設定で再試行する。
解決しなければ、対象IDとM2側の `logs/measure.log` を報告する。
モデルやdtypeを変えるときは、別の出力先を指定する。

### 4.4 SU数とエントロピーを比較する

目的：SUの増減と、条件行・移動した本体・後続部分の変化を確認する。

```sh
.venv/bin/python scripts/run_if_else_samples.py compare
```

期待する出力：`compare` が `expected: 13, ok: 13` になる。
SUの計算には既存の関数を使う。主な比較は `p67 = 0.6813`、補助の比較は `p80_saved = 1.3238` とする。
過去のサンプル設定の `1.2515` は今回は使わない。
比較表には保存正解との不一致も記録する。

困ったとき：`Measurement missing` ならM2の状態を確認し、`measure` を再実行する。
その他の失敗は対象IDとM2側の `logs/compare.log` を報告する。
`Output hash mismatch` が出た場合は、ファイルを手で直さない。

### 4.5 M4へ結果を受け取る

目的：M2の結果をM4へコピーし、欠落と転送中の変更を検出する。

```sh
.venv/bin/python scripts/run_if_else_samples.py fetch
.venv/bin/python scripts/run_if_else_samples.py status
```

期待する出力：受信したファイルのハッシュ検証に通り、`measure` が26件、`compare` が13件成功している。
結果の保存先は、両マシンともリポジトリ内の
`results/equivalence/if_else_translation_13_20261026/` である。

- `compare/summary.csv` に13組の比較を保存する。
- `compare/xcodeeval_code_translation.csv` と `compare/minimal.csv` に対象別の比較を保存する。
- `compare/<データセット>/<ID>/report.html` に元コードと入れ替えコードを並べて表示する。
- `receipt.json` にM2で作ったハッシュ一覧と段階ごとの状態を保存する。

`fetch` は途中までの結果も受け取れる。転送成功だけで計測完了とは判断せず、状態の件数も確認する。
M2だけの状態を確認するときは次を使う。

```sh
.venv/bin/python scripts/run_if_else_samples.py status --remote
```

困ったとき：通信が切れたら同じ `fetch` を再実行する。
`Received file hash mismatch` が残る場合は、対象パスとエラー全文を報告する。
計測中の `Another stage is running` は、その処理が終わってから再試行する。

### 設定を変える場合

入力・実装・設定を変えた結果を、同じ出力先には混ぜない。
`Conditions, inputs or code changed` が出た場合は、新しい `experiment.output` を使う。
設定ファイルのコピーを作り、以降の各コマンドに同じ `--config <パス>` を付ける。
M2への配置先も変える場合は `remote.root` を新規ディレクトリにする。

## 5. 結果から判断する

最小例とxCodeEvalは別々に集計する。SUが増加・減少・不変のすべてを残す。
動作とLOCを保ってSUを変えられるかを確認する。
トークン数やエントロピーも変わる場合は、SU以外の変化として記録する。
条件行・移動した本体・後続部分の境界とエントロピーを確認する。
SUが変わらない例は、書き方だけを変える対照の候補として残す。

この段階では「SU数だけを変えられた」「SUが回答精度低下の原因である」とは結論しない。
回答精度の実験に使える変換と対照を探すことを目的とする。
