import math
import pandas as pd
from typing import Optional

from schema.records import ParquetSchema as PCol

def calculate(df_clean: pd.DataFrame) -> Optional[float]:
    if df_clean.empty or PCol.METRIC_SURPRISAL not in df_clean.columns:
        return None

    surprisal_series = df_clean[PCol.METRIC_SURPRISAL].dropna()
    if len(surprisal_series) == 0:
        return None

    return math.exp(surprisal_series.mean())