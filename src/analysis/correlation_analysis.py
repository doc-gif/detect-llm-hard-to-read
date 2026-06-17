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
OUTPUT_PLOT_DIR = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "plots"

SCORE_FILES = {
    "humaneval": {"path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier" / "results_score.json",
                  "format": "simple"},
    "humaneval_simplified-top60": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier-simplified" / "results_score_simplified.json",
        "format": "simple"},
    "xcodeeval_apr": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr" / "python_test_filtered_results.json",
        "format": "nested"},
    "xcodeeval_simplified-top50_apr": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr-simplified" / "python_test_filtered_results.json",
        "format": "nested"},
    "xcodeeval_code_translation": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation" / "python2c_test_filtered_results.json",
        "format": "nested"},
    "xcodeeval_simplified-top50_code_translation": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation-simplified" / "python2c_test_filtered_results.json",
        "format": "nested"}
}

METRICS_TO_ANALYZE = [SummarySchema.LM_CC, SummarySchema.PPL, SummarySchema.LM_CC_DENSITY]
CONTROL_VARIABLE = SummarySchema.LOC


# ==========================================
# 関数定義
# ==========================================
def get_significance_marker(p_val: float) -> str:
    """p値から論文用の有意水準マーカーを返す"""
    if np.isnan(p_val): return ""
    if p_val < 0.001:
        return "***"
    elif p_val < 0.01:
        return "** "
    elif p_val < 0.05:
        return "* "
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


# ==========================================
# 分析コア関数（ご提示の分析手順に準拠）
# ==========================================
def calculate_binned_partial_corr(df: pd.DataFrame, metric: str, score_col: str, control: str, n_bins: int) -> dict:
    """
    ステップ1〜3: 生データをビニングし、代表値を集約してから偏相関の公式に当てはめる
    """
    try:
        df_temp = df[[metric, score_col, control]].dropna().copy()

        # ステップ1: 指標でランク付けし、約10個のグループに分割
        df_temp['group'] = pd.qcut(df_temp[metric], q=n_bins, labels=False, duplicates='drop')

        # ステップ2: グループごとに代表値を算出
        agg_df = df_temp.groupby('group').agg({
            metric: 'median',  # 指標は中央値
            control: 'median',  # 統制変数は中央値
            score_col: 'mean'  # 正答率は平均値
        }).reset_index()

        if len(agg_df) < 4:  # 偏相関は最低4サンプル必要
            return {"r": np.nan, "p": np.nan, "bins": len(agg_df)}

        # ステップ3: 偏相関の計算
        pcorr = pg.partial_corr(data=agg_df, x=metric, y=score_col, covar=control, method='spearman')

        return {"r": pcorr['r'].values[0], "p": pcorr['p-val'].values[0], "bins": len(agg_df)}

    except Exception as e:
        return {"r": np.nan, "p": np.nan, "bins": np.nan}


def calculate_binned_corr(df: pd.DataFrame, metric: str, score_col: str, n_bins: int) -> dict:
    """ゼロ次相関の計算（統制変数なし）"""
    try:
        df_temp = df[[metric, score_col]].dropna().copy()
        df_temp['group'] = pd.qcut(df_temp[metric], q=n_bins, labels=False, duplicates='drop')
        agg_df = df_temp.groupby('group').agg({
            metric: 'median',
            score_col: 'mean'
        }).dropna().reset_index()

        if len(agg_df) < 3:
            return {"r": np.nan, "p": np.nan, "bins": len(agg_df)}

        r, p = spearmanr(agg_df[metric], agg_df[score_col])
        return {"r": r, "p": p, "bins": len(agg_df)}

    except Exception as e:
        return {"r": np.nan, "p": np.nan, "bins": np.nan}


def get_best_result_by_criteria(results: list) -> dict:
    """
    ステップ4: 「統計的に有意（p<0.05）であり、かつ相関係数の絶対値が最も大きいもの」を採用する
    """
    valid_results = [r for r in results if not np.isnan(r["p"])]
    if not valid_results:
        return {"r": np.nan, "p": np.nan, "bins": np.nan}

    # p < 0.05 で有意なものを抽出
    significant_results = [r for r in valid_results if r["p"] < 0.05]

    if significant_results:
        # 有意なものの中で相関係数の「絶対値(abs)」が最大のものを選ぶ
        return max(significant_results, key=lambda x: abs(x["r"]))
    else:
        # 全てが有意でない場合は、参考として最もp値が小さいものを返す
        return min(valid_results, key=lambda x: x["p"])


def calculate_best_binned_partial_corr(df: pd.DataFrame, metric: str, score_col: str, control: str,
                                       n_list: list) -> dict:
    results = []
    for n in n_list:
        res = calculate_binned_partial_corr(df, metric, score_col, control, n_bins=n)
        results.append(res)
    return get_best_result_by_criteria(results)


def calculate_best_binned_corr(df: pd.DataFrame, metric: str, score_col: str, n_list: list) -> dict:
    results = []
    for n in n_list:
        res = calculate_binned_corr(df, metric, score_col, n_bins=n)
        results.append(res)
    return get_best_result_by_criteria(results)


# ==========================================
# メイン処理
# ==========================================
def main():
    df_summary = pd.read_csv(SUMMARY_CSV_PATH)
    datasets = df_summary['dataset'].unique()

    for ds in datasets:
        print(f"\n{'=' * 50}\n📊 データセット: {ds}\n{'=' * 50}")
        if ds not in SCORE_FILES: continue

        scores_dict = load_scores(ds, SCORE_FILES[ds])
        df_ds = df_summary.loc[df_summary['dataset'] == ds].copy()
        df_ds['score'] = df_ds['uid'].map(scores_dict)

        df_ds = df_ds.dropna(subset=['score', CONTROL_VARIABLE])
        print(f"  -> {len(df_ds)} 件のデータで分析を実行します。")

        for metric in METRICS_TO_ANALYZE:
            if metric not in df_ds.columns: continue
            df_target = df_ds.dropna(subset=[metric, 'score', CONTROL_VARIABLE]).copy()
            if len(df_target) < 10: continue

            # 偏相関とゼロ次相関（それぞれ最適なビニング結果を採用）
            partial_corr = calculate_best_binned_partial_corr(df_target, metric, 'score', CONTROL_VARIABLE, [9, 10, 11])
            zero_corr = calculate_best_binned_corr(df_target, metric, 'score', [9, 10, 11])

            print(f"\n  🔹 指標: {metric}")

            if not np.isnan(partial_corr['r']):
                sig = get_significance_marker(partial_corr['p'])
                print(
                    f"     [偏相関]   r = {partial_corr['r']:>7.4f}, p = {partial_corr['p']:.4f} ({sig:^4}) | Bins: {partial_corr['bins']:>2}, Control: {CONTROL_VARIABLE}")
            else:
                print(f"     [偏相関]   計算不可 (データ不足、または多重共線性による数学的エラー)")

            if not np.isnan(zero_corr['r']):
                sig = get_significance_marker(zero_corr['p'])
                print(
                    f"     [ゼロ次相関] r = {zero_corr['r']:>7.4f}, p = {zero_corr['p']:.4f} ({sig:^4}) | Bins: {zero_corr['bins']:>2}")
            else:
                print(f"     [ゼロ次相関] 計算不可 (データ不足等)")


if __name__ == "__main__":
    main()