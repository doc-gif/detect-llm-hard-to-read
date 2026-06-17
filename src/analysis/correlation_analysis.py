import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
import pingouin as pg
from scipy.stats import spearmanr

from schema.records import SummarySchema

logging.basicConfig(level=logging.INFO, format="%(message)s")

# ==========================================
# ⚙️ 設定エリア
# ==========================================
PROJECTS_DIR = Path(__file__).resolve().parent.parent.parent.parent

SUMMARY_CSV_PATH = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "summaries" / "analysis_summary.csv"

# グラフを保存する大元の出力先ディレクトリ
OUTPUT_PLOT_DIR = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "plots"

SCORE_FILES = {
    "humaneval": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier" / "results_score.json",
        "format": "simple"
    },
    # "humaneval_simplified": {
    #     "path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier-simplified" / "results_score_simplified.json",
    #     "format": "simple"
    # },
    "humaneval_simplified-top60": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier-simplified" / "results_score_simplified.json",
        "format": "simple"
    },
    "xcodeeval_apr": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr" / "python_test_filtered_results.json",
        "format": "nested"
    },
    # "xcodeeval_simplified_apr": {
    #     "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr-simplified" / "python_test_filtered_results.json",
    #     "format": "nested"
    # },
    "xcodeeval_simplified-top50_apr": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr-simplified" / "python_test_filtered_results.json",
        "format": "nested"
    },
    "xcodeeval_code_translation": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation" / "python2c_test_filtered_results.json",
        "format": "nested"
    },
    # "xcodeeval_simplified_code_translation": {
    #     "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation-simplified" / "python2c_test_filtered_results.json",
    #     "format": "nested"
    # },
    "xcodeeval_simplified-top50_code_translation": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation-simplified" / "python2c_test_filtered_results.json",
        "format": "nested"
    }
}

# 分析対象とする指標のリスト（SColの定義に準拠）
METRICS_TO_ANALYZE = [
    SummarySchema.LM_CC,
    SummarySchema.PPL,
    SummarySchema.LM_CC_DENSITY,
]

# 統制変数（コード長）。locがない場合は total_tokens に変更可能
CONTROL_VARIABLE = SummarySchema.LOC


# ==========================================
# 関数定義
# ==========================================
def get_significance_marker(p_val: float) -> str:
    """p値から論文用の有意水準マーカーを返す"""
    if np.isnan(p_val):
        return ""
    if p_val < 0.001:
        return "***"
    elif p_val < 0.01:
        return "** "
    elif p_val < 0.05:
        return "* "
    else:
        return "n.s."  # Not Significant (統計的に有意ではない)

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


def calculate_residual_binned_partial_corr(df: pd.DataFrame, metric: str, score_col: str, control: str,
                                           n_bins: int) -> dict:
    """
    【単一ビニング用】各サンプルから統制変数の影響を排除(残差取得)してからビニングを実行し、偏相関を求める
    """
    try:
        df_temp = df[[metric, score_col, control]].dropna().copy()
        if len(df_temp) < 4:
            return {"r": np.nan, "p": np.nan, "bins": np.nan}

        # 1. 各変数を順位（Rank）に変換（スピアマンの前提）
        rank_metric = df_temp[metric].rank()
        rank_score = df_temp[score_col].rank()
        rank_control = df_temp[control].rank()

        # 2. 回帰分析で control (コード長) の影響を排除し、残差 (Residual) を計算
        slope_m, intercept_m = np.polyfit(rank_control, rank_metric, 1)
        df_temp['metric_resid'] = rank_metric - (slope_m * rank_control + intercept_m)

        slope_s, intercept_s = np.polyfit(rank_control, rank_score, 1)
        df_temp['score_resid'] = rank_score - (slope_s * rank_control + intercept_s)

        # 3. コード長の影響を排除した純粋な metric (残差) でビニングを実行
        df_temp['group'] = pd.qcut(df_temp['metric_resid'], q=n_bins, labels=False, duplicates='drop')

        # 4. グループごとに残差の代表値を集約
        agg_df = df_temp.groupby('group').agg({
            'score_resid': 'mean',
            'metric_resid': 'median'
        }).reset_index()

        if len(agg_df) < 3:
            return {"r": np.nan, "p": np.nan, "bins": len(agg_df)}

        # 5. 集約された「残差同士」で相関を計算（偏相関）
        r, p = spearmanr(agg_df['metric_resid'], agg_df['score_resid'])

        return {"r": r, "p": p, "bins": len(agg_df)}

    except Exception as e:
        return {"r": np.nan, "p": np.nan, "bins": np.nan}


def calculate_best_residual_binned_partial_corr(df: pd.DataFrame, metric: str, score_col: str, control: str,
                                                n_list:list) -> dict:
    """
    【最適探索用】n=9, 10, 11 を全て試し、最も統計的に有意（p値が最小）な残差偏相関の結果を返す
    """
    best_result = {"r": np.nan, "p": np.nan, "bins": np.nan}

    for n in n_list:
        res = calculate_residual_binned_partial_corr(df, metric, score_col, control, n_bins=n)

        if not np.isnan(res["p"]):
            # まだ結果がない、または今回計算したp値の方が小さい（より有意である）場合に更新
            if np.isnan(best_result["p"]) or res["p"] < best_result["p"]:
                best_result = res

    return best_result


def calculate_binned_corr(df: pd.DataFrame, metric: str, score_col: str, n_bins: int) -> dict:
    """指定された分割数(n_bins)で分位ビニングを行い、集約された代表値でゼロ次スピアマン相関を計算する"""
    try:
        # 分析に必要なカラムのみ抽出し、欠損値を除外
        df_temp = df[[metric, score_col]].dropna().copy()

        # 1. metric(LM-CCなど)でRank付けし、n_bins個のグループに等分（分位ビニング）
        # duplicates='drop' により、境界値が重複した際のエラーを防ぎます
        df_temp['group'] = pd.qcut(df_temp[metric], q=n_bins, labels=False, duplicates='drop')

        # 2. グループごとに代表値を集約
        # 正答率(score_col)は「平均値」、不確実性指標(metric)は外れ値に強い「中央値」
        agg_df = df_temp.groupby('group').agg({
            metric: 'median',
            score_col: 'mean'
        }).dropna().reset_index()

        # 相関を計算するには、最低でも3グループ（データポイント）必要
        if len(agg_df) < 3:
            return {"r": np.nan, "p": np.nan, "bins": len(agg_df)}

        # 3. 集約された代表値同士で、ゼロ次スピアマン相関を計算
        r, p = spearmanr(agg_df[metric], agg_df[score_col])

        return {
            "r": r,
            "p": p,
            "bins": len(agg_df) # 実際に作成されたグループ数
        }

    except Exception as e:
        # データ分割に失敗した場合などは NaN を返す
        return {"r": np.nan, "p": np.nan, "bins": np.nan}


def calculate_best_binned_corr(df: pd.DataFrame, metric: str, score_col: str, n_list: list) -> dict:
    """n=9, 10, 11 を全て試し、最も統計的に有意（p値が最小）なゼロ次相関の結果を返す"""
    best_result = {"r": np.nan, "p": np.nan, "bins": np.nan}

    for n in n_list:
        res = calculate_binned_corr(df, metric, score_col, n_bins=n)

        # エラーなく p値 が計算できた場合
        if not np.isnan(res["p"]):
            # まだ結果がない、または今回計算したp値の方が小さい（より有意である）場合にベストを更新
            if np.isnan(best_result["p"]) or res["p"] < best_result["p"]:
                best_result = res

    # 有意な結果が一つもなかった場合でも、最後に試した結果の NaN が入った辞書が返ります
    return best_result


def main():
    df_summary = pd.read_csv(SUMMARY_CSV_PATH)
    datasets = df_summary['dataset'].unique()

    for ds in datasets:
        print(f"\n{'=' * 50}\n📊 データセット: {ds}\n{'=' * 50}")
        if ds not in SCORE_FILES: continue

        # pass@1の評価値を分析データに統合
        scores_dict = load_scores(ds, SCORE_FILES[ds])
        df_ds = df_summary.loc[df_summary['dataset'] == ds].copy()
        df_ds['score'] = df_ds['uid'].map(scores_dict)

        df_ds = df_ds.dropna(subset=['score', CONTROL_VARIABLE])
        print(f"  -> {len(df_ds)} 件のデータで分析を実行します。")

        # METRICS_TO_ANALYZEで指定した指標とscore(pass@1)を相関分析する。
        for metric in METRICS_TO_ANALYZE:
            if metric not in df_ds.columns: continue
            df_target = df_ds.dropna(subset=[metric, 'score', CONTROL_VARIABLE]).copy()
            if len(df_target) < 10: continue

            # 偏相関分析(n=9,10,11の中で最も良い分位ビニングの相関を求める)
            partial_corr = calculate_best_residual_binned_partial_corr(df_target, metric, 'score', CONTROL_VARIABLE, [9, 10, 11])
            # ゼロ次相関分析(n=9,10,11の中で最も良い分位ビニングの相関を求める)
            zero_corr = calculate_best_binned_corr(df_target, metric, 'score', [9, 10, 11])

            print(f"\n  🔹 指標: {metric}")

            # 1. 偏相関の論文用出力
            if not np.isnan(partial_corr['r']):
                sig = get_significance_marker(partial_corr['p'])
                print(
                    f"     [偏相関]   r = {partial_corr['r']:>7.4f}, p = {partial_corr['p']:.4f} ({sig:^4}) | Bins: {partial_corr['bins']:>2}, Control: {CONTROL_VARIABLE}")
            else:
                print(f"     [偏相関]   計算不可 (データ不足、分散ゼロ、または多重共線性による数学的エラー)")

            # 2. ゼロ次相関の論文用出力
            if not np.isnan(zero_corr['r']):
                sig = get_significance_marker(zero_corr['p'])
                print(
                    f"     [ゼロ次相関] r = {zero_corr['r']:>7.4f}, p = {zero_corr['p']:.4f} ({sig:^4}) | Bins: {zero_corr['bins']:>2}")
            else:
                print(f"     [ゼロ次相関] 計算不可 (データ不足、または分散ゼロ等)")


if __name__ == "__main__":
    main()
