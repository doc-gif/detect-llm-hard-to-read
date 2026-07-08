import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import warnings

# correlation_analysis.py で使用しているモジュールをインポート
from schema.records import SummarySchema
from src.analysis.util.correlation import get_grouped_partial_corr, group_by_metric

logging.basicConfig(level=logging.INFO, format="%(message)s")
warnings.filterwarnings("ignore", message="The covariance matrix is rank-deficient")

# ==========================================
# ⚙️ 設定エリア
# ==========================================
PROJECTS_DIR = Path(__file__).resolve().parent.parent.parent.parent
SUMMARY_CSV_PATH = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "summaries" / "analysis_summary.csv"

PLOT_OUTPUT_DIR = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "plots"
PLOT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EXTRACT_OUTPUT_DIR = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "extracted_groups"
EXTRACT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCORE_FILES = {
    "humaneval": {"path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier" / "results_score.json",
                  "format": "simple"},
    "xcodeeval_apr": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr" / "python_test_filtered_results.json",
        "format": "nested"},
    "xcodeeval_code_translation": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation" / "python2c_test_filtered_results.json",
        "format": "nested"}
}

METRICS_TO_ANALYZE = [SummarySchema.LM_CC]
CONTROL_VARIABLE = SummarySchema.LOC


# ==========================================
# 共通関数
# ==========================================
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
# プロット作成処理 (枠線と件数の追加)
# ==========================================
def plot_scatter(dataset_name, metric_name, all_metrics, all_scores, mean_metrics, mean_scores, r_val, p_val):
    plt.figure(figsize=(10, 8))
    sns.set_theme(style="whitegrid")

    # 1. 全個別データポイントのプロット
    plt.scatter(
        all_metrics, all_scores,
        color='gray', alpha=0.4, s=25, edgecolor='white', linewidth=0.5,
        label='All Individual Tasks'
    )

    # 2. ビニングされた代表点と回帰線の描画
    sns.regplot(
        x=mean_metrics,
        y=mean_scores,
        ci=None,
        scatter_kws={'s': 120, 'alpha': 0.9, 'edgecolor': 'w', 'color': '#2b8cbe'},
        line_kws={'color': '#f03b20', 'linestyle': '--', 'linewidth': 2},
        label='Binned Representatives'
    )

    # ---------------------------------------------------------
    # 💡 抽出グループ (A, B, C) の定義と枠線の描画
    # ---------------------------------------------------------
    max_metric = np.max(all_metrics)
    threshold = max_metric * 0.15  # 最大値の15%を閾値とする

    # 各グループの件数を算出
    group_A_count = np.sum((all_metrics >= threshold) & (all_scores == 0.0))
    group_B_count = np.sum((all_metrics <= threshold) & (all_scores == 0.0))
    group_C_count = np.sum((all_metrics <= threshold) & (all_scores == 1.0))

    ax = plt.gca()

    # 📦 グループA: 構造破綻コード (15%以上, Pass@1=0)
    rect_A = patches.Rectangle(
        (threshold, -0.05), (max_metric - threshold + (max_metric * 0.05)), 0.1,
        linewidth=2, edgecolor='red', facecolor='red', alpha=0.1, linestyle='--'
    )
    ax.add_patch(rect_A)
    ax.text(threshold + ((max_metric - threshold) / 2), 0.07,
            f"Group A\n(n={group_A_count})", color='red', ha='center', va='bottom', fontsize=10, weight='bold')

    # 📦 グループB: 構造以外の破綻コード (15%以下, Pass@1=0)
    rect_B = patches.Rectangle(
        (-max_metric * 0.02, -0.05), threshold + (max_metric * 0.02), 0.1,
        linewidth=2, edgecolor='orange', facecolor='orange', alpha=0.1, linestyle='--'
    )
    ax.add_patch(rect_B)
    ax.text(threshold / 2, 0.07,
            f"Group B\n(n={group_B_count})", color='orange', ha='center', va='bottom', fontsize=10, weight='bold')

    # 📦 グループC: 理想的なコード (15%以下, Pass@1=1)
    rect_C = patches.Rectangle(
        (-max_metric * 0.02, 0.95), threshold + (max_metric * 0.02), 0.1,
        linewidth=2, edgecolor='green', facecolor='green', alpha=0.1, linestyle='--'
    )
    ax.add_patch(rect_C)
    ax.text(threshold / 2, 0.93,
            f"Group C\n(n={group_C_count})", color='green', ha='center', va='top', fontsize=10, weight='bold')

    # タイトルと軸ラベルの設定
    plt.title(f"{metric_name} vs Accuracy (Pass@1) with Sampling Groups\n{dataset_name}", fontsize=14, pad=15)
    plt.xlabel(f"{metric_name} Score", fontsize=12)
    plt.ylabel("Accuracy (Pass@1)", fontsize=12)

    # 軸の固定
    plt.ylim(-0.1, 1.1)
    plt.xlim(left=- (max_metric * 0.02), right=(max_metric * 1.05))

    # 凡例・テキストの配置
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=True, fontsize=11)

    textstr = f"Partial Spearman $r$ = {r_val:.3f}   |   $p$-value "
    if p_val < 0.001:
        textstr += "< 0.001"
    else:
        textstr += f"= {p_val:.3f}"

    props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='gray')
    plt.gca().text(0.5, -0.25, textstr, transform=plt.gca().transAxes, fontsize=12,
                   verticalalignment='top', horizontalalignment='center', bbox=props)

    plt.tight_layout()

    safe_ds_name = dataset_name.replace(" ", "_").replace("(", "").replace(")", "")
    safe_metric_name = str(metric_name).replace(" ", "_")
    out_path = PLOT_OUTPUT_DIR / f"scatter_grouped_{safe_ds_name}_{safe_metric_name}.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  📸 プロットを保存しました: {out_path}")
    print(f"     -> [件数] Group A: {group_A_count}, Group B: {group_B_count}, Group C: {group_C_count}")


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
        if len(df_ds) == 0: continue

        for metric in METRICS_TO_ANALYZE:
            if metric not in df_ds.columns: continue
            df_target = df_ds.dropna(subset=[metric, 'score', CONTROL_VARIABLE]).copy()
            if len(df_target) < 10: continue

            score_arr = df_target['score'].values
            metric_arr = df_target[metric].values
            loc_arr = df_target[CONTROL_VARIABLE].values

            print(f"\n  🔹 指標: {metric}")

            # ---------------------------------------------------------
            # 💡 グループA, B, C の抽出とCSV保存
            # ---------------------------------------------------------
            max_metric = df_target[metric].max()
            threshold = max_metric * 0.15

            df_group_a = df_target[(df_target[metric] >= threshold) & (df_target['score'] == 0.0)].copy()
            df_group_b = df_target[(df_target[metric] <= threshold) & (df_target['score'] == 0.0)].copy()
            df_group_c = df_target[(df_target[metric] <= threshold) & (df_target['score'] == 1.0)].copy()

            df_group_a['group'] = 'A'
            df_group_b['group'] = 'B'
            df_group_c['group'] = 'C'
            df_extracted = pd.concat([df_group_a, df_group_b, df_group_c])

            out_csv_path = EXTRACT_OUTPUT_DIR / f"extracted_groups_{ds}_{metric}.csv"
            df_extracted[['uid', 'dataset', 'score', metric, CONTROL_VARIABLE, 'group']].to_csv(out_csv_path, index=False)
            print(f"  💾 抽出データを保存しました: {out_csv_path}")

            try:
                partial_corr, best_min_cnt_p = get_grouped_partial_corr(score_arr, metric_arr, loc_arr)
            except Exception as e:
                continue

            if partial_corr and partial_corr.get("partial_correlation") and best_min_cnt_p is not None:
                r_partial = partial_corr["partial_correlation"].get("spearman-r")
                p_partial = partial_corr["partial_correlation"].get("spearman-pval")

                if r_partial is not None and not np.isnan(r_partial):
                    mean_scores, _, mean_metrics, _ = group_by_metric(score_arr, metric_arr, None,
                                                                      min_cnt=best_min_cnt_p)

                    plot_scatter(ds, metric, metric_arr, score_arr, mean_metrics, mean_scores, r_partial, p_partial)


if __name__ == "__main__":
    main()