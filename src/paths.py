"""プロジェクト内のパスを一元管理するモジュール。

各スクリプトはここで定義した定数を参照する。ディレクトリ構成を変えるときは
このファイルだけを直せばよい。

環境変数:
    LM_CC_ROOT: 先行研究リポジトリ (lm-cc) のパス。未設定ならこのリポジトリと
        同じ親ディレクトリにある ``lm-cc`` を使う。
"""
from __future__ import annotations

import os
from pathlib import Path

#: リポジトリのルート (``src/`` の親)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

#: Phase 1 の入力となるソースコード
DATA_DIR = PROJECT_ROOT / "data"
#: Phase 1 の出力 (トークン単位の Parquet)
OUT_DIR = PROJECT_ROOT / "out"
#: Phase 2 以降の出力
RESULTS_DIR = PROJECT_ROOT / "results"

ENRICHED_DIR = RESULTS_DIR / "enriched"
SUMMARIES_DIR = RESULTS_DIR / "summaries"
PLOTS_DIR = RESULTS_DIR / "plots"
EXTRACTED_GROUPS_DIR = RESULTS_DIR / "extracted_groups"
EXPERIMENTS_DIR = RESULTS_DIR / "experiments"
BLOCK_TREES_DIR = RESULTS_DIR / "block_trees"
TOKEN_ANALYSIS_DIR = RESULTS_DIR / "token_analysis"

#: 先行研究 lm-cc リポジトリ (pass@1 スコアやエントロピーの参照元)
LM_CC_ROOT = Path(os.environ.get("LM_CC_ROOT", PROJECT_ROOT.parent / "lm-cc")).expanduser()
LM_CC_RESULTS_DIR = LM_CC_ROOT / "results"


def summary_csv(suffix: str = "") -> Path:
    """``results/summaries/analysis_summary{suffix}.csv`` のパスを返す。

    例: ``summary_csv("_p67")`` -> ``.../analysis_summary_p67.csv``
    """
    return SUMMARIES_DIR / f"analysis_summary{suffix}.csv"


def resolve_data_path(path_str: str) -> Path:
    """Parquet の ``meta_file`` に記録されたソースパスを、この環境のパスに解決する。

    ``meta_file`` は Phase 1 実行時の絶対パス (例: 別マシンの
    ``/Users/.../detect-llm-hard-to-read/data/humaneval/HumanEval_0.py``) なので、
    リポジトリを移動したり別マシンで分析したりすると見つからない。
    そのまま存在すればそれを、無ければパス中の最後の ``data`` 以降を
    :data:`DATA_DIR` 配下に付け替えたパスを返す。
    """
    path = Path(path_str)
    if path.exists():
        return path
    parts = path.parts
    if "data" in parts:
        idx = len(parts) - 1 - parts[::-1].index("data")
        candidate = DATA_DIR.joinpath(*parts[idx + 1:])
        if candidate.exists():
            return candidate
    return path
