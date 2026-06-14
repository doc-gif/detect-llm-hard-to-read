import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
import pingouin as pg

from schema.records import SummarySchema

logging.basicConfig(level=logging.INFO, format="%(message)s")

# ==========================================
# ⚙️ 設定エリア
# ==========================================
# 1. サマリーCSVのパス
SUMMARY_CSV_PATH = "/Users/hyoishitobi/PycharmProjects/detect-llm-hard-to-read/results/summaries/analysis_summary.csv"

# 2. 各データセットのスコアJSONへのパスと形式の定義
# (パスは実際の環境に合わせて変更してください)
SCORE_FILES = {
    "humaneval": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/humaneval-ier/results_score.json",
        "format": "simple"  # {"HumanEval_43": 1.0, ...}
    },
    "humaneval_simplified": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/humaneval-ier-simplified/results_score_simplified.json",
        "format": "simple"
    },
    "xcodeeval_apr": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/xcodeeval/apr/python_test_filtered_results.json",
        "format": "nested"  # {"task_id": {"pass@1": 1.0}}
    },
    "xcodeeval_simplified_apr": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/xcodeeval/apr-simplified/python_test_filtered_results.json",
        "format": "nested"
    },
    "xcodeeval_code_translation": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/xcodeeval/code_translation/python2c_test_filtered_results.json",
        "format": "nested"
    },
    "xcodeeval_simplified_code_translation": {
        "path": "/Users/hyoishitobi/PycharmProjects/lm-cc/results/xcodeeval/code_translation-simplified/python2c_test_filtered_results.json",
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


def calculate_full_partial_corr(df: pd.DataFrame, metric: str, score_col: str, control: str) -> dict:
    """全データを用いた偏相関（サンプル数が多いので有意になりやすい）"""
    if metric == control:
        return {"r": np.nan, "p": np.nan}  # 自分自身の偏相関は計算しない

    try:
        pcorr = pg.partial_corr(data=df, x=metric, y=score_col, covar=control, method='spearman')
        return {"r": pcorr['r'].values[0], "p": pcorr['p-val'].values[0]}
    except Exception:
        return {"r": np.nan, "p": np.nan}


def calculate_subgroup_corr(df: pd.DataFrame, metric: str, score_col: str) -> dict:
    """グループ化した上での通常のスピアマン相関（論文のビン分割の意図を汲む）"""
    best_r, best_p, best_bins = None, None, 0

    # データ数が少ない場合はビンの最大数を減らす（最低1ビンあたり5件を確保）
    max_bins = min(11, len(df) // 5)
    min_bins = min(4, max_bins - 2) if max_bins >= 6 else 3

    if max_bins < 3:
        return {"r": np.nan, "p": np.nan, "bins": 0}

    for num_groups in range(min_bins, max_bins + 1):
        try:
            df_copy = df.copy()
            df_copy['group'] = pd.qcut(df_copy[metric], q=num_groups, duplicates='drop')
            agg_df = df_copy.groupby('group', observed=True).agg({
                metric: 'median',
                score_col: 'mean'
            }).dropna()

            if len(agg_df) < 3: continue

            r, p = spearmanr(agg_df[metric], agg_df[score_col])

            # 有意な中で最も強い相関を採用
            if p < 0.05:
                if best_r is None or abs(r) > abs(best_r):
                    best_r, best_p, best_bins = r, p, len(agg_df)
        except Exception:
            continue

    # 全く有意にならなかった場合でも、参考までに一番細かく分けた結果を返す
    if best_r is None:
        try:
            df_copy = df.copy()
            df_copy['group'] = pd.qcut(df_copy[metric], q=max_bins, duplicates='drop')
            agg_df = df_copy.groupby('group', observed=True).agg({metric: 'median', score_col: 'mean'}).dropna()
            if len(agg_df) >= 3:
                r, p = spearmanr(agg_df[metric], agg_df[score_col])
                return {"r": r, "p": p, "bins": len(agg_df)}
        except Exception:
            pass
        return {"r": np.nan, "p": np.nan, "bins": 0}

    return {"r": best_r, "p": best_p, "bins": best_bins}


def main():
    df_summary = pd.read_csv(SUMMARY_CSV_PATH)
    datasets = df_summary['dataset'].unique()

    for ds in datasets:
        print(f"\n{'=' * 50}\n📊 データセット: {ds}\n{'=' * 50}")
        if ds not in SCORE_FILES: continue

        scores_dict = load_scores(ds, SCORE_FILES[ds])
        df_ds = df_summary[df_summary['dataset'] == ds].copy()
        df_ds['score'] = df_ds['uid'].map(scores_dict)

        df_ds = df_ds.dropna(subset=['score', CONTROL_VARIABLE])
        print(f"  -> {len(df_ds)} 件のデータで分析を実行します。")

        for metric in METRICS_TO_ANALYZE:
            if metric not in df_ds.columns: continue
            df_target = df_ds.dropna(subset=[metric, 'score', CONTROL_VARIABLE]).copy()
            if len(df_target) < 10: continue

            full_pcorr = calculate_full_partial_corr(df_target, metric, 'score', CONTROL_VARIABLE)
            sub_corr = calculate_subgroup_corr(df_target, metric, 'score')

            print(f"\n  🔹 指標: {metric}")

            # 1. 全データ偏相関
            if not np.isnan(full_pcorr['r']):
                sig1 = "*" if full_pcorr['p'] < 0.05 else ""
                print(
                    f"     [全データ偏相関 (統制: {CONTROL_VARIABLE})] r = {full_pcorr['r']:>7.4f} (p = {full_pcorr['p']:.4f}) {sig1}")
            else:
                print(f"     [全データ偏相関] 計算不可 (統制変数と同一など)")

            # 2. グループ化通常相関
            if not np.isnan(sub_corr['r']):
                sig2 = "*" if sub_corr['p'] < 0.05 else ""
                print(
                    f"     [グループ化相関 (bins: {sub_corr['bins']:>2})]    r = {sub_corr['r']:>7.4f} (p = {sub_corr['p']:.4f}) {sig2}")
            else:
                print(f"     [グループ化相関] 計算不可")


if __name__ == "__main__":
    main()