import logging
import sys
from pathlib import Path
import pandas as pd
import traceback

# 💡 あなたの指定された通りの正しい呼び出し形式に完全対応
from macro import perplexity, lm_cc, lm_cc_density
from micro import context_surprisal_gap, first_token_suprisal

# --- ログの設定 ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# --- 設定エリア ---
INPUT_DIR = Path("../out").resolve()
OUTPUT_DIR = Path("../results").resolve()

ENRICHED_DIR = OUTPUT_DIR / "enriched"
SUMMARIES_DIR = OUTPUT_DIR / "summaries"


def process_file(parquet_path: Path, base_in_dir: Path) -> dict:
    """
    1つのParquetファイルを読み込み、各指標を計算して拡張ファイルを保存し、サマリーを返す。
    """
    df = pd.read_parquet(parquet_path)

    # --- 1. データクレンジング ---
    if 'surprisal' in df.columns:
        df_clean = df[df['surprisal'].notnull()].copy()
    else:
        df_clean = df.copy()

    # --- 2. ミクロ指標の計算 (トークンレベルの拡張) ---
    if 'isolated_surprisal' in df_clean.columns:
        # 💡 正しいモジュール名・関数名で呼び出し
        df_clean = context_surprisal_gap.add_contextual_surprisal_gap(df_clean)

    # --- 3. マクロ指標の計算 (ファイル全体) ---
    ppl = perplexity.calculate(df_clean)
    # 💡 正しいモジュール名・関数名で呼び出し
    macro_lmcc = lm_cc.calculate_macro_lmcc(df_clean)
    # 💡 正しいモジュール名・関数名で呼び出し (マクロ指標)
    avg_lmcc_density = lm_cc_density.calculate_lmcc_density_per_function(df_clean)

    # --- 4. 構造レベル(関数)指標の集計 ---
    # 💡 正しいモジュール名・関数名で呼び出し
    first_tokens_df = first_token_suprisal.extract_first_token_surprisal(df_clean)

    # CSVサマリー用に、ファイル内のすべての関数における第一トークン・サプライザルの平均を算出
    avg_first_token = first_tokens_df['first_token_surprisal'].mean() if not first_tokens_df.empty else None
    avg_gap = df_clean['surprisal_gap'].mean() if 'surprisal_gap' in df_clean.columns else None

    # --- 5. 拡張Parquetの保存 ---
    relative_path = parquet_path.relative_to(base_in_dir)
    out_parquet_path = ENRICHED_DIR / relative_path
    out_parquet_path.parent.mkdir(parents=True, exist_ok=True)

    df_clean.to_parquet(out_parquet_path)

    # --- 6. サマリー辞書の作成 ---
    uid = parquet_path.stem.replace("result_", "")  # result_01479... -> 01479...

    summary = {
        "uid": uid,
        "dataset": relative_path.parent.name,  # (例: apr)
        "ppl": ppl,
        "macro_lmcc": macro_lmcc,
        "avg_lmcc_density": avg_lmcc_density,
        "avg_first_token_surprisal": avg_first_token,
        "avg_surprisal_gap": avg_gap,
        "total_tokens": len(df_clean),
        "num_functions": len(first_tokens_df) if not first_tokens_df.empty else 0
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
