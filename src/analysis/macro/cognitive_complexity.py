# src/analysis/macro/cognitive_complexity.py
"""Cognitive Complexity（認知的複雑度）マクロ指標。

`cognitive-complexity` パッケージ
(https://github.com/Melevir/cognitive_complexity) を使用する。
Python の `ast.FunctionDef` を要求するため、Cyclomatic Complexity
(`cyclomatic_complexity.py`, Lizard使用) と違い Python 専用。

`meta_file`（Phase 1 の `ParquetWriter` が全行に埋め込む、元ソースファイルの
絶対パス）から元ファイルをそのまま読み込んで解析するため、トークンからの
再構築は行わない。
"""
from __future__ import annotations

import ast
import logging
from typing import Iterator, List, Optional, Union

import pandas as pd
from cognitive_complexity.api import get_cognitive_complexity

from macro.complexity_helper.source_reconstruction import load_source_from_meta

logger = logging.getLogger(__name__)

_VALID_AGGREGATIONS = ("sum", "mean", "max")
_PYTHON_SUFFIXES = (".py", ".pyi")

FunctionNode = Union[ast.FunctionDef, ast.AsyncFunctionDef]


def _iter_top_level_functions(tree: ast.Module) -> Iterator[FunctionNode]:
    """モジュール直下 / クラス直下の関数定義のみを列挙するジェネレータ。

    入れ子関数（クロージャ）まで対象に含めてしまうと、外側の関数の
    Cognitive Complexity 計算に内側の関数の中身がそのまま反映される
    ケースで二重カウントになりうるため、ネストした関数定義には潜らない。
    """

    def _walk(node: ast.AST, is_top_level_container: bool) -> Iterator[FunctionNode]:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if is_top_level_container:
                    yield child
                # 関数の中身（ネストした関数）には潜らず打ち切る
            elif isinstance(child, ast.ClassDef):
                yield from _walk(child, is_top_level_container=True)
            else:
                yield from _walk(child, is_top_level_container=False)

    yield from _walk(tree, is_top_level_container=True)


def _wrap_as_virtual_function(source_code: str) -> str:
    """スクリプト全体を、ASTが解析できるように仮想関数でラップする。"""
    indented_lines = [f"    {line}" if line.strip() else line for line in source_code.splitlines()]
    return "def __virtual_wrapper__():\n" + "\n".join(indented_lines)


def _aggregate(scores: List[int], aggregation: str) -> float:
    """指定された集約方法でスコアを計算する。"""
    if not scores:
        return 0.0
    if aggregation == "mean":
        return float(sum(scores)) / len(scores)
    if aggregation == "max":
        return float(max(scores))
    return float(sum(scores))


def calculate(
        token_df: pd.DataFrame,
        source_code: Optional[str] = None,
        aggregation: str = "sum",
) -> Optional[float]:
    """Cognitive Complexity を算出する。

    Args:
        token_df: `meta_file` 列を含むトークン単位の DataFrame。
        source_code: 既にソースコード文字列を持っている場合はここに渡すと、
            `meta_file` からの読み込みをスキップできる（テスト・将来の拡張用）。
            この場合、Python コードであることは呼び出し側の責任とする。
        aggregation: ファイル内に複数関数がある場合の集約方法。
            - "sum"  (既定): 全関数のスコアの合計
            - "mean": 全関数のスコアの平均
            - "max" : 最も複雑な関数のスコア

    Returns:
        算出した Cognitive Complexity。Python 以外のファイルや、算出できない
        場合は None。
    """
    if aggregation not in _VALID_AGGREGATIONS:
        raise ValueError(f"aggregation must be one of {_VALID_AGGREGATIONS}, got: {aggregation!r}")

    if source_code is None:
        loaded = load_source_from_meta(token_df)
        if loaded is None:
            logger.warning("Cognitive complexity calculation skipped: original source file not found.")
            return None
        source_code, source_path = loaded

        if source_path.suffix.lower() not in _PYTHON_SUFFIXES:
            logger.info(
                "Cognitive complexity skipped: '%s' is not a Python file (library is Python-only).",
                source_path,
            )
            return None

    if not source_code or not source_code.strip():
        logger.warning("Cognitive complexity calculation skipped: source file is empty.")
        return None

    try:
        # 1. 通常のソースコードからトップレベル関数のスコアを算出
        tree_normal = ast.parse(source_code)
        scores_normal: List[int] = [get_cognitive_complexity(fn) for fn in _iter_top_level_functions(tree_normal)]
        score_normal = _aggregate(scores_normal, aggregation)

        # 2. 必ずスクリプト全体を仮想関数としてラップしたコードも裏で解析
        wrapped_code = _wrap_as_virtual_function(source_code)
        tree_wrapped = ast.parse(wrapped_code)
        scores_wrapped: List[int] = [get_cognitive_complexity(fn) for fn in _iter_top_level_functions(tree_wrapped)]
        score_wrapped = _aggregate(scores_wrapped, aggregation)

        # 3. 通常解析とラップ解析の結果を比較し、大きい方のスコアを採用する（方針A）
        final_score = max(score_normal, score_wrapped)
        return float(final_score)

    except SyntaxError as e:
        logger.error(f"Failed to parse source for cognitive complexity: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to calculate cognitive complexity: {e}")
        return None
