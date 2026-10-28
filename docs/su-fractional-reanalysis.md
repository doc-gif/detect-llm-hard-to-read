# SU数と回答精度の分数ロジット再分析

監査済みの964コードで、全体の回帰とSU区間内部の評価を実行した。2026年10月20日の探索的な再分析である。独立した確認実験や事前登録済みの分析とは呼ばない。

[結果の本文](../results/reanalysis/2026-10-20-fractional-logit-reviewed/report.md)に、課題別の結論、全比較、図、制約、再現手順をまとめた。今回の指定に従い、1コード1観測の分数ロジットを使った。[従来の分析案](analysis-plan.md)にある二項回帰やGAMの実行結果とは区別する。

実行入口は`scripts/run_su_fractional_analysis.py`である。`prepare`が入力、正解数・試行数、コード対応を確認し、精度を使わず区間境界を保存する。`fit`が保存設定を使い、入力ハッシュを照合してから回帰を実行する。既存の出力先は拒否する。

```sh
.venv/bin/python scripts/run_su_fractional_analysis.py prepare --output-dir results/reanalysis/new-run
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/codex-mpl .venv/bin/python scripts/run_su_fractional_analysis.py fit --run-dir results/reanalysis/new-run
```

結果には`2026-10-20-fractional-logit-reviewed/`を使う。先の`2026-10-20-fractional-logit/`は診断表示の修正前の記録である。中間値の回答平均が少ないだけで判断困難にする条件を取り除いた。両実行の入力・境界・推定値・信頼区間・p値・予測値は一致する。

既存のSU規則、回答生成、entropy測定は変更していない。APRの元問題内の依存には`src_uid`でまとめたCR1共分散を使う。HumanEvalと翻訳は1コード1群で、同じ式はHC1になる。詳しい式と推定上の制約は結果本文に記した。

[Notionの結果ページ](https://app.notion.com/p/3fe99c5c4c9381febf67e5b2d6960cf0)にも本文と図14点を掲載した。「評価方法と既存データ」「検証計画」から参照できる。全ファイルのZIPはローカル保存であり、Notionには添付していない。
