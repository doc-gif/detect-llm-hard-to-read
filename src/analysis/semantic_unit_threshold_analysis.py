"""semantic_unit の量と LLM 正答率 (pass@1) の関係を調べるスクリプト。

【目的】
仮説「LLM は一定の semantic_unit 量を超えるとキャパシティを超え、
     pass@1 がガクっと落ちる」を確かめる。

【手法】
1. results/summaries/analysis_summary_p80.csv (percentile 80 / token entropy=1.3238
   で絞り込み済みのデータ) を読み込む。
2. dataset ごとに lm-cc プロジェクト側のスコアファイルから pass@1 を取得し、
   uid をキーにマージする。
3. num_semantic_units を bin_size ごとの等幅ビン ([a, b) 区間) に分割し、
   ビンごとに pass@1 の平均値・件数を集計 (度数分布表)。
4. 度数分布表を CSV 出力しつつ、n (サンプル数の棒グラフ) と
   pass@1 平均 (折れ線) を重ねたグラフを画像として保存する。
   -> 急落する箇所があるかどうかは、このグラフを目視で判断する。

このスクリプトは {PROJECT_ROOT}/src/analysis/ 配下に配置することを想定。
{PROJECT_ROOT} は実行環境によらず自動算出する。
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ==========================================
# ⚙️ PROJECT_ROOT の自動算出
# ==========================================
# このファイルは {PROJECT_ROOT}/src/analysis/semantic_unit_threshold_analysis.py
# に配置される想定。parents[2] が PROJECT_ROOT になる。
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]

# lm-cc プロジェクトなど、PROJECT_ROOT の兄弟ディレクトリを参照するための基点
# (correlation_analysis.py の PROJECTS_DIR と同じ考え方)
SIBLING_PROJECTS_DIR = PROJECT_ROOT.parent

# import 解決のため、PROJECT_ROOT と PROJECT_ROOT/src を sys.path に追加しておく
for p in (str(PROJECT_ROOT), str(PROJECT_ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from schema.records import SummarySchema  # noqa: E402  (sys.path 追加後に import)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ==========================================
# ⚙️ 設定エリア
# ==========================================

# 入力: percentile 80 / token entropy=1.3238 で絞り込み済みのサマリーCSV
SUMMARY_CSV_PATH = PROJECT_ROOT / "results" / "summaries" / "analysis_summary_p80.csv"

# pass@1 スコアの取得元 (correlation_analysis.py と同一の3種類のみを対象とする)
SCORE_FILES = {
    "humaneval": {
        "path": SIBLING_PROJECTS_DIR / "lm-cc" / "results" / "humaneval-ier" / "results_score.json",
        "format": "simple",
    },
    "xcodeeval_apr": {
        "path": SIBLING_PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "apr" / "python_test_filtered_results.json",
        "format": "nested",
    },
    "xcodeeval_code_translation": {
        "path": SIBLING_PROJECTS_DIR / "lm-cc" / "results" / "xcodeeval" / "code_translation" / "python2c_test_filtered_results.json",
        "format": "nested",
    },
}

# ビン分けに使う semantic_unit 列 (num_semantic_units)
UNIT_COL = SummarySchema.NUM_SEMANTIC_UNITS
# 参考として持っておく lm_cc 列 (今回のビン分け・グラフには直接使わないが、
# マージ後のCSVには残しておく)
LM_CC_COL = SummarySchema.LM_CC
SCORE_COL = "pass_at_1"  # マージ後に追加する列名

# 試すビン幅 (n) のリスト。ここを書き換えて再実行する想定。
BIN_SIZES = [1, 5, 10]

# 全dataset込みの分析に加え、dataset別の内訳グラフも出すかどうか
PER_DATASET_BREAKDOWN = True

# マージ済みデータ (pass@1付き) をCSVとして保存するか
SAVE_MERGED_CSV = True

# 出力先ディレクトリ
OUTPUT_DIR = PROJECT_ROOT / "results" / "semantic_unit_binning"
TABLE_DIR = OUTPUT_DIR / "tables"
FIGURE_DIR = OUTPUT_DIR / "figures"


# ==========================================
# データ読み込み・マージ
# ==========================================
def load_scores(dataset_name: str, config: dict) -> dict:
    """correlation_analysis.py と同じロジックで pass@1 スコアを読み込む。"""
    path = Path(config["path"])
    if not path.exists():
        logger.warning("スコアファイルが見つかりません (dataset=%s): %s", dataset_name, path)
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    scores: dict = {}
    if config["format"] == "simple":
        # humaneval 形式: { "HumanEval_0__xxx": 1.0, ... }
        for k, v in data.items():
            scores[k.split("__")[0]] = v
    elif config["format"] == "nested":
        # xcodeeval 形式: { "uid": {"pass@1": 0.5, ...}, ... }
        for k, v in data.items():
            scores[k] = v.get("pass@1", 0.0)
    return scores


def load_and_merge_summary(csv_path: Path) -> pd.DataFrame:
    """analysis_summary_p80.csv を読み込み、dataset ごとに pass@1 をマージする。"""
    if not csv_path.exists():
        raise FileNotFoundError(f"サマリーCSVが見つかりません: {csv_path}")

    df = pd.read_csv(csv_path)
    datasets = df[SummarySchema.DATASET].unique()

    merged_frames = []
    for ds in datasets:
        if ds not in SCORE_FILES:
            n_skipped = len(df[df[SummarySchema.DATASET] == ds])
            logger.warning("dataset '%s' は SCORE_FILES に無いためスキップ (%d行)", ds, n_skipped)
            continue

        scores_dict = load_scores(ds, SCORE_FILES[ds])
        df_ds = df.loc[df[SummarySchema.DATASET] == ds].copy()
        df_ds[SCORE_COL] = df_ds[SummarySchema.UID].map(scores_dict)

        n_missing = int(df_ds[SCORE_COL].isna().sum())
        if n_missing:
            logger.warning("dataset '%s': %d行 スコアが見つからず除外", ds, n_missing)
        df_ds = df_ds.dropna(subset=[SCORE_COL])
        merged_frames.append(df_ds)

    if not merged_frames:
        raise RuntimeError("マージできたデータが1件もありません。SCORE_FILES のパスを確認してください。")

    merged = pd.concat(merged_frames, ignore_index=True)
    merged = merged.dropna(subset=[UNIT_COL, SCORE_COL])
    logger.info("マージ後の総件数: %d行 (dataset内訳: %s)",
                len(merged), merged[SummarySchema.DATASET].value_counts().to_dict())
    return merged


# ==========================================
# ビン分け・度数分布表の作成
# ==========================================
def build_frequency_table(df: pd.DataFrame, bin_size: int) -> pd.DataFrame:
    """num_semantic_units を bin_size 幅の [a, b) ビンに分け、
    ビンごとの pass@1 平均・件数などを集計した度数分布表を返す。
    """
    max_val = df[UNIT_COL].max()
    # 右端 [a, b) を確実にカバーするため、max_val を含む次の境界まで edges を用意
    n_bins = int(np.ceil((max_val + 1) / bin_size))
    edges = np.arange(0, (n_bins + 1) * bin_size, bin_size)

    bin_index = pd.cut(df[UNIT_COL], bins=edges, right=False, include_lowest=True)

    grouped = (
        df.groupby(bin_index, observed=True)[SCORE_COL]
        .agg(n="count", pass_at_1_mean="mean", pass_at_1_std="std")
        .reset_index()
        .rename(columns={UNIT_COL: "bin"})
    )

    grouped["bin_start"] = grouped["bin"].apply(lambda iv: iv.left)
    grouped["bin_end"] = grouped["bin"].apply(lambda iv: iv.right)
    grouped = grouped.drop(columns=["bin"])
    grouped = grouped.loc[grouped["n"] > 0].reset_index(drop=True)

    # 参考情報として lm_cc の平均もあわせて記録しておく
    if LM_CC_COL in df.columns:
        lm_cc_index = pd.cut(df[UNIT_COL], bins=edges, right=False, include_lowest=True)
        lm_cc_mean = df.groupby(lm_cc_index, observed=True)[LM_CC_COL].mean().reset_index(drop=True)
        grouped["lm_cc_mean"] = lm_cc_mean

    return grouped[["bin_start", "bin_end", "n", "pass_at_1_mean", "pass_at_1_std", "lm_cc_mean"]]


# ==========================================
# グラフ作成
# ==========================================
def plot_frequency_table(freq_df: pd.DataFrame, bin_size: int, dataset_label: str, output_path: Path) -> None:
    """n (棒グラフ) と pass@1 平均 (折れ線) を重ねたグラフを保存する。"""
    fig, ax1 = plt.subplots(figsize=(max(8, len(freq_df) * 0.5), 6))

    x = np.arange(len(freq_df))
    labels = [f"[{int(r.bin_start)},{int(r.bin_end)})" for r in freq_df.itertuples()]

    ax1.bar(x, freq_df["n"], color="lightgray", alpha=0.7, label="n (sample count)")
    ax1.set_ylabel("n (sample count)")
    ax1.set_xlabel(f"num_semantic_units bin (width={bin_size})")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha="right")

    ax2 = ax1.twinx()
    ax2.plot(x, freq_df["pass_at_1_mean"], color="tab:red", marker="o", linewidth=2, label="pass@1 mean")
    ax2.set_ylabel("pass@1 (mean)")
    ax2.set_ylim(-0.05, 1.05)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    ax1.set_title(f"num_semantic_units vs pass@1 (bin={bin_size}, dataset={dataset_label})")
    fig.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    logger.info("グラフを保存しました: %s", output_path)


# ==========================================
# メイン処理
# ==========================================
def run_for_subset(df: pd.DataFrame, bin_size: int, label: str) -> None:
    if len(df) < 10:
        logger.warning("%s (bin=%d): サンプル数が少なすぎるためスキップ (%d件)", label, bin_size, len(df))
        return

    freq_df = build_frequency_table(df, bin_size)

    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    table_path = TABLE_DIR / f"bin{bin_size}_{label}_freq_table.csv"
    freq_df.to_csv(table_path, index=False)
    logger.info("度数分布表を保存しました: %s", table_path)

    fig_path = FIGURE_DIR / f"bin{bin_size}_{label}_plot.png"
    plot_frequency_table(freq_df, bin_size, label, fig_path)


def main() -> None:
    merged_df = load_and_merge_summary(SUMMARY_CSV_PATH)

    if SAVE_MERGED_CSV:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        merged_csv_path = OUTPUT_DIR / "analysis_summary_p80_with_score.csv"
        merged_df.to_csv(merged_csv_path, index=False)
        logger.info("pass@1付きマージデータを保存しました: %s", merged_csv_path)

    for bin_size in BIN_SIZES:
        # 全dataset込み
        run_for_subset(merged_df, bin_size, label="all")

        # dataset別の内訳
        if PER_DATASET_BREAKDOWN:
            for ds in merged_df[SummarySchema.DATASET].unique():
                df_ds = merged_df.loc[merged_df[SummarySchema.DATASET] == ds]
                run_for_subset(df_ds, bin_size, label=str(ds))


if __name__ == "__main__":
    main()