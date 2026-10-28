# プロジェクトとデータの流れ

`detect-llm-hard-to-read`はSU数を含む指標の収集と分析を担当する。`lm-cc`は課題データ、回答と採点結果、先行研究由来の実装、本人が追加した指標計算と分析を持つ。二つを兄弟ディレクトリに置く構成である。

## 調査開始時の状態

| リポジトリ | HEAD | origin |
| --- | --- | --- |
| `lm-cc` | `96dd50f384240a2f75c377b9a109baee8d1d099d` | `https://github.com/doc-gif/lm-cc.git` |
| `detect-llm-hard-to-read` | `2476ee6bfad24e217c0baf465b7709d21608b8c7` | `git@github.com:doc-gif/detect-llm-hard-to-read.git` |

開始時には両リポジトリに`AGENTS.md`も`docs/`もなかった。`lm-cc`には先行研究由来の`README.md`があった。`lm-cc`の6月11〜21日の4コミットは、本人の追加処理とデータを含む。`detect`には6〜7月の指標追加、閾値の比較、区間集計の履歴がある。

`lm-cc`には、`scripts/plot_lmcc_scatter.py`と散布図3枚の未コミット変更があった。LOCのJSON、比較図、抽出済みコード、IDE設定も未追跡だった。`detect`には未追跡の`inference.log`と`.DS_Store`があった。開始時の一覧とハッシュは[記録](evidence/initial-state.json)に残した。既存の変更と過去の出力を保持した。

## 入力から図まで

```text
lm-cc/dataset/（設問、コード、テスト）
  ├─ scripts/tasks/ → lm-cc/results/（回答、各回の判定、平均）
  ├─ 保存entropy → scripts/calc_lmcc_from_entropy.py → lm-cc/out/lm_cc/
  └─ extract_datasets.py → data/*.py
                              ↓
detect/scripts/batch_runner.py → src/collect_metrics.py
                              ↓
detect/out/*/result_*.parquet（トークン値と測定メタデータ）
                              ↓
src/analysis/pipeline.py → results/summaries/analysis_summary*.csv
                              ↓ 完全ID、課題名、コードの一致を確認
lm-cc/results/ の回答精度 ────┘
                              ↓
correlation_analysis / semantic_unit_threshold_analysis /
semantic_unit_model_comparison / plot_analysis_scatter
                              ↓
相関、区間表、曲線の比較、散布図
```

`extract_datasets.py`は`lm-cc`側にある。HumanEvalの派生IDを基本IDにまとめ、先着のファイルを採用するため、基本IDの設問と抽出コードが同じとは限らない。結合時にはこの差を確認する。

## 主要な入口

| 入口 | 役割と編集時の注意 |
| --- | --- |
| `scripts/batch_runner.py` | `data/`を走査してトークン値を測る。モデルを読み込むため、保存データの監査では実行しない。 |
| `src/collect_metrics.py` | 言語処理、モデル、文脈、保存処理をつなぐ。採点は担当しない。 |
| `src/schema/records.py` | `TokenRecord`、`FileMetadata`、`ParquetSchema`、`SummarySchema`が列名を定義する。 |
| `src/analysis/pipeline.py:process_file` | ParquetからSU、LM-CC、LOCと補助指標を求める。既定の入口は保存表を書き換えるため、監査では使わない。 |
| `src/analysis/semantic_unit_threshold_analysis.py` | 指標と回答精度を結合し、SU幅1・5・10の表と図を作る。 |
| `src/analysis/semantic_unit_model_comparison.py` | 直線、hinge、step、4パラメータ曲線を比較する。末尾の起動処理がどちらの分析を呼ぶかも確認する。 |
| `src/analysis/correlation_analysis.py`と`util/correlation.py` | 群の代表値を使う相関と偏相関を求める。過去の群数探索が残っている。 |
| `src/analysis/generate_block_tree.py` | 保存トークン値から木を出力する。SU数を木のノード数へ置き換える処理ではない。 |
| `lm-cc/scripts/tasks/` | HumanEval、APR、翻訳の回答生成と採点を持つ。再実行はAPI呼び出しや生成コードの実行を伴う。 |
| `lm-cc/scripts/run_lmcc_correlation.py` | 本人が追加した保存LM-CCと回答精度の分析である。先行研究のシェル入口と区別する。 |

## ディレクトリと列

`data/`は指標を測るコードを持つ。`out/`は測定したトークン値を持つ。`results/enriched/`は追加列を持つParquet、`results/summaries/`は1コード1行の表である。`results/semantic_unit_binning/`は旧結合表と区間表を持つ。`results/semantic_unit_model_comparison/`は曲線比較の結果を持つ。

| 列 | 意味 |
| --- | --- |
| `dataset`, `uid` | 課題区分とファイルIDである。組で一意に扱う。HumanEvalの`__0`と`__1`は反復回数ではなく派生設問を示す。 |
| `num_semantic_units` | 現行の境界抽出処理が返すSU数である。木の全ノード数や葉数とは違う。 |
| `lm_cc` | 木の深さ合計と枝数から求める値である。詳細は[計算記録](su-calculation.md)に示す。 |
| `loc` | detectではsurprisal欠損を除いたトークンの最大行番号である。lm-ccでは非空行数であり、コメントとdocstringの行も数える。 |
| `pass_at_1` / `score` / `pass@1` | 処理ごとに名前が異なる回答精度である。HumanEvalの設問ごとの保存値は正解数÷5に一致した。 |
| `ppl` | 保存surprisalの平均から求めるperplexityである。回答精度とは違う。 |
| `total_tokens` | pipelineでsurprisal欠損を除いた後のトークン行数である。 |
| `num_functions` | 関数開始トークンの抽出件数である。Pythonの関数定義数と無条件には同一視しない。 |
| `avg_first_token_surprisal` | 関数開始トークンのsurprisalの平均である。 |
| `avg_context_surprisal_gap` | 関数文脈のsurprisalから全文脈のsurprisalを引き、欠損を除いて平均した値である。 |
| `lm_cc_density` | 関数内の文開始で`(1 + nesting_depth) × entropy`を足し、関数ごとの合計を平均する。木から求めるLM-CCやSU密度とは別の式である。 |
| `cyclomatic_complexity`, `cognitive_complexity` | `meta_file`の元コードを静的解析した補助指標である。現在の元ファイルを読むため、保存トークンとコードの世代が一致するか確認する。 |

## 論文との区別

[LM-CC論文v1](https://arxiv.org/html/2602.07882v1)の式4は、枝数と深さ合計の加重和を定義する。付録Cは、指標の中央値と回答精度の平均を群の代表値とし、9〜11群を比較する。論文では有意な結果から絶対値が最大の相関を選ぶ。

本人の実装では、p値の条件をコメントアウトした箇所がある。`lm-cc`は負相関だけを候補とし、`detect`には正負の両方を候補にする処理がある。論文の説明を、そのまま本人の実装や保存結果の説明には使わない。

論文には閾値を`0.67`とする記述と、67パーセンタイルとする記述がある。ローカル実装の数値`0.67`、p67の`0.6813`、保存p80の`1.3238`は区別する。現存summaryは`1.3238`だが、スクリプトは旧`1.2515`のままだった。今回、現存summaryに合わせた。SU抽出規則を変更する場合は、新しい指標として別の分析を用意する。
