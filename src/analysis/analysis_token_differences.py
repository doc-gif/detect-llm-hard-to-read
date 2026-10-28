import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import spearmanr, pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# ==========================================
# 1. パスと設定
# ==========================================
PROJECTS_DIR = Path(__file__).resolve().parent.parent.parent.parent

BASE_DIR_MINE = PROJECTS_DIR / "detect-llm-hard-to-read" / "out"
BASE_DIR_PRIOR = PROJECTS_DIR / "lm-cc" / "results"

# 出力先ディレクトリの作成
OUTPUT_DIR = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "token_analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = [
    # {
    #     "name": "HumanEval",
    #     "prior_json": BASE_DIR_PRIOR / "humaneval-ier" / "entropy" / "entropies-CodeLlama-7b-hf-1.0.json",
    #     "my_dir": BASE_DIR_MINE / "humaneval",
    #     "parquet_format": "result_{task_id}.parquet"
    # },
    # {
    #     "name": "HumanEval-simplified",
    #     "prior_json": BASE_DIR_PRIOR / "humaneval-ier-simplified" / "entropy" / "entropies-CodeLlama-7b-hf-1.0.json",
    #     "my_dir": BASE_DIR_MINE / "humaneval_simplified-top60",
    #     "parquet_format": "result_{task_id}.parquet"
    # },
    {
        "name": "XcodeEval(APR)",
        "prior_json": BASE_DIR_PRIOR / "xcodeeval" / "apr" / "entropy" / "entropies-CodeLlama-7b-hf-1.0.json",
        "my_dir": BASE_DIR_MINE / "xcodeeval_apr",
        "parquet_format": "result_{task_id}.parquet"
    },
    # {
    #     "name": "XcodeEval-simplified(APR)",
    #     "prior_json": BASE_DIR_PRIOR / "xcodeeval" / "apr-simplified" / "entropy" / "entropies-CodeLlama-7b-hf-1.0.json",
    #     "my_dir": BASE_DIR_MINE / "xcodeeval_simplified-top50_apr",
    #     "parquet_format": "result_{task_id}.parquet"
    # },
    {
        "name": "XcodeEval(Code Translation)",
        "prior_json": BASE_DIR_PRIOR / "xcodeeval" / "code_translation" / "entropy" / "entropies-CodeLlama-7b-hf-1.0.json",
        "my_dir": BASE_DIR_MINE / "xcodeeval_code_translation",
        "parquet_format": "result_{task_id}.parquet"
    },
    # {
    #     "name": "XcodeEval-simplified(Code Translation)",
    #     "prior_json": BASE_DIR_PRIOR / "xcodeeval" / "code_translation-simplified" / "entropy" / "entropies-CodeLlama-7b-hf-1.0.json",
    #     "my_dir": BASE_DIR_MINE / "xcodeeval_simplified-top50_code_translation",
    #     "parquet_format": "result_{task_id}.parquet"
    # }
]

# グラフの見た目設定
sns.set_theme(style="whitegrid")


# ==========================================
# 2. 分析ロジック (単一タスクの計算)
# ==========================================
def calculate_entropy_metrics(ds_name, task_id, prior_entropies, my_entropies, my_tokens):
    prior = np.array(prior_entropies, dtype=float)
    mine = np.array(my_entropies, dtype=float)

    # NaNのクリーニング
    if np.isnan(mine).any():
        valid_idx = ~np.isnan(mine)
        mine = mine[valid_idx]
        if my_tokens is not None:
            my_tokens = np.array(my_tokens)[valid_idx]

    len_prior, len_mine = len(prior), len(mine)
    min_len = min(len_prior, len_mine)
    is_length_match = (len_prior == len_mine)

    if min_len < 2:
        return None, []

    prior = prior[:min_len]
    mine = mine[:min_len]
    if my_tokens is not None:
        my_tokens = my_tokens[:min_len]

    diff = prior - mine
    abs_diff = np.abs(diff)
    mae = np.mean(abs_diff)
    max_error = np.max(abs_diff)

    spearman_corr, _ = spearmanr(prior, mine)
    pearson_corr, _ = pearsonr(prior, mine)

    status = "Perfect" if max_error == 0 else "Acceptable" if max_error < 1e-2 else "Error"

    # サマリーデータ
    summary = {
        "dataset": ds_name,
        "task_id": task_id,
        "prior_tokens": len_prior,
        "my_tokens": len_mine,
        "mae": mae,
        "max_error": max_error,
        "spearman_corr": spearman_corr,
        "pearson_corr": pearson_corr,
        "is_length_match": is_length_match,
        "status": status
    }

    # 詳細データ (ファイルサイズ節約のため、誤差が0.01以上のトークンのみ抽出)
    details = []
    if status == "Error":
        error_indices = np.where(abs_diff >= 0.01)[0]
        for idx in error_indices:
            details.append({
                "dataset": ds_name,
                "task_id": task_id,
                "token_index": idx,
                "token_str": my_tokens[idx] if my_tokens is not None else "",
                "prior_entropy": prior[idx],
                "my_entropy": mine[idx],
                "abs_diff": abs_diff[idx]
            })

    return summary, details, prior, mine


# ==========================================
# 3. グラフ描画ロジック
# ==========================================
def plot_results(df_summary, worst_tasks_data):
    print("\n📊 グラフを生成しています...")

    # ① 相関の箱ひげ図
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_summary, x='spearman_corr', y='dataset', palette="viridis")
    plt.title("Spearman Correlation Distribution by Dataset (1.0 = Perfect Match)")
    plt.xlabel("Spearman Correlation")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "plot_1_correlation_boxplot.png")
    plt.close()

    # ② 誤差(MAE)のヒストグラム (Errorが含まれるOriginalデータセット用)
    plt.figure(figsize=(10, 6))
    df_errors = df_summary[df_summary['mae'] > 0.01]
    if not df_errors.empty:
        sns.histplot(data=df_errors, x='mae', hue='dataset', element="step", bins=30)
        plt.title("Distribution of Mean Absolute Error (MAE > 0.01)")
        plt.xlabel("MAE")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "plot_2_mae_histogram.png")
    plt.close()

    # ③ 外れ値タスクの折れ線グラフ (ワースト3件)
    if worst_tasks_data:
        fig, axes = plt.subplots(len(worst_tasks_data), 1, figsize=(12, 4 * len(worst_tasks_data)))
        if len(worst_tasks_data) == 1: axes = [axes]

        for ax, task_data in zip(axes, worst_tasks_data):
            ax.plot(task_data['prior'], label='Prior (Paper)', alpha=0.8, linewidth=2)
            ax.plot(task_data['mine'], label='Mine (Replicated)', alpha=0.8, linewidth=2, linestyle='--')
            ax.set_title(
                f"Entropy Transition: {task_data['dataset']} - {task_data['task_id']} (MAE: {task_data['mae']:.4f})")
            ax.set_xlabel("Token Index")
            ax.set_ylabel("Entropy")
            ax.legend()

        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "plot_3_worst_tasks_transition.png")
        plt.close()


# ==========================================
# 4. メイン処理
# ==========================================
def run_analysis():
    all_summaries = []
    all_details = []

    # グラフ描画用に「誤差が大きいワースト3」の波形データを保持
    worst_tasks_data = []

    for dataset in DATASETS:
        ds_name = dataset["name"]
        prior_json_path = dataset["prior_json"]
        my_dir = dataset["my_dir"]

        if not prior_json_path.exists():
            continue

        with prior_json_path.open('r', encoding='utf-8') as f:
            prior_data = json.load(f)

        print(f"\n🚀 処理中: {ds_name} ({len(prior_data)} 件)")

        # プログレスバーで進捗を表示
        for item in tqdm(prior_data, desc="Analyzing", unit="task"):
            task_id = item.get("task_id")
            prior_entropies = item.get("entropies", [])

            safe_task_id = str(task_id).replace("/", "_")
            parquet_path = my_dir / dataset["parquet_format"].format(task_id=safe_task_id)

            if not parquet_path.exists():
                continue

            try:
                df = pd.read_parquet(parquet_path)
                if "metric_entropy" not in df.columns:
                    continue

                my_entropies = df["metric_entropy"].values
                my_tokens = df["token_str"].values if "token_str" in df.columns else None

                summary, details, prior_arr, mine_arr = calculate_entropy_metrics(
                    ds_name, task_id, prior_entropies, my_entropies, my_tokens
                )

                if summary:
                    all_summaries.append(summary)
                    all_details.extend(details)

                    # Error判定されたものをワースト記録候補として保持
                    if summary["status"] == "Error":
                        worst_tasks_data.append({
                            "dataset": ds_name,
                            "task_id": task_id,
                            "mae": summary["mae"],
                            "prior": prior_arr,
                            "mine": mine_arr
                        })

            except Exception:
                continue

    # ワーストタスクをMAEが大きい順にソートし、Top 3を抽出
    worst_tasks_data = sorted(worst_tasks_data, key=lambda x: x["mae"], reverse=True)[:3]

    # --- CSV出力 ---
    print("\n💾 データをCSVに保存しています...")
    df_summary = pd.DataFrame(all_summaries)
    df_details = pd.DataFrame(all_details)

    summary_path = OUTPUT_DIR / "analysis_summary.csv"
    details_path = OUTPUT_DIR / "token_diff_details.csv"

    df_summary.to_csv(summary_path, index=False)
    if not df_details.empty:
        df_details.to_csv(details_path, index=False)

    print(f"  ✅ {summary_path.name} を保存しました。")
    print(f"  ✅ {details_path.name} を保存しました。")

    # --- グラフ出力 ---
    plot_results(df_summary, worst_tasks_data)
    print(f"  ✅ グラフ画像を {OUTPUT_DIR.name}/ ディレクトリに保存しました。")
    print("\n🎉 全ての処理が完了しました！")


if __name__ == "__main__":
    run_analysis()