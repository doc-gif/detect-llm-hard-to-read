# アーキテクチャ

このリポジトリは「LLM にとって読みにくいコード」を、LLM 自身のトークン予測の不確かさ
(surprisal / entropy) から定量化する研究用コードです。先行研究
[LM-CC](https://github.com/doc-gif/lm-cc) (以下 lm-cc) の指標を再実装・拡張し、
LLM の正答率 (pass@1) との相関を調べます。

## 全体の流れ

```
data/<dataset>/*.py                         ソースコード (入力)
   │
   │  Phase 1: src/collect_metrics.py   (scripts/batch_runner.py で一括実行)
   │    - LLM (既定: codellama/CodeLlama-7b-hf) でファイル全体を1回推論
   │    - 関数ごとに切り出して再推論 (isolated_surprisal)
   │    - Tree-sitter で各トークンに行・AST 種別・ネスト深さ・関数 ID を付与
   ▼
out/<dataset>/result_<uid>.parquet          1行 = 1トークン
   │
   │  Phase 2: src/analysis/pipeline.py     (並列実行、閾値を引数で指定)
   │    - トークン表に surprisal_gap 列を追加
   │    - ファイル単位の指標 (PPL, LM-CC, LoC, CC, CogC, ...) を算出
   ▼
results/enriched/<dataset>/*.parquet         surprisal_gap 付きトークン表
results/summaries/analysis_summary{suffix}.csv   1行 = 1ファイル
   │
   │  Phase 3: src/analysis/experiments/, plotting/   (+ lm-cc の pass@1)
   ▼
results/plots/, results/experiments/, results/semantic_unit_*/ ...
```

Phase 1 だけが LLM (torch / transformers, GPU or Apple MPS) を必要とします。
Phase 2 以降は CPU のみで、コミット済みの `out/` から再現できます。

## ディレクトリ

| パス | 内容 |
|---|---|
| `src/paths.py` | **全パスの定義**。`data/`, `out/`, `results/*`, lm-cc の場所 (`LM_CC_ROOT`) |
| `src/collect_metrics.py` | Phase 1 CLI。下の4層を組み立てるだけ |
| `src/language/` | 言語アダプタ (Python / Java / C)。Tree-sitter パーサ、関数・文の判定 |
| `src/model/` | モデルアダプタ。`hf_causal_lm` (HuggingFace CausalLM) のみ。torch は遅延 import |
| `src/context/` | isolated 推論のウィンドウ切り出し戦略。`function_scope` のみ |
| `src/writer/` | 出力形式。`parquet` (既定) / `json` |
| `src/schema/records.py` | データ構造と**列名の定数** (`ParquetSchema`, `SummarySchema`) |
| `src/utils/` | ロギング、文字⇔バイト位置変換、IO |
| `src/analysis/pipeline.py` | Phase 2 のエントリポイント |
| `src/analysis/macro/` | ファイル単位の指標 (perplexity, lm_cc, lm_cc_density, loc, cyclomatic, cognitive) |
| `src/analysis/macro/lm_cc_helper/` | LM-CC の境界判定・ブロックツリー構築 (lm-cc からの移植) |
| `src/analysis/micro/` | トークン単位の指標 (surprisal gap, 関数先頭トークンの surprisal) |
| `src/analysis/scores.py` | **pass@1 スコアの読み込み** (`SCORE_FILES`, `load_scores`) |
| `src/analysis/stats/` | グループ化 Spearman 相関など (lm-cc の `scripts/utils` からの移植) |
| `src/analysis/experiments/` | 相関分析・閾値探索・semantic unit 分析など、論文用の分析スクリプト |
| `src/analysis/plotting/` | 散布図・閾値グラフ |
| `src/analysis/tools/` | データ欠落チェック、先行研究との一致検証などの補助スクリプト |
| `src/analysis/viewer_app.py` | Streamlit の定性分析ビューア |
| `src/equivalence/` | 等価変換の前後比較実験 (変換・動作確認・計測・比較・回答精度)。`docs/equivalence_experiment.md` |
| `configs/equivalence/` | 等価変換実験の設定 (TOML) |
| `scripts/` | 長時間のバッチ (Phase 1 一括実行、閾値ごとの相関実験) |
| `tests/` | pytest。モデル不要。コミット済みデータを使う回帰テストを含む |

### import の規約

`src/` を唯一の import ルートにしています (`from schema.records import ...`,
`from analysis.macro import lm_cc`, `import paths`)。
実行可能なスクリプトは先頭で `sys.path.insert(0, <src>)` しているので、
どのディレクトリからでも `python src/analysis/...py` で直接実行できます。
`from src.xxx` や `from macro import ...` のような書き方は使いません。

## Phase 1: トークン単位データ (`out/`)

1ファイル → 1 Parquet。列は `src/schema/records.py` の `ParquetSchema` が正です。

| 列 | 意味 |
|---|---|
| `idx`, `token_id`, `token_str` | トークン位置・ID・文字列 (CodeLlama なので `▁` = 空白, `<0x0A>` = 改行) |
| `line`, `column` | トークン開始位置 (1始まりの行、0始まりの**文字**列) |
| `ast_type`, `nesting_depth` | トークン内の最初の非空白文字にある Tree-sitter ノードの種別と、block 系祖先の数 |
| `function_id` | 含まれる最内関数名 (関数外は null) |
| `is_statement_start` | 文ノードがこのトークンの最初の非空白文字から始まるか |
| `is_function_start` | 関数定義の開始バイトがこのトークン内にあるか |
| `metric_surprisal` | ファイル全体を文脈にした `-ln p(token)` [nats] |
| `metric_entropy` | 予測分布のエントロピー [nats] |
| `metric_isolated_surprisal` | 関数単体を切り出して推論した surprisal (関数外は null) |
| `meta_*` | ファイル単位のメタデータを全行に複製 (`meta_file` は実行マシンの絶対パス) |

BOS トークンがあるモデルでは BOS を先頭に付けて推論するので、先頭トークンにも値が入ります。

`meta_collector_version` でどの版の Phase 1 で作られたかが分かります。
**コミット済みの `out/` は 1.0.0** で、`ast_type` / `nesting_depth` / `is_statement_start`
に既知の問題があります (`AGENTS.md` の「既知の注意点」参照)。

## Phase 2: ファイル単位の指標 (`results/summaries/`)

`pipeline.process_file` が1ファイルを処理します。surprisal が null の行は先に除外します。

| 列 (`SummarySchema`) | 算出方法 |
|---|---|
| `ppl` | `exp(mean(surprisal))` |
| `lm_cc` | lm-cc のアルゴリズム。エントロピー ≥ 閾値のトークンを含む行の前に境界を入れ、ブロックツリーを作って `0.2 * 深さ合計 + 0.8 * 分岐数` |
| `num_semantic_units` | 上の境界で区切られたユニット数 (境界数 + 1) |
| `lm_cc_density` | 関数内の文先頭トークンについて `(1 + nesting_depth) * entropy` を関数ごとに合計し平均 |
| `loc` | トークンがある最大行番号 |
| `cyclomatic_complexity` | Lizard。元ソースを `meta_file` から読み直す。そのままとトップレベルを関数で包んだ版の大きい方 |
| `cognitive_complexity` | `cognitive-complexity` パッケージ (Python のみ)。同上 |
| `avg_first_token_surprisal` | `is_function_start` トークンの surprisal 平均 |
| `avg_context_surprisal_gap` | `isolated_surprisal - surprisal` の平均 |
| `total_tokens`, `num_functions` | 行数、関数先頭トークン数 |

閾値と出力ファイル名の対応 (全トークンのエントロピー分布のパーセンタイル。
`experiments/calculate_entropy_thresholds.py` で算出):

| suffix | 閾値 [nats] | 主な利用箇所 |
|---|---|---|
| `_p67` | 0.6813 | pipeline の既定、`correlation_analysis.py` の既定 |
| `_p80` | 1.2515 | `semantic_unit_*`, `plot_analysis_scatter.py` |
| (なし) | 実行時の値 | `plot_distributions.py`, `plot_analysis_scatter_with_group.py`, `check_missing_data.py` |
| `_p05`〜`_p95` | `scripts/run_threshold_experiments.py` の表 | 閾値実験 |

## Phase 3: 正答率との相関

pass@1 は lm-cc リポジトリの `results/` にあり、`analysis/scores.py` の
`SCORE_FILES` で dataset 名と対応付けています。lm-cc の場所は既定で
このリポジトリと同じ親ディレクトリの `lm-cc/`、別の場所なら環境変数 `LM_CC_ROOT` で指定します。

| dataset (summary の `dataset` 列) | lm-cc のスコアファイル |
|---|---|
| `humaneval` | `humaneval-ier/results_score.json` |
| `humaneval_simplified-top60` | `humaneval-ier-simplified/results_score_simplified.json` |
| `xcodeeval_apr` | `xcodeeval/apr/python_test_filtered_results.json` |
| `xcodeeval_simplified-top50_apr` | `xcodeeval/apr-simplified/python_test_filtered_results.json` |
| `xcodeeval_code_translation` | `xcodeeval/code_translation/python2c_test_filtered_results.json` |
| `xcodeeval_simplified-top50_code_translation` | `xcodeeval/code_translation-simplified/python2c_test_filtered_results.json` |

相関は `stats/correlation.get_grouped_partial_corr` (lm-cc と同じ手法) で、
指標でソートして `min_cnt` 件ずつのグループに分け、グループ平均どうしの Spearman 相関を取ります。
`min_cnt` は件数の 1/20〜1/8 を総当たりし、有効グループ数が 9〜11 のうち |r| 最大のものを採用します。

## 拡張ポイント

- 新しい言語: `src/language/` に `LanguageAdapter` を実装し `language/__init__.py` で `register_language`
- 新しいモデル: `src/model/` に `ModelAdapter` を実装し `register_model("kind", ".module:Class")`
- 新しい isolated 戦略: `src/context/` に `ContextStrategy` を実装し `register_strategy`
- 新しいファイル単位指標: `src/analysis/macro/<name>.py` に `calculate(df_clean)` を作り、
  `pipeline.process_file` と `SummarySchema` に列を追加
- 新しい等価変換: `src/equivalence/transforms/` に `Transformation` を実装し `register_transformation`
- 新しいデータセット: `data/<name>/` に置いて `scripts/batch_runner.py` の `INPUT_DIRS` に追加。
  正答率があるなら `analysis/scores.py` の `SCORE_FILES` に登録
