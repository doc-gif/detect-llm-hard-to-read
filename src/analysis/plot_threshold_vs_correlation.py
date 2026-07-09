import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def main():
    # パス設定
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent

    results_csv_path = project_root / "results" / "experiments" / "threshold_correlation_results.csv"
    output_dir = project_root / "results" / "experiments" / "plots"

    if not results_csv_path.exists():
        print(f"❌ 結果CSVが見つかりません。先に run_threshold_experiments.py を実行してください。")
        print(f"   参照パス: {results_csv_path}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # データの読み込み
    df = pd.read_csv(results_csv_path)

    # TargetがScore（精度との相関）のものだけ抽出
    df_score = df[df["Target"] == "Score"].copy()

    if df_score.empty:
        print("❌ 'Target' が 'Score' のデータが見つかりませんでした。")
        return

    # Percentile_Label (p50, p80など) から数値だけを抽出してX軸用にする
    df_score["Percentile_Num"] = df_score["Percentile_Label"].str.replace("p", "").astype(int)

    # グラフのスタイル設定 (日本語フォント対応)
    plt.rcParams['font.family'] = ['Meiryo', 'Hiragino Maru Gothic Pro', 'sans-serif']
    # Seabornのスタイルを適用
    sns.set_theme(style="whitegrid", font=["Meiryo", "Hiragino Maru Gothic Pro", "sans-serif"])

    datasets = df_score["Dataset"].unique()
    corr_types = df_score["Type"].unique()

    print("📈 閾値 vs 相関係数のグラフを生成しています...")

    for ds in datasets:
        for c_type in corr_types:
            # データセットと相関タイプ（Partial / Zero-Order）で絞り込み
            df_plot = df_score[(df_score["Dataset"] == ds) & (df_score["Type"] == c_type)]
            if df_plot.empty:
                continue

            plt.figure(figsize=(10, 6))

            # LM_CCとNUM_SEMANTIC_UNITSの2つのラインをプロット
            sns.lineplot(
                data=df_plot,
                x="Percentile_Num",
                y="r",
                hue="Metric",
                marker="o",
                linewidth=2.5,
                markersize=8,
                palette="Set1"  # 見やすい配色
            )

            # グラフの装飾
            plt.title(f"Threshold vs LLM Score Correlation\n(Dataset: {ds} | Type: {c_type})", fontsize=15, pad=15)
            plt.xlabel("Threshold (Percentile)", fontsize=13)
            plt.ylabel("Spearman Correlation (r)", fontsize=13)

            # X軸の目盛りを存在するパーセンタイルのみに設定
            plt.xticks(sorted(df_plot["Percentile_Num"].unique()))

            # 相関ゼロのライン（基準線）を引く
            plt.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)

            plt.legend(title="Metric", fontsize=11, title_fontsize=12)
            plt.tight_layout()

            # ファイル名にスラッシュが入らないようにサニタイズ
            safe_ds_name = str(ds).replace("/", "_").replace("\\", "_")
            out_filename = output_dir / f"threshold_vs_r_{safe_ds_name}_{c_type}.png"

            # 画像として保存
            plt.savefig(out_filename, dpi=300)
            plt.close()

            print(f"  ✅ 保存完了: {out_filename.name}")

    print(f"\n🎉 全てのグラフが {output_dir} に出力されました！")


if __name__ == "__main__":
    main()
