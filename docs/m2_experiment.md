# 過去のHumanEval実験の手順と記録

この文書はHumanEvalを対象にした過去の手順と記録である。
今回のxCodeEvalと最小例の実験には、[新しい実験手順](if_else_swap_translation.md)を使う。
以下のコマンドと設定は今回の対象には使わない。

CodeLlama-7bによる計測はM2のMPSで実行する。M4はSSHで起動し、結果をrsyncで受け取る。
M4のPycharmProjects内のリポジトリを最新mainへ更新した。既存の未コミット変更とログは元のパスに保持している。

## 配置

- M4のリポジトリは `/Users/hyoishitobi/PycharmProjects/detect-llm-hard-to-read` にある。
- M2の実験用コピーは `/Users/hyoishitobi/experiments/llm-readability-20261026/detect-llm-hard-to-read` にある。
- コードはmainのコミット `8f1b9dc` を使う。追加した設定と操作スクリプトは未コミットである。
- M2のPython環境は実験用コピーの `.venv` にある。LiteLLMの環境とは別である。
- M2では兄弟の `lm-cc` に入力とテストのコピーを置いている。コピー元の情報は `m2-input-provenance.json` にある。

## 計測条件

`configs/equivalence/if_else_swap_humaneval_m2.toml` を使う。
モデルは `codellama/CodeLlama-7b-hf`、revisionは `6c284d1468fe6c413cf56183e69b194dcfa27fe6` に固定した。
M2のHugging Faceキャッシュへモデルを転送済みで、オフラインで読み込む。
デバイスは `mps`、dtypeは `float16`、文脈は `function_scope` である。

対象はHumanEval_47、123、126、159の4問である。
閾値はリポジトリのサンプル設定と同じ `p67 = 0.6813`、`p80 = 1.2515` を使う。
過去の保存summaryに対応するp80の `1.3238` とは異なるため、結果を混同しない。

この計測にはHugging Face版のモデルを使う。現行の計測コードは全語彙の予測分布から
エントロピーを計算するため、Ollama・LiteLLMの回答APIを計測の代わりには使わない。
回答モデルは未指定として `UNCONFIGURED` を設定した。`accuracy-run` は実行しない。
回答精度も評価する場合は、モデルを決めて別の実験名で設定を作る。

## M4から操作する

```sh
cd '/Users/hyoishitobi/PycharmProjects/detect-llm-hard-to-read'
bash scripts/m2_experiment.sh status
```

4問の変換と動作確認は済んでいる。計測を開始するときは次を使う。
既存の `out/` や保存summaryは書き換えない。

```sh
bash scripts/m2_experiment.sh measure
```

このコマンドはM2で `measure` と `compare` を実行し、M4へ結果をコピーする。
端末はコマンドが終わるまで開いておく。成功済みの計測は再実行しない。
中断した場合は同じコマンドで再開する。失敗は出力先の `status/` とログで確認する。

結果だけを受け取り直す場合は次を使う。

```sh
bash scripts/m2_experiment.sh fetch
```

両マシンとも、本計測の出力先はリポジトリ内の
`results/equivalence/if_else_swap_humaneval_m2_20261026/` である。
比較表は `compare/summary.csv`、各変換の表示は `compare/<ID>/<変換ID>/report.html` にある。
`prepare` は変換と動作確認を再開するコマンドである。

## 準備の確認記録

全テストのログと依存ライブラリの固定用一覧は `results/m2_preflight/` にある。
実測確認にはHumanEval_47だけを使い、本計測とは別の
`results/equivalence/if_else_swap_humaneval_m2_preflight_20261026/` に保存する。
実測確認で得た値は本計測の結果に自動では取り込まない。

## M4の指定フォルダへの反映

最新mainでは分析スクリプトの配置が変わっている。既存の編集済みファイルは旧パスに保持した。
その編集を新配置の分析スクリプトへ移植したわけではない。今回のM2計測は新しい `src/equivalence/` を使う。
M4の反映後テストは75件成功、失敗は0件だった。元からあった391ファイルはハッシュがすべて一致した。
記録は `results/m2_preflight/m4-reflection-pytest.log` と `m4-preservation.json` にある。
