import pandas as pd
from typing import Optional

from schema.records import ParquetSchema as PCol


def calculate(df_clean: pd.DataFrame) -> Optional[int]:
    """
    データフレームからファイルの総行数(Lines of Code)を計算します。
    トークンが存在する最大の行番号をLoCとして返します。
    """
    if df_clean.empty or PCol.LINE not in df_clean.columns:
        return None

    # 行番号データ（NaNを除外）を取得
    lines = df_clean[PCol.LINE].dropna()

    if lines.empty:
        return 0

    # 最も下にあるトークンの行番号をファイルの総行数（LoC）とする
    return int(lines.max())