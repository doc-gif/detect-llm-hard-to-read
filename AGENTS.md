# このリポジトリで作業するエージェントへ

ここはSU数とLLMの回答精度を調べる実験用リポジトリです。兄弟の`../lm-cc`も本人の追加実装を含みます。変更のない先行研究クローンとは扱わないでください。

## 読む順序

1. [docs/README.md](docs/README.md)と[プロジェクト構造](docs/project.md)で役割と入口を確認してください。
2. [調査結果](docs/audit.md)で保存値の世代、既知の問題、再現手順を確認してください。
3. 変更する範囲に応じて[SUの計算](docs/su-calculation.md)、[回答の計算](docs/score-calculation.md)、[結合と分析](docs/analysis-calculation.md)を読んでください。
4. 分析方法を変える前に[今後の分析案](docs/analysis-plan.md)を読んでください。

## 作業前と編集時

- 両リポジトリの`git status`、`git remote -v`、履歴を確認してください。未コミットのコード、ログ、画像、未追跡データを保持してください。
- `data/`、`out/`、既存の`results/`は研究の入力と過去の結果です。新しい結果は別のディレクトリへ出してください。出力先を確認せず、過去のバッチ入口を実行しないでください。
- `src/analysis/pipeline.py`は保存表とenriched Parquetを書き換えます。計算の確認には`docs/audit.md`の読み取り用スクリプトを使ってください。
- HumanEvalの`__0`と`__1`は派生設問です。IDを切り詰めて辞書へ代入しないでください。設問の5回平均と、複数設問をまとめた平均を区別してください。
- 結合キーは`(dataset, uid)`です。完全IDだけでなく、測定コードと採点コードの一致も確認してください。除外はIDと理由を残してください。
- SU数の定義は`macro/lm_cc_helper/calculate_code_with_boudaries.py`にあります。木のノード数への置き換えは、不具合修正とは別の指標変更です。
- p67の閾値は`0.6813`、保存p80の閾値は`1.3238`です。無印`analysis_summary.csv`は名前から閾値を判断できません。今回の再計算ではp10と一致しました。
- 群数や閾値を探索した最大相関を、事前に固定した分析の結果として報告しないでください。図の回帰線と相関は同じ代表点を使ってください。
- 計算を変えたら、最小例のテストと保存値の比較を付けてください。論文の定義、現在の実装、保存値、実行ログを区別してください。
- モデルのダウンロード、回答の再生成、APIでの大量測定は、保存データの調査には不要です。必要になったら作業範囲を確認してください。

## 実行方法

リポジトリ直下で実行してください。既存の`.venv`を使います。再現コマンドと出力は[docs/audit.md](docs/audit.md)にまとめています。

```sh
PYTHONPATH=.:src:src/analysis .venv/bin/python -m unittest discover -s tests
```

主要な入口は`src/collect_metrics.py`、`src/analysis/pipeline.py`、`src/analysis/semantic_unit_threshold_analysis.py`です。列名は`src/schema/records.py`に定義しています。

## 日本語

[日本語の書き方](https://github.com/doc-gif/.github/blob/main/japanese-writing.md)を読み、投稿前のチェックリストで確認してください。チャットとコメントは「です・ます」、`docs/`は「だ・である」にそろえてください。
