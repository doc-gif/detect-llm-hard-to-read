import pandas as pd
import numpy as np

from schema.records import ParquetSchema as PCol

def add_contextual_surprisal_gap(df: pd.DataFrame) -> pd.DataFrame:
    res_df = df.copy()
    if PCol.METRIC_ISOLATED_SURPRISAL in res_df.columns and PCol.METRIC_SURPRISAL in res_df.columns:
        res_df[PCol.CALC_SURPRISAL_GAP] = res_df[PCol.METRIC_ISOLATED_SURPRISAL] - res_df[PCol.METRIC_SURPRISAL]
    else:
        res_df[PCol.CALC_SURPRISAL_GAP] = np.nan

    return res_df