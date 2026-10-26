# detect-llm-hard-to-read

LLM 自身のトークン予測の不確かさ (surprisal / entropy) から、「LLM にとって読みにくいコード」を
定量化する研究用コードです。先行研究 [LM-CC](https://github.com/doc-gif/lm-cc) の指標を再実装・拡張し、
LLM の正答率 (pass@1) との相関を調べます。

- 設計・データ形式・指標の定義: [docs/architecture.md](docs/architecture.md)
- AI エージェント向けの作業ガイド (規約・既知の注意点): [AGENTS.md](AGENTS.md) (Claude Code は `CLAUDE.md` 経由で同じ内容を読み込みます)

## セットアップ

Python 3.11 以上 (3.13 で動作確認)。

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

pass@1 スコアは lm-cc リポジトリの `results/` を参照します。このリポジトリと同じ親ディレクトリに
置くか、環境変数で場所を指定してください。

```
PycharmProjects/
├── detect-llm-hard-to-read/   ← このリポジトリ
└── lm-cc/                     ← 既定ではここを見る (別の場所なら LM_CC_ROOT=/path/to/lm-cc)
```

## 使い方

### Phase 1: トークン単位データの収集 (LLM を使う)

```bash
# 1ファイル
python src/collect_metrics.py --model codellama/CodeLlama-7b-hf \
    --source data/examples/example1.py --output out/examples/result_example1.parquet \
    --device mps --dtype float16

# data/ 配下を一括 (対象ディレクトリやデバイスはスクリプト先頭の設定エリアで指定)
python scripts/batch_runner.py
```

出力: `out/<dataset>/result_<uid>.parquet` (1行 = 1トークン)。既に出力があるファイルはスキップします。

### Phase 2: ファイル単位の指標 (CPU のみ)

```bash
python src/analysis/pipeline.py                                  # 既定: 閾値 0.6813 (p67)
python src/analysis/pipeline.py --threshold 1.2515 --suffix _p80
```

出力: `results/summaries/analysis_summary{suffix}.csv`, `results/enriched/`

### Phase 3: 分析・作図

| やりたいこと | スクリプト |
|---|---|
| 各指標と pass@1 の相関表 | `src/analysis/experiments/correlation_analysis.py [summary.csv]` |
| 閾値ごとの相関をまとめる | `scripts/run_threshold_experiments.py` → `src/analysis/plotting/plot_threshold_vs_correlation.py` |
| エントロピーのパーセンタイル閾値を出す | `src/analysis/experiments/calculate_entropy_thresholds.py` |
| semantic unit 数と pass@1 の関係 | `src/analysis/experiments/semantic_unit_threshold_analysis.py`, `semantic_unit_model_comparison.py` |
| 散布図 | `src/analysis/plotting/plot_analysis_scatter.py`, `plot_distributions.py`, `plot_analysis_scatter_with_group.py` |
| LM-CC ブロックツリーの JSON を出す | `src/analysis/experiments/generate_block_tree.py` |
| 推論漏れの確認 / 先行研究との一致検証 | `src/analysis/tools/check_missing_data.py`, `verify_token_entropies.py`, `analysis_token_differences.py` |
| 抽出グループのコードを眺める | `streamlit run src/analysis/viewer_app.py` |

どのスクリプトもリポジトリ内のどこからでも実行できます (パスは `src/paths.py` で一元管理)。

## テスト

```bash
python -m pytest
```

モデルは不要です。コミット済みの `out/` と `results/summaries/analysis_summary_p67.csv` を使って、
Phase 2 の数値が変わっていないことも確認します。

## データセット

| `data/` | 件数 | 内容 |
|---|---|---|
| `humaneval` | 162 | HumanEval (実行推論タスク) |
| `humaneval_simplified`, `humaneval_simplified-top60` | 63, 60 | LLM で簡略化したもの / LM-CC 上位 60% |
| `xcodeeval/apr` | 271 | xCodeEval プログラム修正 |
| `xcodeeval/code_translation` | 536 | xCodeEval コード翻訳 (Python → C) |
| `xcodeeval_simplified*/…` | | 上記の簡略化版 |
| `examples` | 1 | 動作確認用 |

`out/` と `results/` のディレクトリ名は `data/` からの相対パスを `_` で連結したもの
(例: `data/xcodeeval/apr` → `out/xcodeeval_apr`) で、summary CSV の `dataset` 列と一致します。
