import pandas as pd
import numpy as np
from typing import Optional

from schema.records import ParquetSchema as PCol


# ---------------------------------------------------------
# 1. コア計算ロジック (ビジネスロジック)
# ---------------------------------------------------------
def __calculate__(isolated_series: pd.Series, full_series: pd.Series) -> pd.Series:
    """
    【純粋関数】2つのサプライザル配列を受け取り、ギャップ（差分）の配列を計算して返す。
    """
    return isolated_series - full_series


# ---------------------------------------------------------
# 2. データフレーム成形 (Transformation)
# ---------------------------------------------------------
def add_contextual_surprisal_gap(df: pd.DataFrame) -> pd.DataFrame:
    """
    データフレームを受け取り、計算ロジックを呼び出して新しい列を追加した状態のDFを返す。
    """
    res_df = df.copy()

    if PCol.METRIC_ISOLATED_SURPRISAL in res_df.columns and PCol.METRIC_SURPRISAL in res_df.columns:
        # 計算はコアロジックに委譲する
        res_df[PCol.CALC_SURPRISAL_GAP] = __calculate__(
            res_df[PCol.METRIC_ISOLATED_SURPRISAL],
            res_df[PCol.METRIC_SURPRISAL]
        )
    else:
        res_df[PCol.CALC_SURPRISAL_GAP] = np.nan

    return res_df


# ---------------------------------------------------------
# 3. マクロ集計 (Aggregation)
# ---------------------------------------------------------
def calculate_avg(df_enriched: pd.DataFrame) -> Optional[float]:
    """
    ギャップ列の平均値を計算してスカラーで返す。
    """
    if PCol.CALC_SURPRISAL_GAP not in df_enriched.columns:
        return None

    return float(df_enriched[PCol.CALC_SURPRISAL_GAP].mean())