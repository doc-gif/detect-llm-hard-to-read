# src/analysis/pipeline.py
import logging
import sys
from pathlib import Path
import pandas as pd
import traceback
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

from macro import perplexity, lm_cc, lm_cc_density, loc, cyclomatic_complexity, cognitive_complexity
from micro import context_surprisal_gap, first_token_suprisal

from schema.records import ParquetSchema as PCol
from schema.records import SummarySchema as SCol

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# --- 設定エリア ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_DIR = PROJECT_ROOT / "out"
OUTPUT_DIR = PROJECT_ROOT / "results"

ENRICHED_DIR = OUTPUT_DIR / "enriched"
SUMMARIES_DIR = OUTPUT_DIR / "summaries"


def process_file(parquet_path: Path, base_in_dir: Path, threshold: float) -> dict:
    """1ファイルの処理（並列ワーカーで実行される関数）"""
    df = pd.read_parquet(parquet_path)

    # ==========================================
    # 1. データクレンジング (ノイズ除去)
    # ==========================================
    if PCol.METRIC_SURPRISAL in df.columns:
        df_clean = df[df[PCol.METRIC_SURPRISAL].notnull()].copy()
    else:
        df_clean = df.copy()

    # ==========================================
    # 2. データ成形 (Transformation)
    # ==========================================
    df_clean = context_surprisal_gap.add_contextual_surprisal_gap(df_clean)
    first_tokens_df = first_token_suprisal.extract_first_token_surprisal(df_clean)

    # ==========================================
    # 3. マクロ指標算出 (Macro Metrics Calculation)
    # ==========================================
    cal_perplexity = perplexity.calculate(df_clean)
    cal_lm_cc, semantic_unit_count = lm_cc.calculate(df_clean, threshold=threshold)
    cal_lm_cc_density = lm_cc_density.calculate(df_clean)
    cal_loc = loc.calculate(df_clean)

    # 💡 Cyclomatic Complexity / Cognitive Complexity は、Phase 1 の
    # ParquetWriter が全行に埋め込んでいる meta_file（元ソースファイルの
    # 絶対パス）から元ファイルをそのまま読み込んで静的解析する。
    # df / df_clean どちらでも meta_file の値は同じなので、ここでは df_clean
    # をそのまま渡す。
    cal_cyclomatic_complexity = cyclomatic_complexity.calculate(df_clean)
    cal_cognitive_complexity = cognitive_complexity.calculate(df_clean)

    # ==========================================
    # 4. ミクロ指標算出 (Micro Metrics Aggregation)
    # ==========================================
    avg_context_surprisal_gap = context_surprisal_gap.calculate_avg(df_clean)
    avg_first_token_surprisal = first_token_suprisal.calculate_avg(first_tokens_df)

    # ==========================================
    # 5. 保存と結果の返却
    # ==========================================
    relative_path = parquet_path.relative_to(base_in_dir)
    out_parquet_path = ENRICHED_DIR / relative_path
    out_parquet_path.parent.mkdir(parents=True, exist_ok=True)

    df_clean.to_parquet(out_parquet_path)

    uid = parquet_path.stem.replace("result_", "")

    summary = {
        SCol.UID: uid,
        SCol.DATASET: relative_path.parent.name,
        SCol.PPL: cal_perplexity,
        SCol.LM_CC: cal_lm_cc,
        SCol.LM_CC_DENSITY: cal_lm_cc_density,
        SCol.LOC: cal_loc,
        SCol.AVG_FIRST_TOKEN_SURPRISAL: avg_first_token_surprisal,
        SCol.AVG_CONTEXT_SURPRISAL_GAP: avg_context_surprisal_gap,
        SCol.TOTAL_TOKENS: len(df_clean),
        SCol.NUM_FUNCTIONS: len(first_tokens_df) if not first_tokens_df.empty else 0,
        SCol.NUM_SEMANTIC_UNITS: semantic_unit_count,
        SCol.CYCLOMATIC_COMPLEXITY: cal_cyclomatic_complexity,
        SCol.COGNITIVE_COMPLEXITY: cal_cognitive_complexity,
    }
    return summary


def run_pipeline(threshold: float = 0.6813, suffix: str = "_p67"):
    if not INPUT_DIR.exists():
        logging.error(f"入力ディレクトリが見つかりません: {INPUT_DIR}")
        sys.exit(1)

    ENRICHED_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

    parquet_files = list(INPUT_DIR.rglob("result_*.parquet"))
    total_files = len(parquet_files)

    if total_files == 0:
        logging.error("❌ 処理対象のParquetファイルが見つかりません。")
        sys.exit(1)

    # 使用するCPUコア数を決定（OSを重くしないよう最大コア数から1つ残す）
    max_workers = max(1, multiprocessing.cpu_count() - 1)
    logging.info(f"🚀 合計 {total_files} 件のファイルを並列分析します (使用コア数: {max_workers})...")

    summary_list = []
    success_count = 0
    error_count = 0

    # 💡 ProcessPoolExecutorによるマルチプロセス処理
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # タスクをキューに登録
        future_to_path = {executor.submit(process_file, p, INPUT_DIR, threshold): p for p in parquet_files}

        # 完了したものから順次結果を受け取る
        for i, future in enumerate(as_completed(future_to_path), 1):
            parquet_path = future_to_path[future]
            try:
                summary = future.result()
                summary_list.append(summary)
                success_count += 1
            except Exception as e:
                # エラー時のみ即座に出力
                logging.error(f"\n❌ エラー ({parquet_path.name}): {e}")
                logging.error(traceback.format_exc())
                error_count += 1

            # 💡 ログ出力の頻度を削減 (50件ごと、または最後の1件にのみ出力)
            if i % 50 == 0 or i == total_files:
                logging.info(f"進捗: [{i}/{total_files}] 完了 (成功: {success_count} / エラー: {error_count})")

    if summary_list:
        summary_df = pd.DataFrame(summary_list)
        cols = [getattr(SCol, k) for k in dir(SCol) if not k.startswith("_") and isinstance(getattr(SCol, k), str)]
        summary_df = summary_df[[c for c in cols if c in summary_df.columns]]

        if SCol.DATASET in summary_df.columns and SCol.UID in summary_df.columns:
            try:
                summary_df['temp_sort_uid'] = pd.to_numeric(summary_df[SCol.UID].str.extract(r'(\d+)')[0])
                summary_df = summary_df.sort_values(by=[SCol.DATASET, 'temp_sort_uid']).drop(columns=['temp_sort_uid'])
            except:
                summary_df = summary_df.sort_values(by=[SCol.DATASET, SCol.UID])
            summary_df = summary_df.reset_index(drop=True)

        summary_csv_path = SUMMARIES_DIR / f"analysis_summary{suffix}.csv"
        summary_df.to_csv(summary_csv_path, index=False)
        logging.info(f"💾 サマリーCSVを保存しました: {summary_csv_path}")

    logging.info("=" * 40)
    logging.info("🎉 分析パイプラインが終了しました。")
    logging.info(f"  成功: {success_count} 件")
    logging.info(f"  エラー: {error_count} 件")
    logging.info("=" * 40)


if __name__ == "__main__":
    run_pipeline()