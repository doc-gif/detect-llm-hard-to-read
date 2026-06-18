import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
import pingouin as pg
from scipy import stats
import warnings

from schema.records import SummarySchema

logging.basicConfig(level=logging.INFO, format="%(message)s")

warnings.filterwarnings("ignore", message="The covariance matrix is rank-deficient")

# ==========================================
# ⚙️ 設定エリア
# ==========================================
PROJECTS_DIR = Path(__file__).resolve().parent.parent.parent.parent
SUMMARY_CSV_PATH = PROJECTS_DIR / "detect-llm-hard-to-read" / "results" / "summaries" / "analysis_summary.csv"

SCORE_FILES = {
    # "humaneval": {"path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier" / "results_score.json",
    #               "format": "simple"},
    "humaneval_simplified-top60": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier-simplified" / "results_score_simplified.json",
        "format": "simple"},
    # "xcodeeval_apr": {
    #     "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr" / "python_test_filtered_results.json",
    #     "format": "nested"},
    "xcodeeval_simplified-top50_apr": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr-simplified" / "python_test_filtered_results.json",
        "format": "nested"},
    # "xcodeeval_code_translation": {
    #     "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation" / "python2c_test_filtered_results.json",
    #     "format": "nested"},
    "xcodeeval_simplified-top50_code_translation": {
        "path": PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation-simplified" / "python2c_test_filtered_results.json",
        "format": "nested"}
}

METRICS_TO_ANALYZE = [SummarySchema.LM_CC, SummarySchema.PPL, SummarySchema.LM_CC_DENSITY]
CONTROL_VARIABLE = SummarySchema.LOC


# ==========================================
# 共通関数
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
# 先行研究のコアアルゴリズムの実装
# ==========================================
def group_by_metric(score, metric, loc, min_cnt):
    """先行研究のビニング手法（指定した最小データ数 min_cnt を担保しながらグループ化）"""
    score = np.asarray(score)
    metric = np.asarray(metric)
    loc_sorted = None
    if loc is not None:
        loc = np.asarray(loc)

    idx = np.argsort(metric)
    score_sorted = score[idx]
    metric_sorted = metric[idx]
    if loc is not None:
        loc_sorted = loc[idx]

    n = len(score)
    groups = []
    start = 0
    while start < n:
        end = start + 1
        while end < n and (end - start) < min_cnt:
            end += 1
        while end < n and (end - start) < min_cnt:  # 原本の謎の2重ループを踏襲
            end += 1
        groups.append((start, end))
        start = end

    mean_scores, mean_metrics, counts = [], [], []
    mean_locs = [] if loc is not None else None

    for s, e in groups:
        mean_scores.append(np.nanmean(score_sorted[s:e]))
        mean_metrics.append(np.nanmedian(metric_sorted[s:e]))
        counts.append(e - s)
        if loc is not None:
            mean_locs.append(np.nanmedian(loc_sorted[s:e]))

    if mean_locs is not None:
        results = list(zip(mean_scores, mean_locs, mean_metrics, counts))
        results_sorted = sorted(results, key=lambda x: (x[2], -x[0]))
        mean_scores, mean_locs, mean_metrics, counts = map(list, zip(*results_sorted))
    else:
        results = list(zip(mean_scores, mean_metrics, counts))
        results_sorted = sorted(results, key=lambda x: (x[1], -x[0]))
        mean_scores, mean_metrics, counts = map(list, zip(*results_sorted))

    return mean_scores, mean_locs, mean_metrics, counts


def partial_by_residuals_rp(xv, yv, zv):
    """pingouinが多重共線性で落ちた場合の緊急回避用（残差での手計算）"""
    xv, yv, zv = stats.rankdata(xv), stats.rankdata(yv), stats.rankdata(zv)
    if np.allclose(zv, zv[0]):
        return np.nan, np.nan
    coef_x = np.polyfit(zv, xv, 1)
    resid_x = xv - (coef_x[0] * zv + coef_x[1])
    coef_y = np.polyfit(zv, yv, 1)
    resid_y = yv - (coef_y[0] * zv + coef_y[1])
    if resid_x.size < 2:
        return np.nan, np.nan
    try:
        r, p = stats.pearsonr(resid_x, resid_y)
        return float(r), float(p)
    except Exception:
        return np.nan, np.nan


def calculate_single_correlation(score, metric, loc=None, min_cnt=10):
    """1つの min_cnt パターンで相関（または偏相関）を計算する"""
    mean_scores, mean_locs, mean_metrics, counts = group_by_metric(score, metric, loc, min_cnt)

    ms_arr = np.array(mean_scores)
    mm_arr = np.array(mean_metrics)
    counts_arr = np.array(counts, dtype=int)

    if loc is not None:
        ml_arr = np.array(mean_locs)
        base_mask = ~(np.isnan(ms_arr) | np.isnan(ml_arr) | np.isnan(mm_arr))
    else:
        base_mask = ~(np.isnan(ms_arr) | np.isnan(mm_arr))

    valid_mask = base_mask & (counts_arr >= min_cnt)
    valid_count = int(np.count_nonzero(valid_mask))

    spearman_r = spearman_p = r_mc = np.nan  # r_mc (多重共線性チェック用) を追加

    if valid_count >= 2:
        x, y = mm_arr[valid_mask], ms_arr[valid_mask]
        if loc is None:
            try:
                sr = stats.spearmanr(x, y)
                spearman_r = float(sr.correlation) if hasattr(sr, 'correlation') else float(sr[0])
                spearman_p = float(sr.pvalue) if hasattr(sr, 'pvalue') else float(sr[1])
            except Exception:
                pass
        else:
            z = ml_arr[valid_mask]

            # --- 💡 追加: 指標(x)と統制変数(z)の相関を計算 ---
            try:
                sr_mc = stats.spearmanr(x, z)
                r_mc = float(sr_mc.correlation) if hasattr(sr_mc, 'correlation') else float(sr_mc[0])
            except Exception:
                pass
            # ------------------------------------------------

            df_temp = pd.DataFrame({"mean_metric": x, "mean_score": y, "mean_loc": z})
            try:
                spearman = pg.partial_corr(data=df_temp, x='mean_metric', y='mean_score', covar='mean_loc',
                                           method='spearman')
                spearman_r = float(spearman['r'].iloc[0])
                spearman_p = float(spearman['p-val'].iloc[0])
            except Exception:
                spearman_r, spearman_p = partial_by_residuals_rp(x, y, z)

    # 戻り値に r_mc を追加
    return {"r": spearman_r, "p": spearman_p, "bins": valid_count, "min_cnt": min_cnt, "r_mc": r_mc}


def search_best_correlation(score, metric, loc=None):
    """
    先行研究に準拠したループ探索：
    1. min_cnt を N//20 から N//8 まで変化させて全て試す
    2. グループ数が 9〜11 (8 < groups < 12) で、負の相関 (r < 0) かつ有意 (p < 0.05) なものを探す
    3. 複数あれば絶対値 |r| が最大のものを採用
    """
    best_result = {"r": np.nan, "p": np.nan, "bins": np.nan, "min_cnt": np.nan, "r_mc": np.nan}
    max_abs_r = -1
    n_samples = len(score)

    # 探索範囲
    min_min_cnt = max(1, n_samples // 20)
    max_min_cnt = max(1, n_samples // 8)

    valid_results = []

    for min_cnt in range(min_min_cnt, max_min_cnt + 1):
        res = calculate_single_correlation(score, metric, loc, min_cnt)
        r, p, valid_groups = res["r"], res["p"], res["bins"]

        if not np.isnan(p):
            valid_results.append(res)
            # 先行研究のフィルタリング条件
            if 8 < valid_groups < 12 and r < 0 and p < 0.05:
                if abs(r) > max_abs_r:
                    max_abs_r = abs(r)
                    best_result = res

    # フィルタを通過する完璧な結果がなかった場合、一番 p値 が小さいものを妥協して返す
    if np.isnan(best_result["p"]) and valid_results:
        best_result = min(valid_results, key=lambda x: x["p"])

    return best_result


# ==========================================
# メイン処理
# ==========================================
def main():
    df_summary = pd.read_csv(SUMMARY_CSV_PATH)
    datasets = df_summary['dataset'].unique()

    for ds in datasets:
        print(f"\n{'=' * 70}\n📊 データセット: {ds}\n{'=' * 70}")
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

            # データ配列の抽出
            score_arr = df_target['score'].values
            metric_arr = df_target[metric].values
            loc_arr = df_target[CONTROL_VARIABLE].values

            # 先行研究の手法で最適な偏相関とゼロ次相関を探索
            partial_corr = search_best_correlation(score_arr, metric_arr, loc=loc_arr)
            zero_corr = search_best_correlation(score_arr, metric_arr, loc=None)

            print(f"\n  🔹 指標: {metric}")

            if not np.isnan(partial_corr['r']):
                sig = get_significance_marker(partial_corr['p'])

                # 多重共線性の警告メッセージを生成
                mc_warning = ""
                r_mc_val = partial_corr.get('r_mc')
                if not np.isnan(r_mc_val) and abs(r_mc_val) >= 0.90:
                    mc_warning = f" | ⚠️ 多重共線性の疑い(r_mc={r_mc_val:.2f})"

                print(
                    f"     [偏相関]   r = {partial_corr['r']:>7.4f}, p = {partial_corr['p']:.4f} ({sig:^4}) | Bins: {partial_corr['bins']:>2}, min_cnt: {partial_corr['min_cnt']:>2}, Control: {CONTROL_VARIABLE}")
            else:
                print(f"     [偏相関]   計算不可")

            if not np.isnan(zero_corr['r']):
                sig = get_significance_marker(zero_corr['p'])
                print(
                    f"     [ゼロ次相関] r = {zero_corr['r']:>7.4f}, p = {zero_corr['p']:.4f} ({sig:^4}) | Bins: {zero_corr['bins']:>2}, min_cnt: {zero_corr['min_cnt']:>2}")
            else:
                print(f"     [ゼロ次相関] 計算不可")


if __name__ == "__main__":
    main()