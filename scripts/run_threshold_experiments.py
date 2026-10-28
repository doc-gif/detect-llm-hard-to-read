import argparse
import sys
import pandas as pd
from pathlib import Path

# プロジェクトルートをPYTHONPATHに追加してモジュールを読み込めるようにする
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(PROJECT_ROOT), str(PROJECT_ROOT / "src"), str(PROJECT_ROOT / "src" / "analysis")]

# 先ほど改修した関数をインポート
from src.analysis.correlation_analysis import run_analysis
from src.analysis.thresholds import SAVED_SUMMARY_THRESHOLDS
from src.analysis.score_io import new_output_dir


def main(argv=None):
    parser = argparse.ArgumentParser(description="Analyze saved summaries with their recorded thresholds.")
    parser.add_argument("--output-dir", type=Path, help="New directory; existing paths are refused.")
    args = parser.parse_args(argv)
    # 保存CSVと照合した数値閾値を使う。pXXは過去のファイル名に対応する。
    thresholds = SAVED_SUMMARY_THRESHOLDS

    all_results = []

    out_dir = new_output_dir(PROJECT_ROOT / "results" / "experiments", args.output_dir)

    for label, thr in thresholds.items():
        print(f"\n=======================================================")
        print(f"🚀 実験開始: {label} (Threshold: {thr} nats)")
        print(f"=======================================================")

        suffix = f"_{label}"

        # 1. パイプラインを実行して、この閾値用のサマリーCSVを生成
        # print("▶️ 1. Pipelineを実行中...")
        # from src.analysis.pipeline import run_pipeline
        # run_pipeline(threshold=thr, suffix=suffix)

        # 2. 生成されたサマリーCSVを読み込んで相関分析を実行
        print("▶️ 2. 相関分析を実行中...")
        summary_csv = PROJECT_ROOT / "results" / "summaries" / f"analysis_summary{suffix}.csv"

        if summary_csv.exists():
            experiment_results = run_analysis(summary_csv)

            # 結果にどの閾値のデータかを紐付ける
            for r in experiment_results:
                r["Percentile_Label"] = label
                r["Threshold_Value"] = thr

            all_results.extend(experiment_results)
        else:
            print(f"⚠️ CSVが生成されませんでした: {summary_csv}")

    # 3. 全ての実験結果を1つのデータフレームにまとめてCSV出力
    if all_results:
        df_results = pd.DataFrame(all_results)

        # カラムの並び順を見やすく整理
        cols_order = ["Percentile_Label", "Threshold_Value", "Dataset", "Target", "Metric", "Type", "r", "p_value",
                      "Bins", "Min_Cnt", "Control"]
        df_results = df_results[cols_order]

        final_csv_path = out_dir / "threshold_correlation_results.csv"
        df_results.to_csv(final_csv_path, index=False, mode="x")

        print(f"\n🎉 全ての実験が完了しました！")
        print(f"📁 統合結果CSVを保存しました: {final_csv_path}")
    else:
        print("❌ 結果が取得できませんでした。")


if __name__ == "__main__":
    main()
