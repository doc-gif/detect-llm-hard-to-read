import math
import pandas as pd
from typing import Optional


def calculate(df_clean: pd.DataFrame) -> Optional[float]:
    """
    ファイル全体のパープレキシティ(PPL)を算出する。

    【算出式】
    PPL = exp( mean(surprisal) )
    """
    if df_clean.empty or 'surprisal' not in df_clean.columns:
        return None

    surprisal_series = df_clean['surprisal'].dropna()
    if len(surprisal_series) == 0:
        return None

    return math.exp(surprisal_series.mean())