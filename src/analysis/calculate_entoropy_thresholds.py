import pandas as pd
from pathlib import Path
import os


def main():
    # 実行ディレクトリ (src/analysis) からプロジェクトルートへのパスを解決
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent

    # Parquetファイルが格納されているベースディレクトリ
    enriched_dir = project_root / "results" / "enriched"

    # 検索対象の3つのディレクトリ
    dirs_to_search = [
        enriched_dir / "humaneval",
        enriched_dir / "xcodeeval_apr",
        enriched_dir / "xcodeeval_code_translation"
    ]

    all_entropies = []
    total_files_processed = 0

    print("Parquetファイルの読み込みを開始します...")

    for target_dir in dirs_to_search:
        if not target_dir.exists():
            print(f"⚠️ ディレクトリが見つかりません: {target_dir}")
            continue

        # ディレクトリ内のすべての .parquet ファイルを検索
        for parquet_file in target_dir.glob("*.parquet"):
            try:
                # メモリ節約のため 'metric_entropy' カラムのみを読み込む
                df = pd.read_parquet(parquet_file, columns=["metric_entropy"])

                # 欠損値 (NaN) を除外してリストに結合
                entropies = df["metric_entropy"].dropna().tolist()
                all_entropies.extend(entropies)
                total_files_processed += 1

            except Exception as e:
                print(f"❌ ファイル読み込みエラー ({parquet_file.name}): {e}")

    if not all_entropies:
        print("❌ エントロピーデータが見つかりませんでした。パスを確認してください。")
        return

    print(f"読み込み完了: 計 {total_files_processed} ファイル, 全 {len(all_entropies):,} トークン\n")

    # Pandas Series に変換して統計量を計算
    entropy_series = pd.Series(all_entropies)

    print("==================================================")
    print("📊 トークンエントロピー 閾値（パーセンタイル）分析結果")
    print("==================================================")

    thresholds = {}
    # 50から95まで、5刻みでループ処理
    for p in range(0, 100, 5):
        val = entropy_series.quantile(p / 100.0)
        thresholds[p] = val
        print(f"・{p}th Percentile (上位{100 - p:02d}%) : {val:.4f} nats")

    print("==================================================\n")

    # グラフの作成と保存
    # print("📈 エントロピーの分布図を生成しています...")
    # try:
    #     import matplotlib.pyplot as plt
    #
    #     # 日本語フォントの簡易設定 (Windows: Meiryo, Mac: Hiragino)
    #     plt.rcParams['font.family'] = ['Meiryo', 'Hiragino Maru Gothic Pro', 'sans-serif']
    #
    #     plt.figure(figsize=(12, 6))
    #
    #     # ヒストグラムの描画（ビンの数を100にして細かく分布を表示）
    #     plt.hist(entropy_series, bins=100, color='skyblue', edgecolor='black', alpha=0.7)
    #
    #     # 重要な閾値を縦線でハイライト表示（50, 65, 80, 95）
    #     # ※ 65は論文の67%付近の参考値として、80は本命のForking Tokensとして
    #     highlight_percentiles = [50, 65, 80, 95]
    #     colors = ['green', 'orange', 'red', 'purple']
    #
    #     for i, p in enumerate(highlight_percentiles):
    #         if p in thresholds:
    #             plt.axvline(x=thresholds[p], color=colors[i], linestyle='dashed', linewidth=2,
    #                         label=f'{p}th Percentile ({thresholds[p]:.2f} nats)')
    #
    #     # グラフの装飾
    #     plt.title("トークンエントロピーの分布 (Token Entropy Distribution)", fontsize=16)
    #     plt.xlabel("トークンエントロピー [nats]", fontsize=14)
    #     plt.ylabel("頻度 (Frequency)", fontsize=14)
    #     plt.legend(fontsize=12)
    #     plt.grid(axis='y', linestyle='--', alpha=0.7)
    #     plt.tight_layout()
    #
    #     # 画像として保存 (results ディレクトリ直下)
    #     output_image_path = project_root / "results" / "entropy_distribution.png"
    #     # ディレクトリが存在しない場合は作成
    #     output_image_path.parent.mkdir(parents=True, exist_ok=True)
    #     plt.savefig(output_image_path)
    #
    #     print(f"✅ 分布図を保存しました: {output_image_path}")
    #
    # except ImportError:
    #     print("⚠️ matplotlibがインストールされていないため、分布図の作成をスキップしました。")
    #     print("   グラフを作成する場合はターミナルで 'pip install matplotlib' を実行してください。")


if __name__ == "__main__":
    main()