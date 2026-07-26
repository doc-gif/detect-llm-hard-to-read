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
SUMMARY_CSV_PATH = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "summaries" / "analysis_summary_p67.csv"

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
    SummarySchema.CYCLOMATIC_COMPLEXITY,
    SummarySchema.COGNITIVE_COMPLEXITY,
    SummarySchema.LOC
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


def run_analysis(csv_path: Path) -> list:
    df_summary = pd.read_csv(csv_path)
    datasets = df_summary['dataset'].unique()

    results_list = []  # 💡 結果を格納するリスト

    for ds in datasets:
        if ds not in SCORE_FILES: continue
        scores_dict = load_scores(ds, SCORE_FILES[ds])
        df_ds = df_summary.loc[df_summary['dataset'] == ds].copy()
        df_ds['score'] = df_ds['uid'].map(scores_dict)
        df_ds = df_ds.dropna(subset=['score', CONTROL_VARIABLE])

        for metric in METRICS_TO_ANALYZE:
            if metric not in df_ds.columns: continue
            df_target = df_ds.dropna(subset=[metric, 'score', CONTROL_VARIABLE]).copy()
            if len(df_target) < 10: continue

            df_target = df_target.sort_values(by=[CONTROL_VARIABLE, metric, 'uid']).reset_index(drop=True)

            score_arr = df_target['score'].values
            metric_arr = df_target[metric].values
            # loc_arr = df_target[CONTROL_VARIABLE].values
            #
            # partial_corr, best_min_cnt_p = get_grouped_partial_corr(score_arr, metric_arr, loc_arr)
            zero_corr, best_min_cnt_z = get_grouped_partial_corr(score_arr, metric_arr, None)

            # # 偏相関の記録
            # if partial_corr and partial_corr.get("partial_correlation"):
            #     r_val = partial_corr["partial_correlation"].get("spearman-r")
            #     p_val = partial_corr["partial_correlation"].get("spearman-pval")
            #     bins = partial_corr.get("valid_groups", "N/A")
            #     if r_val is not None and not np.isnan(r_val):
            #         results_list.append({
            #             "Dataset": ds, "Target": "Score", "Metric": metric, "Type": "Partial",
            #             "r": r_val, "p_value": p_val, "Bins": bins, "Min_Cnt": best_min_cnt_p,
            #             "Control": CONTROL_VARIABLE
            #         })

            # ゼロ次相関の記録
            if zero_corr and zero_corr.get("partial_correlation"):
                r_val = zero_corr["partial_correlation"].get("spearman-r")
                p_val = zero_corr["partial_correlation"].get("spearman-pval")
                bins = zero_corr.get("valid_groups", "N/A")
                if r_val is not None and not np.isnan(r_val):
                    results_list.append({
                        "Dataset": ds, "Target": "Score", "Metric": metric, "Type": "Zero-Order",
                        "r": r_val, "p_value": p_val, "Bins": bins, "Min_Cnt": best_min_cnt_z, "Control": "None"
                    })

        # メトリクス間相関 (ゼロ次相関のみ)
        metric1 = SummarySchema.LM_CC
        metric2 = SummarySchema.NUM_SEMANTIC_UNITS
        if metric1 in df_ds.columns and metric2 in df_ds.columns:
            df_metric_corr = df_ds.dropna(subset=[metric1, metric2]).copy()
            if len(df_metric_corr) >= 10:
                df_metric_corr = df_metric_corr.sort_values(by=[metric1, metric2, 'uid']).reset_index(drop=True)
                r_val, p_val = stats.spearmanr(df_metric_corr[metric1], df_metric_corr[metric2])
                if r_val is not None and not np.isnan(r_val):
                    results_list.append({
                        "Dataset": ds, "Target": metric1, "Metric": metric2, "Type": "Zero-Order",
                        "r": r_val, "p_value": p_val, "Bins": "N/A", "Min_Cnt": "N/A", "Control": "None"
                    })

    return results_list


# ==========================================
# 実行と結果出力
# ==========================================
if __name__ == "__main__":
    import sys

    # 💡 コマンドライン引数で別のCSVパスが指定された場合はそちらを優先する
    target_csv = Path(sys.argv[1]) if len(sys.argv) > 1 else SUMMARY_CSV_PATH

    logging.info(f"📊 解析対象ファイル: {target_csv}")
    if not target_csv.exists():
        logging.error(f"❌ 指定されたファイルが見つかりません: {target_csv}")
        sys.exit(1)

    # 分析の実行
    results = run_analysis(target_csv)

    if not results:
        logging.warning("⚠️ 有効な相関結果が得られませんでした。データ件数や列名を確認してください。")
    else:
        # 結果をDataFrameに変換
        df_results = pd.DataFrame(results)

        # 有意水準マーカーを追加
        df_results["Sig"] = df_results["p_value"].apply(get_significance_marker)

        # 1. 回答精度(Score)との相関のみを抽出
        df_score_corr = df_results[df_results["Target"] == "Score"].copy()

        # 2. 相関係数の「絶対値(abs)」を表す作業列を作り、データセット名 ＞ 絶対値の降順 で並び替え
        df_score_corr["r_abs"] = df_score_corr["r"].abs()
        df_score_corr = df_score_corr.sort_values(
            by=["Dataset", "r_abs"], ascending=[True, False]
        ).reset_index(drop=True)

        # コンソールに見やすく表示
        print("\n" + "=" * 80)
        print("📈 相関分析結果 (LLM回答精度 vs 各指標: rの絶対値ランキング順)")
        print("=" * 80)

        display_cols = ["Dataset", "Metric", "Type", "r", "p_value", "Sig", "Control", "Bins"]
        print(df_score_corr[display_cols].to_string(index=False))
        print("=" * 80)

        # 3. メトリクス間相関（lm_cc vs num_semantic_units）があれば下部に別途表示
        df_metric_corr = df_results[df_results["Target"] != "Score"]
        if not df_metric_corr.empty:
            print("\n" + "-" * 80)
            print("🔗 メトリクス間相関 (lm_cc vs num_semantic_units)")
            print("-" * 80)
            print(df_metric_corr[["Dataset", "Target", "Metric", "r", "p_value", "Sig"]].to_string(index=False))
            print("-" * 80 + "\n")

        # 💡 必要に応じて結果をCSVとして保存（コメントアウトを解除）
        # output_path = target_csv.parent / f"correlation_results_{target_csv.stem}.csv"
        # df_results.to_csv(output_path, index=False)
        # logging.info(f"💾 相関結果を保存しました: {output_path}")