import pandas as pd
from typing import Optional

from schema.records import ParquetSchema as PCol

OUT_COL = "first_token_surprisal"


# ---------------------------------------------------------
# 1. コア計算ロジック (ビジネスロジック)
# ---------------------------------------------------------
def __calculate__(is_function_start_series: pd.Series) -> pd.Series:
    """
    【純粋関数】関数の開始フラグの配列を受け取り、抽出用の真偽値マスク（条件式）を計算して返す。
    """
    return is_function_start_series == True


# ---------------------------------------------------------
# 2. データフレーム成形 (Transformation)
# ---------------------------------------------------------
def extract_first_token_surprisal(df_clean: pd.DataFrame) -> pd.DataFrame:
    """
    データフレームを受け取り、計算されたマスクを使って抽出を行い、新しいDFを返す。
    """
    if PCol.IS_FUNCTION_START not in df_clean.columns or PCol.FUNCTION_ID not in df_clean.columns or PCol.METRIC_SURPRISAL not in df_clean.columns:
        return pd.DataFrame(columns=[PCol.FUNCTION_ID, OUT_COL])

    # 抽出条件の計算はコアロジックに委譲する
    mask = __calculate__(df_clean[PCol.IS_FUNCTION_START])
    first_tokens = df_clean[mask].copy()

    return first_tokens[[PCol.FUNCTION_ID, PCol.METRIC_SURPRISAL]].rename(
        columns={PCol.METRIC_SURPRISAL: OUT_COL}
    )


# ---------------------------------------------------------
# 3. マクロ集計 (Aggregation)
# ---------------------------------------------------------
def calculate_avg(df_extracted: pd.DataFrame) -> Optional[float]:
    """
    抽出された第一トークンDFの平均値を計算してスカラーで返す。
    """
    if OUT_COL not in df_extracted.columns or df_extracted.empty:
        return None

    return float(df_extracted[OUT_COL].mean())