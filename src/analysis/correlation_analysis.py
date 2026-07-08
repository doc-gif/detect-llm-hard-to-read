import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from scipy import stats
import warnings

from schema.records import SummarySchema
from src.analysis.util.correlation import get_grouped_partial_corr

logging.basicConfig(level=logging.INFO, format="%(message)s")
warnings.filterwarnings("ignore", message="The covariance matrix is rank-deficient")

# ==========================================
# ⚙️ 設定エリア
# ==========================================
PROJECTS_DIR = Path(__file__).resolve().parent.parent.parent.parent
SUMMARY_CSV_PATH = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "summaries" / "analysis_summary.csv"

SCORE_FILES = {
    "humaneval": {"path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier" / "results_score.json",
                  "format": "simple"},
    # "humaneval_simplified-top60": {"path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier-simplified" / "results_score_simplified.json", "format": "simple"},
    "xcodeeval_apr": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr" / "python_test_filtered_results.json",
        "format": "nested"},
    # "xcodeeval_simplified-top50_apr": {"path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr-simplified" / "python_test_filtered_results.json", "format": "nested"},
    "xcodeeval_code_translation": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation" / "python2c_test_filtered_results.json",
        "format": "nested"},
    # "xcodeeval_simplified-top50_code_translation": {"path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation-simplified" / "python2c_test_filtered_results.json", "format": "nested"}
}

METRICS_TO_ANALYZE = [
    SummarySchema.LM_CC,
    SummarySchema.NUM_SEMANTIC_UNITS,
    # SummarySchema.PPL,
    # SummarySchema.LM_CC_DENSITY,
]
CONTROL_VARIABLE = SummarySchema.LOC


# ==========================================
# 共通関数
# ==========================================
def get_significance_marker(p_val: float) -> str:
    """p値から論文用の有意水準マーカーを返す"""
    if p_val is None or np.isnan(p_val): return ""
    if p_val < 0.001:
        return "0.001 "
    elif p_val < 0.01:
        return "<0.01 "
    elif p_val < 0.05:
        return "<0.05 "
    else:
        return "n.s."


def load_scores(dataset_name: str, config: dict) -> dict:
    path = Path(config["path"])
    if not path.exists(): return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    scores = {}
    if config["format"] == "simple":
        for k, v in data.items(): scores[k.split("__")[0]] = v
    elif config["format"] == "nested":
        for k, v in data.items(): scores[k] = v.get("pass@1", 0.0)
    return scores


# ==========================================
# メイン処理
# ==========================================
def main():
    df_summary = pd.read_csv(SUMMARY_CSV_PATH)
    datasets = df_summary['dataset'].unique()

    for ds in datasets:
        if ds not in SCORE_FILES: continue
        print(f"\n{'=' * 70}\n📊 データセット: {ds}\n{'=' * 70}")

        scores_dict = load_scores(ds, SCORE_FILES[ds])
        df_ds = df_summary.loc[df_summary['dataset'] == ds].copy()
        df_ds['score'] = df_ds['uid'].map(scores_dict)

        df_ds = df_ds.dropna(subset=['score', CONTROL_VARIABLE])
        print(f"  -> {len(df_ds)} 件のデータで分析を実行します。")

        for metric in METRICS_TO_ANALYZE:
            if metric not in df_ds.columns: continue
            df_target = df_ds.dropna(subset=[metric, 'score', CONTROL_VARIABLE]).copy()
            if len(df_target) < 10: continue

            # データ配列の抽出
            score_arr = df_target['score'].values
            metric_arr = df_target[metric].values
            loc_arr = df_target[CONTROL_VARIABLE].values

            # 💡 先行研究の関数を呼び出して最適な偏相関とゼロ次相関を計算
            partial_corr, best_min_cnt_p = get_grouped_partial_corr(score_arr, metric_arr, loc_arr)
            zero_corr, best_min_cnt_z = get_grouped_partial_corr(score_arr, metric_arr, None)

            print(f"\n  🔹 指標: {metric}")

            # 偏相関の出力
            if partial_corr and partial_corr.get("partial_correlation"):
                r_val = partial_corr["partial_correlation"].get("spearman-r")
                p_val = partial_corr["partial_correlation"].get("spearman-pval")
                bins = partial_corr.get("valid_groups", "N/A")

                if r_val is not None and not np.isnan(r_val):
                    sig = get_significance_marker(p_val)
                    print(
                        f"     [偏相関]   r = {r_val:>7.4f}, p = {p_val:.4f} ({sig:^4}) | Bins: {bins:>2}, min_cnt: {best_min_cnt_p:>2}, Control: {CONTROL_VARIABLE}")
                else:
                    print(f"     [偏相関]   計算不可")
            else:
                print(f"     [偏相関]   計算不可")

            # ゼロ次相関の出力
            if zero_corr and zero_corr.get("partial_correlation"):
                r_val = zero_corr["partial_correlation"].get("spearman-r")
                p_val = zero_corr["partial_correlation"].get("spearman-pval")
                bins = zero_corr.get("valid_groups", "N/A")

                if r_val is not None and not np.isnan(r_val):
                    sig = get_significance_marker(p_val)
                    print(
                        f"     [ゼロ次相関] r = {r_val:>7.4f}, p = {p_val:.4f} ({sig:^4}) | Bins: {bins:>2}, min_cnt: {best_min_cnt_z:>2}")
                else:
                    print(f"     [ゼロ次相関] 計算不可")


if __name__ == "__main__":
    main()