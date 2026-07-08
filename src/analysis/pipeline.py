import logging
import sys
from pathlib import Path
import pandas as pd
import traceback

from macro import perplexity, lm_cc, lm_cc_density, loc
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


def process_file(parquet_path: Path, base_in_dir: Path) -> dict:
    df = pd.read_parquet(parquet_path)

    # ==========================================
    # 1. データクレンジング (ノイズ除去)
    # ==========================================
    # 予測対象外のトークン（BOSなど）を除外し、計算のベースとなる綺麗なデータを作成
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
    cal_lm_cc, semantic_unit_count = lm_cc.calculate(df_clean)
    cal_lm_cc_density = lm_cc_density.calculate(df_clean)
    cal_loc = loc.calculate(df_clean)

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

    # ギャップ列などが追加された「拡張版」のデータフレームを保存
    df_clean.to_parquet(out_parquet_path)

    uid = parquet_path.stem.replace("result_", "")

    # スキーマ定義（SCol）に従ってサマリー辞書を構築
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
    }
    return summary


def run_pipeline():
    if not INPUT_DIR.exists():
        logging.error(f"入力ディレクトリが見つかりません: {INPUT_DIR}")
        sys.exit(1)

    ENRICHED_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

    parquet_files = list(INPUT_DIR.rglob("*.parquet"))
    total_files = len(parquet_files)

    if total_files == 0:
        logging.error("❌ 処理対象のParquetファイルが見つかりません。")
        sys.exit(1)

    logging.info(f"🚀 合計 {total_files} 件のParquetファイルを分析します...")

    summary_list = []
    success_count = 0
    error_count = 0

    for i, parquet_path in enumerate(parquet_files, 1):
        progress = f"[{i}/{total_files}]"
        logging.info(f"{progress} 分析中: {parquet_path.name}")

        try:
            summary = process_file(parquet_path, INPUT_DIR)
            summary_list.append(summary)
            success_count += 1
        except Exception as e:
            logging.error(f"{progress} ❌ エラー ({parquet_path.name}): {e}")
            logging.error(traceback.format_exc())
            error_count += 1

    if summary_list:
        summary_df = pd.DataFrame(summary_list)
        # SColの定義順にカラムを並び替える（オプションですが綺麗に整頓されます）
        cols = [getattr(SCol, k) for k in dir(SCol) if not k.startswith("_") and isinstance(getattr(SCol, k), str)]
        summary_df = summary_df[[c for c in cols if c in summary_df.columns]]

        summary_csv_path = SUMMARIES_DIR / "analysis_summary.csv"
        summary_df.to_csv(summary_csv_path, index=False)
        logging.info(f"💾 サマリーCSVを保存しました: {summary_csv_path}")

    logging.info("=" * 40)
    logging.info("🎉 分析パイプラインが終了しました。")
    logging.info(f"  成功: {success_count} 件")
    logging.info(f"  エラー: {error_count} 件")
    logging.info("=" * 40)


if __name__ == "__main__":
    run_pipeline()