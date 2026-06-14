import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as plt_sns

from schema.records import SummarySchema

logging.basicConfig(level=logging.INFO, format="%(message)s")

# ==========================================
# ⚙️ 設定エリア
# ==========================================
SUMMARY_CSV_PATH = "/Users/hyoishitobi/PycharmProjects/detect-llm-hard-to-read/results/summaries/analysis_summary.csv"

# グラフを保存する大元の出力先ディレクトリ
OUTPUT_PLOT_DIR = Path("/Users/hyoishitobi/PycharmProjects/detect-llm-hard-to-read/results/plots")

SCORE_FILES = {
    "humaneval": {"path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/humaneval-ier/results_score.json",
                  "format": "simple"},
    "humaneval_simplified": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/humaneval-ier-simplified/results_score_simplified.json",
        "format": "simple"},
    "xcodeeval_apr": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/xcodeeval/apr/python_test_filtered_results.json",
        "format": "nested"},
    "xcodeeval_simplified_apr": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/xcodeeval/apr-simplified/python_test_filtered_results.json",
        "format": "nested"},
    "xcodeeval_code_translation": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/xcodeeval/code_translation/python2c_test_filtered_results.json",
        "format": "nested"},
    "xcodeeval_simplified_code_translation": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/xcodeeval/code_translation-simplified/python2c_test_filtered_results.json",
        "format": "nested"}
}

METRIC_LABELS = {
    SummarySchema.LM_CC: "Language Model Cognitive Complexity (LM-CC)",
    SummarySchema.PPL: "Perplexity (PPL)"
}


# ==========================================
# 関数定義
# ==========================================
def load_scores(dataset_name: str, config: dict) -> dict:
    path = Path(config["path"])
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    scores = {}
    if config["format"] == "simple":
        for k, v in data.items():
            uid = k.split("__")[0]
            scores[uid] = v
    elif config["format"] == "nested":
        for k, v in data.items():
            scores[k] = v.get("pass@1", 0.0)
    return scores


def create_scatter(df: pd.DataFrame, x_col: str, y_col: str, ax: plt.Axes, title: str, x_label: str,
                   raw_only: bool = False):
    if raw_only:
        plt_sns.scatterplot(
            data=df, x=x_col, y=y_col,
            alpha=0.4, s=30, color='#1f77b4',
            ax=ax,
        )
    else:
        is_binary = df[y_col].isin([0.0, 1.0]).all()

        plt_sns.regplot(
            data=df, x=x_col, y=y_col,
            logistic=is_binary,
            ci=None,
            scatter_kws={'alpha': 0.25, 's': 20, 'color': '#1f77b4'},
            line_kws={'color': '#17becf', 'alpha': 0.6, 'linestyle': '--'},
            ax=ax,
        )

        num_bins = min(10, len(df) // 5)
        if num_bins >= 3:
            try:
                df_copy = df.copy()
                df_copy['group'] = pd.qcut(df_copy[x_col], q=num_bins, duplicates='drop')
                agg_df = df_copy.groupby('group', observed=True).agg({
                    x_col: 'median',
                    y_col: 'mean'
                }).dropna()

                ax.scatter(
                    agg_df[x_col], agg_df[y_col],
                    color='#ff7f0e', s=120, edgecolor='black', zorder=5,
                    label='Bin Median/Mean'
                )
            except Exception as e:
                logging.debug(f"Binning failed for {x_col}: {e}")

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel("Reading Accuracy (pass@1)", fontsize=12)
    ax.set_ylim(-0.05, 1.05)

    ax.grid(True, linestyle=':', alpha=0.6)

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='best', fontsize=10)


# ==========================================
# メイン処理
# ==========================================
def main():
    if not Path(SUMMARY_CSV_PATH).exists():
        logging.error(f"❌ サマリーCSVが見つかりません: {SUMMARY_CSV_PATH}")
        return

    df_summary = pd.read_csv(SUMMARY_CSV_PATH)
    datasets = df_summary['dataset'].unique()

    print("🚀 分割された分布図の生成を開始します...")

    for ds in datasets:
        if ds not in SCORE_FILES:
            continue

        scores_dict = load_scores(ds, SCORE_FILES[ds])
        df_ds = df_summary[df_summary['dataset'] == ds].copy()
        df_ds['score'] = df_ds['uid'].map(scores_dict)

        df_clean = df_ds.dropna(subset=['score', SummarySchema.LM_CC, SummarySchema.PPL]).copy()

        if len(df_clean) < 10:
            logging.warning(f"⚠️ {ds}: データ数が少なすぎるためプロットをスキップします ({len(df_clean)}件)")
            continue

        print(f"📊 {ds} の画像を生成中... ({len(df_clean)}件)")

        # 💡 データセットごとの専用ディレクトリを作成
        safe_ds_name = ds.replace("/", "_").replace("\\", "_")
        ds_out_dir = OUTPUT_PLOT_DIR / safe_ds_name
        ds_out_dir.mkdir(parents=True, exist_ok=True)

        for metric in [SummarySchema.LM_CC, SummarySchema.PPL]:
            if metric not in df_clean.columns:
                continue

            x_label = METRIC_LABELS.get(metric, metric)
            safe_metric_name = metric.replace("_", "-")

            # --------------------------------------------------
            # 1. Raw Data (未処理) の画像をPNGで保存
            # --------------------------------------------------
            fig_raw, ax_raw = plt.subplots(figsize=(7, 6))
            title_raw = f"[{ds}] {metric.upper()} vs Accuracy"

            create_scatter(df_clean, metric, 'score', ax_raw, title_raw, x_label, raw_only=True)
            plt.tight_layout()

            # データセットごとのフォルダに保存 (PDF出力は廃止)
            fig_raw.savefig(ds_out_dir / f"{safe_metric_name}_raw.png", dpi=300, bbox_inches='tight')
            plt.close(fig_raw)

            # --------------------------------------------------
            # 2. Processed Data (ビン分割処理済み) の画像をPNGで保存
            # --------------------------------------------------
            fig_proc, ax_proc = plt.subplots(figsize=(7, 6))
            title_proc = f"[{ds}] {metric.upper()} vs Accuracy"

            create_scatter(df_clean, metric, 'score', ax_proc, title_proc, x_label, raw_only=False)
            plt.tight_layout()

            # データセットごとのフォルダに保存 (PDF出力は廃止)
            fig_proc.savefig(ds_out_dir / f"{safe_metric_name}_processed.png", dpi=300, bbox_inches='tight')
            plt.close(fig_proc)

    print(f"\n🎉 すべての画像の分割出力が完了しました！\n📂 保存先: {OUTPUT_PLOT_DIR}")


if __name__ == "__main__":
    plt_sns.set_theme(style="whitegrid", palette="muted")
    main()