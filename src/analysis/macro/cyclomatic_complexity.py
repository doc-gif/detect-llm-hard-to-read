# src/analysis/macro/cyclomatic_complexity.py
"""Cyclomatic Complexity（循環的複雑度）マクロ指標。

Lizard (https://github.com/terryyin/lizard) を使用する。Lizard は
C/C++/Java/Python/JS など多言語に対応した軽量な複雑度解析ツール。

`meta_file`（Phase 1 の `ParquetWriter` が全行に埋め込む、元ソースファイルの
絶対パス）から元ファイルをそのまま読み込んで解析するため、トークンからの
再構築は行わない。ファイル拡張子がそのまま使えるので、対象言語が Python
以外に広がっても自動的に対応できる。
"""
from __future__ import annotations

import logging
from typing import List, Optional

import lizard
import pandas as pd

from macro.complexity_helper.source_reconstruction import load_source_from_meta

logger = logging.getLogger(__name__)

# meta_file が無い/読み込めない場合のフォールバック用仮想ファイル名。
DEFAULT_VIRTUAL_FILENAME = "snippet.py"

_VALID_AGGREGATIONS = ("sum", "mean", "max")


def _wrap_as_virtual_function(source_code: str, filename: str) -> str:
    """スクリプト全体を、Lizardが解析できるように仮想関数でラップする。"""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext in ("py", "py3", "pyw") or filename == DEFAULT_VIRTUAL_FILENAME:
        # Python: 各行を4スペースでインデントし、冒頭にラッパー関数を付与する
        indented_lines = [f"    {line}" if line.strip() else line for line in source_code.splitlines()]
        return "def __virtual_wrapper__():\n" + "\n".join(indented_lines)
    elif ext in ("rb",):
        # Ruby
        return f"def __virtual_wrapper__\n{source_code}\nend"
    else:
        # C/C++/Java/JS/TS/Rust/C# など、中括弧を使用する言語向け
        return f"void __virtual_wrapper__() {{\n{source_code}\n}}"


def _aggregate(values: List[int], aggregation: str) -> float:
    """指定された集約方法でスコアを計算する。"""
    if not values:
        return 0.0
    if aggregation == "mean":
        return float(sum(values)) / len(values)
    if aggregation == "max":
        return float(max(values))
    return float(sum(values))


def calculate(
        token_df: pd.DataFrame,
        source_code: Optional[str] = None,
        filename: Optional[str] = None,
        aggregation: str = "sum",
) -> Optional[float]:
    """Cyclomatic Complexity を算出する。

    Args:
        token_df: `meta_file` 列を含むトークン単位の DataFrame。
        source_code: 既にソースコード文字列を持っている場合はここに渡すと、
            `meta_file` からの読み込みをスキップできる（テスト・将来の拡張用）。
        filename: 言語判定用のファイル名（拡張子で対象言語が決まる）。
            省略時は `meta_file` の実際のファイル名を使う。
        aggregation: ファイル内に複数関数がある場合の集約方法。
            - "sum"  (既定): 全関数の CCN の合計
            - "mean": 全関数の CCN の平均
            - "max" : 最も複雑な関数の CCN

    Returns:
        算出した Cyclomatic Complexity。算出できない場合は None。
    """
    if aggregation not in _VALID_AGGREGATIONS:
        raise ValueError(f"aggregation must be one of {_VALID_AGGREGATIONS}, got: {aggregation!r}")

    if source_code is None:
        loaded = load_source_from_meta(token_df)
        if loaded is None:
            logger.warning("Cyclomatic complexity calculation skipped: original source file not found.")
            return None
        source_code, source_path = loaded
        if filename is None:
            filename = source_path.name  # 実際の拡張子を使い、Lizardに言語を自動判定させる

    if filename is None:
        filename = DEFAULT_VIRTUAL_FILENAME

    if not source_code or not source_code.strip():
        logger.warning("Cyclomatic complexity calculation skipped: source file is empty.")
        return None

    try:
        # 1. 通常のソースコードをそのまま解析
        analysis_normal = lizard.analyze_file.analyze_source_code(filename, source_code)
        ccn_values_normal: List[int] = [f.cyclomatic_complexity for f in analysis_normal.function_list]
        ccn_normal = _aggregate(ccn_values_normal, aggregation)

        # 2. 必ずスクリプト全体を仮想関数としてラップしたコードも裏で解析
        wrapped_code = _wrap_as_virtual_function(source_code, filename)
        analysis_wrapped = lizard.analyze_file.analyze_source_code(filename, wrapped_code)
        ccn_values_wrapped: List[int] = [f.cyclomatic_complexity for f in analysis_wrapped.function_list]
        ccn_wrapped = _aggregate(ccn_values_wrapped, aggregation)

        # 3. 通常解析とラップ解析の結果を比較し、大きい方のスコアを採用する（方針A）
        final_ccn = max(ccn_normal, ccn_wrapped)

        # どちらの解析でも有効な関数・分岐が検出されない場合は、ベースラインである 1.0 を返す
        if final_ccn < 1.0:
            return 1.0

        return float(final_ccn)

    except Exception as e:
        logger.error(f"Failed to calculate cyclomatic complexity for '{filename}': {e}")
        return None
