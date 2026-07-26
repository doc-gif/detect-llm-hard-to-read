# src/analysis/macro/complexity_helper/source_reconstruction.py
"""ソースコード読み込みヘルパー。

以前の実装ではトークン列からソースコードを再構築していたが、
`ParquetWriter`（Phase 1）が既に `FileMetadata`（元ファイルの絶対パス等）を
`meta_*` プレフィックス付きで全トークン行に非正規化して埋め込んでいることが
判明したため、再構築せず元ファイルをそのまま読み込む方式に変更した。

再構築より確実な上、`meta_file` の拡張子をそのまま Lizard に渡せるため、
対象言語が Python 以外に広がった場合も自動的に対応できる。
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

from schema.records import ParquetSchema as PCol

logger = logging.getLogger(__name__)


def load_source_from_meta(
    df: pd.DataFrame,
    file_col: str = PCol.META_FILE,
) -> Optional[Tuple[str, Path]]:
    """DataFrameの `meta_file` 列から元ソースファイルを読み込む。

    `ParquetWriter` はファイル単位のメタデータ（元ファイルの絶対パス含む）を
    全トークン行に非正規化して埋め込んでいるため、どの行からでも
    （先頭行で十分）元パスを取得できる。

    Args:
        df: `meta_file` 列を含むトークン単位の DataFrame。
        file_col: 元ファイルパスが入っているカラム名。

    Returns:
        ``(source_code, path)`` のタプル。読み込めない場合は None。
    """
    if df.empty or file_col not in df.columns:
        logger.warning(
            "'%s' column not found (or DataFrame is empty); cannot locate original source file.",
            file_col,
        )
        return None

    path_str = df[file_col].iloc[0]
    if not path_str:
        logger.warning("Empty '%s' value; cannot locate original source file.", file_col)
        return None

    path = Path(str(path_str))
    try:
        return path.read_text(encoding="utf-8"), path
    except OSError as e:
        logger.error(f"Failed to read original source file '{path}': {e}")
        return None