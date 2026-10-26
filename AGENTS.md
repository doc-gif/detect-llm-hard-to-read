# AGENTS.md

AI エージェント (Claude Code, Codex, Cursor など) 向けの作業ガイド。人間向けの概要は
`README.md`、設計の詳細は `docs/architecture.md` を参照。
`CLAUDE.md` はこのファイルを読み込むだけにしているので、規約の追加・変更はこのファイルに書く。

## このリポジトリ

修士研究のコード。LLM のトークン予測 (surprisal / entropy) からコードの「LLM にとっての
読みにくさ」を測り、先行研究 LM-CC (別リポジトリ `lm-cc`) の指標と比較しつつ、LLM の正答率
(pass@1) との相関を調べる。ユーザーは日本語で書くので、返答・コメント・ドキュメントは日本語。

処理は3段階:
1. **Phase 1** `src/collect_metrics.py`: ソース → トークン単位 Parquet (`out/`)。LLM が必要
2. **Phase 2** `src/analysis/pipeline.py`: `out/` → ファイル単位 summary CSV (`results/summaries/`)
3. **Phase 3** `src/analysis/experiments/`, `plotting/`: summary + lm-cc の pass@1 → 相関・図

## コマンド

```bash
pip install -r requirements.txt          # Phase 1 も回すなら torch/transformers も入る
python -m pytest                          # テスト (モデル不要、数秒)

# Phase 2 (CPU、1500ファイルで数十秒)。出力先を変えるなら --results-dir
python src/analysis/pipeline.py --threshold 0.6813 --suffix _p67

# Phase 3 の例
python src/analysis/experiments/correlation_analysis.py results/summaries/analysis_summary_p67.csv
python scripts/run_threshold_experiments.py

# Phase 1 (要 GPU / Apple MPS と CodeLlama-7b。ユーザーの Mac で実行するもの)
python src/collect_metrics.py --model codellama/CodeLlama-7b-hf --source data/examples/example1.py --output /tmp/x.parquet
python scripts/batch_runner.py           # INPUT_DIRS / DEVICE は先頭の設定エリアで編集

# 等価変換の前後比較 (docs/equivalence_experiment.md)。measure 段階だけがモデルを使う
python scripts/equivalence_experiment.py all --config configs/equivalence/if_else_swap_humaneval_sample.toml
python scripts/equivalence_experiment.py all --config configs/equivalence/if_else_swap_humaneval_sample_dummy.toml  # ダミーモデルで通す
python scripts/equivalence_experiment.py scan --dataset all --transform if_else_swap   # 候補数と理由だけ (ファイルを書かない)
python scripts/equivalence_experiment.py all --config configs/equivalence/template.toml --dataset all  # 全データセット
```

lm-cc は既定でこのリポジトリと同じ親ディレクトリの `lm-cc/` を参照する。別の場所なら
`LM_CC_ROOT=/path/to/lm-cc` を付ける。無いと pass@1 が読めず相関系スクリプトは空振りする。

## コードの規約

- **import ルートは `src/` だけ**。`from schema.records import ...`, `from analysis.macro import lm_cc`,
  `import paths`。`from src....` や `from macro import ...` は書かない。
  実行スクリプトは先頭で `sys.path.insert(0, str(Path(__file__).resolve().parents[N]))` して
  `src/` を通している (N はファイルの深さに合わせる)。新しいスクリプトも同じ形にする。
- **パスは `src/paths.py` から取る**。`Path(__file__).parent.parent...` や絶対パスを書かない。
- **pass@1 は `analysis.scores.load_scores(dataset)` で読む**。スクリプトごとに `SCORE_FILES` や
  `load_scores` をコピーしない。対象データセットは各スクリプトの `TARGET_DATASETS` で絞る。
- **列名は `schema.records.ParquetSchema` / `SummarySchema` の定数を使う**。文字列直書きを増やさない。
- 分析スクリプトは「先頭に設定エリア (定数) → 関数 → `main()`」の形。既存の書き方
  (日本語コメント、絵文字入りのログ) に合わせる。
- `analysis/macro/lm_cc_helper/` と `analysis/stats/` は lm-cc からの移植。先行研究と数値を
  合わせるためのコードなので、挙動を変えるときは lm-cc 側の実装と比較してから。

## 変更したら確認すること

- `python -m pytest` が通る。`tests/test_pipeline_regression.py` はコミット済みの `out/` と
  `results/summaries/analysis_summary_p67.csv` を突き合わせるので、Phase 2 の数値が変わると落ちる。
  意図した変更なら、その理由をユーザーに説明してから CSV を再生成する。
- Phase 2 全体の一致を見たいときは、出力先を一時ディレクトリにして回し、既存 CSV と比較する:
  `python src/analysis/pipeline.py --results-dir /tmp/r` → `/tmp/r/summaries/analysis_summary_p67.csv`
  (`cyclomatic_complexity` だけは Lizard のバージョン差で数件ずれることがある)。
- `results/` と `out/` はコミットされた研究成果物。スクリプトを試すときに上書きしない
  (上書きしたら `git checkout -- results/` で戻す)。

- 等価変換の実験 (`src/equivalence/`) は Phase 1 / Phase 2 の関数 (`collect_metrics.collect`,
  `analysis.macro.*`, `get_code_with_boundaries`) を呼んで使う。SU や LOC の定義を独自に書き直さない
  (`tests/test_equivalence_compare.py` で summary CSV と同じ値になることを確認している)。
  新しい変換は `src/equivalence/transforms/` に追加する (`scan` で候補数を確認できる)。
  measure は `results/equivalence/_cache/measure/` の計測結果を、モデル・dtype・コードの中身などが同じときだけ
  再利用する。キーに入る条件を増やすときは `measure.CACHE_CONFIG_KEYS` に足す。結果は `results/equivalence/<name>/` に出し、
  条件を変えるときは別の `experiment.name` にする。
- `model` の `dummy` は動作確認専用 (エントロピーに意味は無い)。研究の計測には使わない。

## 既知の注意点 (データ)

- **`out/` は collector 1.0.0 で作られている** (`meta_collector_version`)。1.0.0 には次の問題があり、
  1.1.0 で修正済みだが `out/` は再生成していない (再生成にはユーザーの Mac で Phase 1 を回す必要がある):
  - `is_statement_start` / `ast_type` / `nesting_depth` を、SentencePiece トークン先頭の空白位置で
    引いていた。そのため `is_statement_start` は「文の先頭」ではなく「先頭の空白が文ノードの内側にある
    トークン」(例: `if x` の `▁x`) を指しており、代入文はほぼ拾えていない。
    → これを使う **`lm_cc_density` は 1.0.0 のデータでは信頼できない**。`lm_cc` / `ppl` /
    `num_semantic_units` / `loc` はトークン文字列・エントロピー・行番号だけを使うので影響しない。
  - `function_id` も先頭空白の位置で判定していたため、インデントされた `▁def` トークンが関数外 (null)
    になっていた (関数先頭トークン 2803 件中 485 件)。`num_functions` / `avg_first_token_surprisal` は
    `function_id` を使わないので影響しない。
  - Tree-sitter に文字単位の列を渡していたため、非 ASCII 文字を含む行 (15ファイル) で AST 情報がずれていた。
- `meta_file` は Phase 1 実行マシンの絶対パス (`/Users/...`)。`paths.resolve_data_path` が
  `data/` 以降を付け替えて読むので、別マシンでも cyclomatic / cognitive complexity は計算できる。
- HumanEval のスコアファイルは 1 問につき `HumanEval_N`, `HumanEval_N__0`, `HumanEval_N__1` の3キーがある。
  先行研究に合わせて接尾辞なしのキーだけを使う (`scores.parse_scores`)。以前は最後に現れたキーで
  上書きしていたため 162 問中 17 問のスコアが先行研究と違っていた。
  **コミット済みの `results/experiments/threshold_correlation_results.csv` や `results/plots/` の
  HumanEval の数値は旧仕様のまま**。xcodeeval 系は影響なし。
- **HumanEval の `data/humaneval/<ID>.py` は、先行研究の pass@1 (接尾辞なしのケース) のプロンプトに入った
  lm-cc `dataset/humaneval/<ID>/main.py` と一致しないものがある** (162 問中 83 問。`__0`/`__1` の `main.py`
  と同じで、空行・空白が違う。HumanEval_1, 105, 124, 150 は AST も違う)。また HumanEval_10, 33 は
  計測用ソースの実行結果が `output.txt` と一致しない。詳細は `docs/equivalence_experiment.md`。
- `results/block_trees/` は古い Phase 1 出力 (BOS 修正前) から作られたもので、現在の `out/` とは
  エントロピーが一致しない。必要なら `experiments/generate_block_tree.py` で作り直す。
- `analysis/stats/metrics.py` の `get_code_cc` などは `radon` / `black` の CLI を呼ぶ
  (requirements には入れていない)。現在どのスクリプトからも呼ばれていない。
- `japanize_matplotlib` は Python 3.12+ で入らないことが多いので任意 import にしている。
