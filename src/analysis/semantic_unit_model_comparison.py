"""semantic_unit の量と pass@1 の関係を調べるスクリプト。

【現在のデフォルト動作: 検証ステップ1'.2（目視のみ）】
仮説「Semantic Unitの量が増え一定値を超えると、LLMの回答精度が急に低下するのではないか」
について、データセットごとに Semantic Unit の量を等幅ビン（n=5, 10）に分割し、
ビンごとの pass@1 平均を折れ線グラフとして可視化して目視で傾向を確認する
（run_visual_trend_analysis()、閾値 p67 / p80 × 3データセット × bin幅5,10 の
全組み合わせで図を出力する）。統計的なモデル比較はこの段階のスコープ外。

【将来的に使う場合: AIC/BICによるフルのモデル比較 (run_model_comparison())】
  (A) 区分線形モデル (hinge / broken-stick regression)
      ある breakpoint を境に "なめらかに" 傾きが変わる (真の不連続な崖ではない点に注意)
  (B) ステップ関数モデル (真の崖仮説)
      breakpoint を境に値が不連続にジャンプする
  (C) 滑らかな減衰モデル (4パラメータ・ロジスティック曲線)
      連続的に減衰していく -> 「じわじわ蝕む」仮説に対応

これらを生データ (ビン分けする前の1レコード=1ファイル単位) にフィットし、
AIC / BIC で当てはまりの良さをパラメータ数のペナルティ込みで比較する
(参考として単純な線形回帰もベースラインとして併記)。

このスクリプトは {PROJECT_ROOT}/src/analysis/ 配下に、
semantic_unit_threshold_analysis.py と同じディレクトリに配置することを想定。
(そちらのマージ処理・パス解決ロジックを再利用するため)
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# ==========================================
# semantic_unit_threshold_analysis.py の資産を再利用
# ==========================================
THIS_FILE = Path(__file__).resolve()
if str(THIS_FILE.parent) not in sys.path:
    sys.path.insert(0, str(THIS_FILE.parent))

from semantic_unit_threshold_analysis import (  # noqa: E402
    PROJECT_ROOT,
    SUMMARY_CSV_PATH,
    OUTPUT_DIR,
    UNIT_COL,
    SCORE_COL,
    load_and_merge_summary,
)
from schema.records import SummarySchema  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ==========================================
# ⚙️ 設定エリア
# ==========================================

# semantic_unit_threshold_analysis.py が保存したマージ済みCSV (pass@1付き)
MERGED_CSV_PATH = OUTPUT_DIR / "analysis_summary_p80_with_score.csv"

# dataset別にもモデル比較を行うか (全体1回に加えて)
PER_DATASET_BREAKDOWN = True

# hinge モデルの breakpoint 探索範囲 (外側5%はデータが少なく不安定なので除外)
BREAKPOINT_SEARCH_PERCENTILES = (5, 95)
BREAKPOINT_GRID_SIZE = 300

# 出力先
MODEL_OUTPUT_DIR = PROJECT_ROOT / "results" / "semantic_unit_model_comparison"
TABLE_DIR = MODEL_OUTPUT_DIR / "tables"
FIGURE_DIR = MODEL_OUTPUT_DIR / "figures"

# ロバストネス確認: dataset制御ありの分析について、特定のdatasetを除外しても
# 結論 (曲線構造の要否、hinge vs logisticの優劣) が変わらないかを確認する。
# サンプル数が少なく semantic_unit のレンジも狭い humaneval を除外した場合を試す。
# 空リスト [] にすれば、このロバストネス確認はスキップされる。
ROBUSTNESS_EXCLUDE_DATASETS = ["humaneval"]


# ==========================================
# モデル定義
# ==========================================
def linear_model(x: np.ndarray, a: float, b: float) -> np.ndarray:
    """ベースライン: 単純な線形回帰 (2パラメータ)。"""
    return a + b * x


def hinge_predict(x: np.ndarray, bp: float, a: float, b: float, c: float) -> np.ndarray:
    """区分線形 (broken-stick) モデル。breakpoint で連続的に傾きが変わる。

    y = a + b*x                      (x < bp)
    y = a + b*x + c*(x - bp)         (x >= bp)
    """
    return a + b * x + c * np.maximum(0.0, x - bp)


def logistic4_model(x: np.ndarray, L: float, U: float, k: float, x0: float) -> np.ndarray:
    """滑らかな減衰モデル: 4パラメータ・ロジスティック曲線 (下限L, 上限U, 傾きk, 中点x0)。"""
    return L + (U - L) / (1.0 + np.exp(k * (x - x0)))


def step_predict(x: np.ndarray, bp: float, level_high: float, level_low: float) -> np.ndarray:
    """真の崖仮説: 不連続なステップ関数。
    breakpoint を境に、値が連続的にではなく一気にジャンプする。

    y = level_high   (x < bp)
    y = level_low    (x >= bp)
    """
    return np.where(x < bp, level_high, level_low)


# ==========================================
# フィッティング
# ==========================================
def fit_linear(x: np.ndarray, y: np.ndarray) -> dict:
    coef = np.polyfit(x, y, deg=1)  # [b, a] (numpy の polyfit は高次項から)
    b, a = coef
    y_pred = linear_model(x, a, b)
    rss = float(np.sum((y - y_pred) ** 2))
    return {
        "name": "linear",
        "label": "線形回帰 (ベースライン)",
        "k_params": 2,
        "rss": rss,
        "params": {"a": a, "b": b},
        "predict": lambda xx: linear_model(xx, a, b),
    }


def fit_hinge(x: np.ndarray, y: np.ndarray) -> dict:
    """breakpoint をグリッドサーチし、各候補で最小二乗フィットしてRSS最小のものを採用する。"""
    lo, hi = np.percentile(x, BREAKPOINT_SEARCH_PERCENTILES)
    candidates = np.linspace(lo, hi, BREAKPOINT_GRID_SIZE)

    best = None
    for bp in candidates:
        design = np.column_stack([np.ones_like(x), x, np.maximum(0.0, x - bp)])
        coef, _, _, _ = np.linalg.lstsq(design, y, rcond=None)
        y_pred = design @ coef
        rss = float(np.sum((y - y_pred) ** 2))
        if best is None or rss < best["rss"]:
            a, b, c = coef
            best = {"bp": bp, "a": a, "b": b, "c": c, "rss": rss}

    return {
        "name": "hinge",
        "label": "区分線形モデル (崖仮説・旧版/なめらか)",
        # breakpoint も自由パラメータとしてカウント (a, b, c, bp の4つ)
        "k_params": 4,
        "rss": best["rss"],
        "params": {"breakpoint": best["bp"], "a": best["a"], "b": best["b"], "c": best["c"]},
        "predict": lambda xx: hinge_predict(xx, best["bp"], best["a"], best["b"], best["c"]),
    }


def fit_step(x: np.ndarray, y: np.ndarray) -> dict:
    """真の崖仮説: breakpoint を境に平均値が不連続にジャンプするステップ関数をフィットする。
    区分線形(hinge)モデルと違い、breakpoint の前後で値がなめらかに繋がらない点が本質的に異なる。
    """
    lo, hi = np.percentile(x, BREAKPOINT_SEARCH_PERCENTILES)
    candidates = np.linspace(lo, hi, BREAKPOINT_GRID_SIZE)

    best = None
    for bp in candidates:
        mask_low = x < bp
        mask_high = ~mask_low
        if mask_low.sum() < 2 or mask_high.sum() < 2:
            continue
        level_high = float(np.mean(y[mask_low]))
        level_low = float(np.mean(y[mask_high]))
        y_pred = np.where(mask_low, level_high, level_low)
        rss = float(np.sum((y - y_pred) ** 2))
        if best is None or rss < best["rss"]:
            best = {"bp": bp, "level_high": level_high, "level_low": level_low, "rss": rss}

    if best is None:
        return None

    return {
        "name": "step",
        "label": "ステップ関数モデル (真の崖仮説)",
        "k_params": 3,  # breakpoint, level_high, level_low
        "rss": best["rss"],
        "params": {"breakpoint": best["bp"], "level_high": best["level_high"], "level_low": best["level_low"]},
        "predict": lambda xx: step_predict(xx, best["bp"], best["level_high"], best["level_low"]),
    }


def fit_logistic(x: np.ndarray, y: np.ndarray) -> dict:
    p0 = [max(y.min(), 0.0), min(y.max(), 1.0), 0.1, float(np.median(x))]
    bounds = (
        [-0.5, -0.5, 1e-5, float(x.min())],
        [1.5, 1.5, 10.0, float(x.max())],
    )
    try:
        popt, _ = curve_fit(logistic4_model, x, y, p0=p0, bounds=bounds, maxfev=30000)
    except RuntimeError as e:
        logger.warning("ロジスティックモデルのフィットに失敗しました: %s", e)
        return None

    L, U, k, x0 = popt
    y_pred = logistic4_model(x, *popt)
    rss = float(np.sum((y - y_pred) ** 2))
    return {
        "name": "logistic",
        "label": "滑らかな減衰モデル (浸食仮説)",
        "k_params": 4,
        "rss": rss,
        "params": {"L": L, "U": U, "k": k, "x0": x0},
        "predict": lambda xx: logistic4_model(xx, L, U, k, x0),
    }


# ==========================================
# AIC / BIC 計算
# ==========================================
def compute_aic_bic(rss: float, n: int, k_params: int) -> tuple[float, float]:
    """最小二乗(ガウス誤差)モデルのAIC/BICを計算する。
    ノイズ分散 sigma^2 も推定パラメータの1つとしてカウントする (k_params + 1)。
    """
    if rss <= 0:
        rss = 1e-12
    k_eff = k_params + 1
    aic = n * np.log(rss / n) + 2 * k_eff
    bic = n * np.log(rss / n) + k_eff * np.log(n)
    return float(aic), float(bic)


# ==========================================
# モデル比較の実行
# ==========================================
def compare_models(df: pd.DataFrame, label: str) -> pd.DataFrame:
    x = df[UNIT_COL].to_numpy(dtype=float)
    y = df[SCORE_COL].to_numpy(dtype=float)
    n = len(x)

    fitted = [fit_linear(x, y), fit_hinge(x, y), fit_step(x, y)]
    logistic_fit = fit_logistic(x, y)
    if logistic_fit is not None:
        fitted.append(logistic_fit)

    # グラフの凡例は文字化け防止のため英語表記を使う
    plot_labels = {
        "linear": "linear (baseline)",
        "hinge": "hinge / broken-stick (smooth, NOT a true cliff)",
        "step": "step function (true cliff hypothesis)",
        "logistic": "logistic decay (erosion hypothesis)",
    }
    for m in fitted:
        m["plot_label"] = plot_labels.get(m["name"], m["name"])


    rows = []
    for m in fitted:
        aic, bic = compute_aic_bic(m["rss"], n, m["k_params"])
        rows.append({
            "model": m["name"],
            "label": m["label"],
            "n": n,
            "k_params": m["k_params"],
            "rss": m["rss"],
            "aic": aic,
            "bic": bic,
            "params": m["params"],
        })

    result_df = pd.DataFrame(rows)
    result_df["delta_aic"] = result_df["aic"] - result_df["aic"].min()
    result_df["delta_bic"] = result_df["bic"] - result_df["bic"].min()
    result_df = result_df.sort_values("aic").reset_index(drop=True)

    logger.info("----- %s (n=%d) -----", label, n)
    for _, row in result_df.iterrows():
        logger.info(
            "%-10s  AIC=%.1f (Δ%.1f)  BIC=%.1f (Δ%.1f)  params=%s",
            row["model"], row["aic"], row["delta_aic"], row["bic"], row["delta_bic"], row["params"],
        )
    best = result_df.iloc[0]
    logger.info("=> AIC/BIC 最良モデル: %s (%s)", best["model"], best["label"])
    if best["delta_aic"] > 10 and len(result_df) > 1:
        second = result_df.iloc[1]
        logger.info(
            "   (ΔAIC=%.1f > 10 のため、%s より %s の方が強く支持される)",
            second["delta_aic"], second["model"], best["model"],
        )

    plot_model_comparison(x, y, fitted, label)

    return result_df


def plot_model_comparison(x: np.ndarray, y: np.ndarray, fitted: list, label: str) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))

    # 生データは点が多いので薄い散布図として表示
    ax.scatter(x, y, s=10, alpha=0.15, color="gray", label="raw data")

    x_line = np.linspace(x.min(), x.max(), 400)
    colors = {"linear": "tab:blue", "hinge": "tab:orange", "step": "tab:green", "logistic": "tab:red"}
    for m in fitted:
        y_line = m["predict"](x_line)
        ax.plot(x_line, y_line, color=colors.get(m["name"], "black"), linewidth=2.5, label=m["plot_label"])
        if m["name"] == "hinge":
            ax.axvline(m["params"]["breakpoint"], color=colors["hinge"], linestyle="--", alpha=0.6,
                       label=f"breakpoint(hinge)={m['params']['breakpoint']:.1f}")
        if m["name"] == "step":
            ax.axvline(m["params"]["breakpoint"], color=colors["step"], linestyle="--", alpha=0.6,
                       label=f"breakpoint(step)={m['params']['breakpoint']:.1f}")
        if m["name"] == "logistic":
            ax.axvline(m["params"]["x0"], color=colors["logistic"], linestyle="--", alpha=0.6,
                       label=f"x0(midpoint)={m['params']['x0']:.1f}")

    ax.set_xlabel("num_semantic_units")
    ax.set_ylabel("Accuracy(pass@1)")
    ax.set_ylim(-0.1, 1.1)
    ax.set_title(f"model comparison: linear vs hinge vs step(true cliff) vs logistic - {label}")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIGURE_DIR / f"model_comparison_{label}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info("グラフを保存しました: %s", out_path)


# ==========================================
# dataset切片を制御したモデル (共通の傾き・形状 + dataset別の切片)
# ==========================================
def fit_linear_with_dataset(x: np.ndarray, y: np.ndarray, datasets: pd.Series) -> dict:
    """y = intercept_d + b*x  (傾き b は全dataset共通、切片のみdataset別)"""
    unique_datasets = sorted(pd.unique(datasets))
    dummy_cols = [(datasets == d).astype(float).to_numpy() for d in unique_datasets]
    design = np.column_stack(dummy_cols + [x])
    coef, _, _, _ = np.linalg.lstsq(design, y, rcond=None)
    y_pred = design @ coef
    rss = float(np.sum((y - y_pred) ** 2))

    intercepts = {d: float(coef[i]) for i, d in enumerate(unique_datasets)}
    b = float(coef[-1])

    def predict(xx: np.ndarray, ds: str) -> np.ndarray:
        return intercepts[ds] + b * xx

    return {
        "name": "linear_ds",
        "label": "線形回帰＋dataset切片制御",
        "k_params": len(unique_datasets) + 1,  # 切片(dataset数) + 共通の傾き
        "rss": rss,
        "params": {"intercepts": intercepts, "b": b},
        "predict_by_dataset": predict,
        "datasets": unique_datasets,
    }


def fit_hinge_with_dataset(x: np.ndarray, y: np.ndarray, datasets: pd.Series) -> dict:
    """y = intercept_d + b*x + c*max(0, x-bp)  (b, c, bp は全dataset共通)"""
    unique_datasets = sorted(pd.unique(datasets))
    dummy_cols = [(datasets == d).astype(float).to_numpy() for d in unique_datasets]

    lo, hi = np.percentile(x, BREAKPOINT_SEARCH_PERCENTILES)
    candidates = np.linspace(lo, hi, BREAKPOINT_GRID_SIZE)

    best = None
    for bp in candidates:
        hinge_col = np.maximum(0.0, x - bp)
        design = np.column_stack(dummy_cols + [x, hinge_col])
        coef, _, _, _ = np.linalg.lstsq(design, y, rcond=None)
        y_pred = design @ coef
        rss = float(np.sum((y - y_pred) ** 2))
        if best is None or rss < best["rss"]:
            best = {"bp": bp, "coef": coef, "rss": rss}

    coef = best["coef"]
    n_ds = len(unique_datasets)
    intercepts = {d: float(coef[i]) for i, d in enumerate(unique_datasets)}
    b = float(coef[n_ds])
    c = float(coef[n_ds + 1])
    bp = float(best["bp"])

    def predict(xx: np.ndarray, ds: str) -> np.ndarray:
        return intercepts[ds] + b * xx + c * np.maximum(0.0, xx - bp)

    return {
        "name": "hinge_ds",
        "label": "区分線形モデル＋dataset切片制御 (崖仮説)",
        "k_params": n_ds + 3,  # 切片(dataset数) + b, c, breakpoint
        "rss": best["rss"],
        "params": {"intercepts": intercepts, "b": b, "c": c, "breakpoint": bp},
        "predict_by_dataset": predict,
        "datasets": unique_datasets,
    }


def fit_logistic_with_dataset(x: np.ndarray, y: np.ndarray, datasets: pd.Series) -> dict | None:
    """y = logistic4(x; L,U,k,x0) + shift_d  (曲線の形状 L,U,k,x0 は全dataset共通、
    dataset間のベースラインの差だけを shift_d で吸収する)。
    reference dataset (辞書順で最初) の shift は 0 に固定する。
    """
    unique_datasets = sorted(pd.unique(datasets))
    reference = unique_datasets[0]
    others = unique_datasets[1:]
    dataset_idx = pd.Categorical(datasets, categories=unique_datasets).codes  # reference=0

    def model(x_and_idx, L, U, k, x0, *gammas):
        xv, idx = x_and_idx
        idx = idx.astype(int)
        base = L + (U - L) / (1.0 + np.exp(k * (xv - x0)))
        shift = np.zeros_like(xv, dtype=float)
        for i, g in enumerate(gammas):
            shift = shift + g * (idx == (i + 1))
        return base + shift

    n_gamma = len(others)
    p0 = [max(y.min(), 0.0), min(y.max(), 1.0), 0.1, float(np.median(x))] + [0.0] * n_gamma
    lower = [-0.5, -0.5, 1e-5, float(x.min())] + [-1.0] * n_gamma
    upper = [1.5, 1.5, 10.0, float(x.max())] + [1.0] * n_gamma

    try:
        popt, _ = curve_fit(
            model, (x, dataset_idx), y, p0=p0, bounds=(lower, upper), maxfev=50000
        )
    except RuntimeError as e:
        logger.warning("dataset制御ロジスティックモデルのフィットに失敗しました: %s", e)
        return None

    L, U, k, x0 = popt[:4]
    gammas = popt[4:]
    y_pred = model((x, dataset_idx), *popt)
    rss = float(np.sum((y - y_pred) ** 2))

    shifts = {reference: 0.0}
    for d, g in zip(others, gammas):
        shifts[d] = float(g)

    def predict(xx: np.ndarray, ds: str) -> np.ndarray:
        base = L + (U - L) / (1.0 + np.exp(k * (xx - x0)))
        return base + shifts[ds]

    return {
        "name": "logistic_ds",
        "label": "滑らかな減衰モデル＋dataset切片制御 (浸食仮説)",
        "k_params": 4 + n_gamma,  # L,U,k,x0 + dataset間シフト(reference除く)
        "rss": rss,
        "params": {"L": float(L), "U": float(U), "k": float(k), "x0": float(x0), "shifts": shifts},
        "predict_by_dataset": predict,
        "datasets": unique_datasets,
    }


# ==========================================
# dataset制御モデルの比較・プロット
# ==========================================
def compare_models_with_dataset_control(
    df: pd.DataFrame, scope_label: str = "all", fig_suffix: str = "all"
) -> pd.DataFrame:
    x = df[UNIT_COL].to_numpy(dtype=float)
    y = df[SCORE_COL].to_numpy(dtype=float)
    datasets = df[SummarySchema.DATASET]
    n = len(x)

    fitted = [
        fit_linear_with_dataset(x, y, datasets),
        fit_hinge_with_dataset(x, y, datasets),
    ]
    logistic_fit = fit_logistic_with_dataset(x, y, datasets)
    if logistic_fit is not None:
        fitted.append(logistic_fit)

    plot_labels = {
        "linear_ds": "linear + dataset intercepts (baseline)",
        "hinge_ds": "hinge + dataset intercepts (cliff hypothesis)",
        "logistic_ds": "logistic + dataset shift (erosion hypothesis)",
    }
    for m in fitted:
        m["plot_label"] = plot_labels.get(m["name"], m["name"])

    rows = []
    for m in fitted:
        aic, bic = compute_aic_bic(m["rss"], n, m["k_params"])
        rows.append({
            "model": m["name"],
            "label": m["label"],
            "n": n,
            "k_params": m["k_params"],
            "rss": m["rss"],
            "aic": aic,
            "bic": bic,
            "params": m["params"],
        })

    result_df = pd.DataFrame(rows)
    result_df["delta_aic"] = result_df["aic"] - result_df["aic"].min()
    result_df["delta_bic"] = result_df["bic"] - result_df["bic"].min()
    result_df = result_df.sort_values("aic").reset_index(drop=True)

    logger.info("----- dataset切片制御あり: %s (n=%d, datasets=%s) -----",
                scope_label, n, sorted(datasets.unique()))
    for _, row in result_df.iterrows():
        logger.info(
            "%-14s  AIC=%.1f (Δ%.1f)  BIC=%.1f (Δ%.1f)  params=%s",
            row["model"], row["aic"], row["delta_aic"], row["bic"], row["delta_bic"], row["params"],
        )
    best = result_df.iloc[0]
    logger.info("=> AIC/BIC 最良モデル (dataset制御あり, %s): %s (%s)", scope_label, best["model"], best["label"])
    if best["delta_aic"] > 10 and len(result_df) > 1:
        second = result_df.iloc[1]
        logger.info(
            "   (ΔAIC=%.1f > 10 のため、%s より %s の方が強く支持される)",
            second["delta_aic"], second["model"], best["model"],
        )
    elif len(result_df) > 1:
        second = result_df.iloc[1]
        logger.info(
            "   (ΔAIC=%.1f <= 10 のため、%s と %s は統計的にほぼ同格)",
            second["delta_aic"], second["model"], best["model"],
        )

    plot_dataset_controlled_comparison(df, fitted, fig_suffix=fig_suffix)

    return result_df


def plot_dataset_controlled_comparison(df: pd.DataFrame, fitted: list, fig_suffix: str = "all") -> None:
    unique_datasets = fitted[0]["datasets"]
    fig, axes = plt.subplots(1, len(unique_datasets), figsize=(6 * len(unique_datasets), 5), sharey=True)
    if len(unique_datasets) == 1:
        axes = [axes]

    colors = {"linear_ds": "tab:blue", "hinge_ds": "tab:orange", "logistic_ds": "tab:red"}

    for ax, ds in zip(axes, unique_datasets):
        df_ds = df.loc[df[SummarySchema.DATASET] == ds]
        x_ds = df_ds[UNIT_COL].to_numpy(dtype=float)
        y_ds = df_ds[SCORE_COL].to_numpy(dtype=float)
        ax.scatter(x_ds, y_ds, s=10, alpha=0.15, color="gray", label="raw data")

        x_line = np.linspace(x_ds.min(), x_ds.max(), 300)
        for m in fitted:
            y_line = m["predict_by_dataset"](x_line, ds)
            ax.plot(x_line, y_line, color=colors.get(m["name"], "black"), linewidth=2.2, label=m["plot_label"])

        ax.set_title(str(ds))
        ax.set_xlabel("num_semantic_units")
        ax.set_ylim(-0.1, 1.1)

    axes[0].set_ylabel("Accuracy(pass@1)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=9, bbox_to_anchor=(0.5, -0.05))
    fig.suptitle("dataset-controlled model comparison (shared shape, per-dataset intercept)")
    fig.tight_layout()

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIGURE_DIR / f"model_comparison_dataset_controlled_{fig_suffix}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("グラフを保存しました: %s", out_path)


# ==========================================
# メイン処理: AIC/BIC モデル比較 (フル版。現在は 1'.2 のスコープ外だが将来使えるよう保持)
# ==========================================
def run_model_comparison() -> None:
    if MERGED_CSV_PATH.exists():
        logger.info("マージ済みキャッシュを読み込みます: %s", MERGED_CSV_PATH)
        df = pd.read_csv(MERGED_CSV_PATH)
    else:
        logger.info("マージ済みキャッシュが無いため、summary CSV から再マージします。")
        df = load_and_merge_summary(SUMMARY_CSV_PATH)

    df = df.dropna(subset=[UNIT_COL, SCORE_COL])

    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    all_results = []

    result_all = compare_models(df, "all")
    result_all.insert(0, "scope", "all")
    all_results.append(result_all)

    if PER_DATASET_BREAKDOWN:
        for ds in df[SummarySchema.DATASET].unique():
            df_ds = df.loc[df[SummarySchema.DATASET] == ds]
            if len(df_ds) < 30:
                logger.warning("dataset '%s' はサンプル数が少なすぎるためスキップ (%d件)", ds, len(df_ds))
                continue
            result_ds = compare_models(df_ds, str(ds))
            result_ds.insert(0, "scope", str(ds))
            all_results.append(result_ds)

    # dataset間の切片差 (難易度ベースラインの違い) を制御した上での比較 (全dataset)
    result_controlled = compare_models_with_dataset_control(df, scope_label="all", fig_suffix="all")
    result_controlled.insert(0, "scope", "all_dataset_controlled")
    all_results.append(result_controlled)

    # ロバストネス確認: 特定のdatasetを除外しても結論が変わらないか
    if ROBUSTNESS_EXCLUDE_DATASETS:
        df_robust = df.loc[~df[SummarySchema.DATASET].isin(ROBUSTNESS_EXCLUDE_DATASETS)]
        remaining_datasets = df_robust[SummarySchema.DATASET].unique()
        if len(df_robust) >= 30 and len(remaining_datasets) >= 2:
            excl_label = "excl_" + "_".join(ROBUSTNESS_EXCLUDE_DATASETS)
            logger.info("ロバストネス確認: %s を除外して再フィット (残り%d件, datasets=%s)",
                        ROBUSTNESS_EXCLUDE_DATASETS, len(df_robust), sorted(remaining_datasets))
            result_robust = compare_models_with_dataset_control(
                df_robust, scope_label=excl_label, fig_suffix=excl_label
            )
            result_robust.insert(0, "scope", f"dataset_controlled_{excl_label}")
            all_results.append(result_robust)
        else:
            logger.warning(
                "ロバストネス確認をスキップ: 除外後のデータが不十分 (%d件, dataset数=%d)",
                len(df_robust), len(remaining_datasets),
            )

    combined = pd.concat(all_results, ignore_index=True)
    combined_out = combined.copy()
    # params は辞書なので、CSVには文字列化して残す (完全に消さず参照できるようにする)
    combined_out["params"] = combined_out["params"].apply(str)
    table_path = TABLE_DIR / "model_comparison_summary.csv"
    combined_out.to_csv(table_path, index=False)
    logger.info("比較結果テーブルを保存しました: %s", table_path)


# ==========================================
# メイン処理: 検証ステップ1'.2 (目視のみ) 用のビン分けトレンド可視化
# ==========================================
# 検証ステップ1'.2: Semantic Unitの量が増え一定値を超えると、
#                   LLMの回答精度が急に低下するのではないか。
# 検証アプローチ: データセットごとに Semantic Unit の量をビン分けし、
#                 ビンごとの pass@1 平均を折れ線グラフで可視化して目視で傾向を確認する。
#                 (統計的なモデル比較は行わない。AIC/BICでの検証は run_model_comparison() 側で扱う)

# Semantic Unit / LM-CC の算出に使うトークンエントロピー閾値 (percentile)。
# [1] LM-CC 提唱論文 (Xie et al., 2026) のデフォルト設定 p67
# [2] LM-CC が Semantic Unit の概念で参考にした論文の設定 p80
VISUAL_SUMMARY_CSV_PATHS = {
    "p67": PROJECT_ROOT / "results" / "summaries" / "analysis_summary_p67.csv",
    "p80": PROJECT_ROOT / "results" / "summaries" / "analysis_summary_p80.csv",
}

# 対象データセット (タスクの種類が異なるため、pool せずデータセットごとに個別で見る)
VISUAL_DATASETS = ["humaneval", "xcodeeval_apr", "xcodeeval_code_translation"]

# ビン分けの基準 (Semantic Unit 分布を n ごとの等幅ビンに分割する)
VISUAL_BIN_SIZES = [5, 10]

VISUAL_OUTPUT_DIR = PROJECT_ROOT / "results" / "semantic_unit_visual_trend"
VISUAL_FIGURE_DIR = VISUAL_OUTPUT_DIR / "figures"


def compute_bin_trend(x: np.ndarray, y: np.ndarray, bin_size: int) -> pd.DataFrame:
    """num_semantic_units を bin_size 幅の等幅ビンに分け、ビンごとの pass@1 平均・件数を返す。
    (縦軸=サンプル数 n ではなく、縦軸=pass@1平均・横軸=semantic_unit を可視化する目的専用)
    """
    max_val = float(np.max(x))
    n_bins = int(np.ceil((max_val + 1) / bin_size))
    edges = np.arange(0, (n_bins + 1) * bin_size, bin_size)

    bin_index = pd.cut(x, bins=edges, right=False, include_lowest=True)
    tmp = pd.DataFrame({"bin": bin_index, "y": y})
    grouped = tmp.groupby("bin", observed=True)["y"].agg(n="count", pass_at_1_mean="mean").reset_index()
    grouped["bin_mid"] = grouped["bin"].apply(lambda iv: (iv.left + iv.right) / 2.0)
    grouped = grouped.loc[grouped["n"] > 0].sort_values("bin_mid").reset_index(drop=True)
    return grouped[["bin_mid", "n", "pass_at_1_mean"]]


def plot_visual_trend(df: pd.DataFrame, bin_size: int, threshold_label: str, dataset_label: str) -> None:
    x = df[UNIT_COL].to_numpy(dtype=float)
    y = df[SCORE_COL].to_numpy(dtype=float)

    trend = compute_bin_trend(x, y, bin_size)

    fig, ax = plt.subplots(figsize=(8, 5.5))

    # 生データはうっすらと散布図で背景に表示するのみ (主役はビンごとの平均の折れ線)
    ax.scatter(x, y, s=14, alpha=0.12, color="gray", label="raw data (Accuracy(pass@1) per file)")

    # ビンごとの Accuracy(pass@1) 平均の折れ線 (これが今回見たい主役)
    ax.plot(trend["bin_mid"], trend["pass_at_1_mean"], color="tab:red", linewidth=2.5,
             marker="o", markersize=5, label=f"Accuracy(pass@1) mean per bin (width={bin_size})")

    ax.set_xlabel("num_semantic_units")
    ax.set_ylabel("Accuracy(pass@1)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title(f"{dataset_label} | threshold={threshold_label} | bin width={bin_size}")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()

    VISUAL_FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = VISUAL_FIGURE_DIR / f"trend_{threshold_label}_{dataset_label}_bin{bin_size}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info("グラフを保存しました: %s", out_path)


def run_visual_trend_analysis() -> None:
    for threshold_label, csv_path in VISUAL_SUMMARY_CSV_PATHS.items():
        if not csv_path.exists():
            logger.warning("閾値 %s のサマリーCSVが見つからないためスキップ: %s", threshold_label, csv_path)
            continue

        logger.info("===== threshold=%s のデータを読み込み中 (%s) =====", threshold_label, csv_path)
        merged = load_and_merge_summary(csv_path)
        merged = merged.dropna(subset=[UNIT_COL, SCORE_COL])

        # 1. データセットごとのプロット
        for ds in VISUAL_DATASETS:
            df_ds = merged.loc[merged[SummarySchema.DATASET] == ds]
            if len(df_ds) < 10:
                logger.warning("threshold=%s, dataset=%s はサンプル数が少なすぎるためスキップ (%d件)",
                               threshold_label, ds, len(df_ds))
                continue
            for bin_size in VISUAL_BIN_SIZES:
                plot_visual_trend(df_ds, bin_size, threshold_label, ds)

        # 2. 全データセット合算 (ALL) のプロットを追加
        logger.info("===== threshold=%s, dataset=ALL (合算) の処理 =====", threshold_label)
        if len(merged) >= 10:
            for bin_size in VISUAL_BIN_SIZES:
                plot_visual_trend(merged, bin_size, threshold_label, "ALL_datasets")


if __name__ == "__main__":
    # 検証ステップ1'.2 (目視のみ) のためのビン分けトレンド可視化。
    # AIC/BICによるフルのモデル比較を行いたい場合は run_model_comparison() を呼び出す。
    run_visual_trend_analysis()
    # run_model_comparison()