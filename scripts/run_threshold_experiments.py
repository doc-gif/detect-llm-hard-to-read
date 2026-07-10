import sys
import pandas as pd
from pathlib import Path

# プロジェクトルートをPYTHONPATHに追加してモジュールを読み込めるようにする
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# 先ほど改修した関数をインポート
from src.analysis.pipeline import run_pipeline
from src.analysis.correlation_analysis import run_analysis


def main():
    # 📝 先ほど計測した各パーセンタイルの閾値リスト
    thresholds = {
        "p05": 0.0037,
        "p10": 0.0114,
        "p15": 0.0214,
        "p20": 0.0335,
        "p25": 0.0483,
        "p30": 0.0675,
        "p35": 0.0921,
        "p40": 0.1244,
        "p45": 0.1691,
        "p50": 0.2327,
        "p55": 0.3254,
        "p60": 0.4536,
        "p65": 0.6154,
        "p67": 0.6813,
        "p70": 0.7781,
        "p75": 0.9829,
        "p80": 1.2515,
        "p85": 1.5920,
        "p90": 2.1097,
        "p95": 3.2355
    }

    all_results = []

    out_dir = PROJECT_ROOT / "results" / "experiments"
    out_dir.mkdir(parents=True, exist_ok=True)

    for label, thr in thresholds.items():
        print(f"\n=======================================================")
        print(f"🚀 実験開始: {label} (Threshold: {thr} nats)")
        print(f"=======================================================")

        suffix = f"_{label}"

        # 1. パイプラインを実行して、この閾値用のサマリーCSVを生成
        # print("▶️ 1. Pipelineを実行中...")
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
        df_results.to_csv(final_csv_path, index=False)

        print(f"\n🎉 全ての実験が完了しました！")
        print(f"📁 統合結果CSVを保存しました: {final_csv_path}")
    else:
        print("❌ 結果が取得できませんでした。")


if __name__ == "__main__":
    main()
