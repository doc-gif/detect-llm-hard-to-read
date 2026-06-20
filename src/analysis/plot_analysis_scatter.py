import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
import matplotlib.pyplot as plt
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
# correlation_analysis.py と同じパス解決
PROJECTS_DIR = Path(__file__).resolve().parent.parent.parent.parent
SUMMARY_CSV_PATH = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "summaries" / "analysis_summary.csv"

# 💡 プロット画像の保存先 (detect-llm-hard-to-read/results/plots)
PLOT_OUTPUT_DIR = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "plots"
PLOT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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

# 散布図を作成したいメトリクスを指定
METRICS_TO_ANALYZE = [
    SummarySchema.LM_CC,
    # SummarySchema.PPL,
    # SummarySchema.LM_CC_DENSITY,
]
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
# プロット作成処理
# ==========================================
def plot_scatter(dataset_name, metric_name, all_metrics, all_scores, mean_metrics, mean_scores, r_val, p_val):
    # 下部の余白を確保するため、縦幅を少し大きめに設定
    plt.figure(figsize=(9, 7))
    sns.set_theme(style="whitegrid")

    # 1. 全個別データポイントのプロット
    plt.scatter(
        all_metrics, all_scores,
        color='gray', alpha=0.3, s=20, edgecolor='none',
        label='All Individual Tasks'
    )

    # 2. ビニングされた代表点と回帰線 (トレンドライン) の描画
    sns.regplot(
        x=mean_metrics,
        y=mean_scores,
        ci=None,
        scatter_kws={'s': 100, 'alpha': 0.9, 'edgecolor': 'w', 'color': '#2b8cbe'},
        line_kws={'color': '#f03b20', 'linestyle': '--', 'linewidth': 2},
        label='Binned Representatives'
    )

    # タイトルと軸ラベルの設定
    plt.title(f"{metric_name} vs Accuracy (Pass@1)\n{dataset_name}", fontsize=14, pad=15)
    plt.xlabel(f"{metric_name} Score", fontsize=12)
    plt.ylabel("Accuracy (Pass@1)", fontsize=12)

    # y軸（正答率）の範囲を0.0〜1.05に固定
    plt.ylim(-0.05, 1.05)

    # 💡 凡例をグラフの下（X軸ラベルのさらに下）の中央に2列で配置
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=True, fontsize=11)

    # 💡 相関係数とp値のテキストを1行にまとめ、凡例のさらに下に配置
    textstr = f"Partial Spearman $r$ = {r_val:.3f}   |   $p$-value "
    if p_val < 0.001:
        textstr += "< 0.001"
    else:
        textstr += f"= {p_val:.3f}"

    props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='gray')
    plt.gca().text(0.5, -0.28, textstr, transform=plt.gca().transAxes, fontsize=12,
                   verticalalignment='top', horizontalalignment='center', bbox=props)

    plt.tight_layout()

    # 画像保存時に枠外の要素が見切れないように bbox_inches='tight' を指定
    safe_ds_name = dataset_name.replace(" ", "_").replace("(", "").replace(")", "")
    safe_metric_name = str(metric_name).replace(" ", "_")
    out_path = PLOT_OUTPUT_DIR / f"scatter_partial_{safe_ds_name}_{safe_metric_name}.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  📸 プロットを保存しました: {out_path}")


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

        # スコアとコントロール変数（LOC）で欠損値を弾く
        df_ds = df_ds.dropna(subset=['score', CONTROL_VARIABLE])

        if len(df_ds) == 0:
            print("  ❌ 有効なデータがありません。")
            continue

        for metric in METRICS_TO_ANALYZE:
            if metric not in df_ds.columns: continue
            df_target = df_ds.dropna(subset=[metric, 'score', CONTROL_VARIABLE]).copy()
            if len(df_target) < 10:
                print(f"  ⚠️ {metric} のデータ件数が少なすぎるためスキップします。")
                continue

            # データ配列の抽出
            score_arr = df_target['score'].values
            metric_arr = df_target[metric].values
            loc_arr = df_target[CONTROL_VARIABLE].values

            print(f"\n  🔹 指標: {metric}")

            # 偏相関（LOCを考慮）の最適なグループ化パラメータを取得
            try:
                partial_corr, best_min_cnt_p = get_grouped_partial_corr(score_arr, metric_arr, loc_arr)
            except Exception as e:
                print(f"  ❌ {metric} の相関計算エラー: {e}")
                continue

            if partial_corr and partial_corr.get("partial_correlation") and best_min_cnt_p is not None:
                r_partial = partial_corr["partial_correlation"].get("spearman-r")
                p_partial = partial_corr["partial_correlation"].get("spearman-pval")

                if r_partial is not None and not np.isnan(r_partial):
                    print(f"  🔍 最適なBinサイズ (min_cnt): {best_min_cnt_p}")

                    # グラフ描画用に代表点（平均と中央値）を取得 (X軸・Y軸のプロット用なので loc=None)
                    mean_scores, _, mean_metrics, _ = group_by_metric(score_arr, metric_arr, None,
                                                                      min_cnt=best_min_cnt_p)

                    # グラフの描画
                    plot_scatter(ds, metric, metric_arr, score_arr, mean_metrics, mean_scores, r_partial, p_partial)
                else:
                    print(f"  ❌ {metric} の相関係数が有効でないため、プロットをスキップします。")
            else:
                print(f"  ❌ {metric} の相関係数が有効でないため、プロットをスキップします。")


if __name__ == "__main__":
    main()