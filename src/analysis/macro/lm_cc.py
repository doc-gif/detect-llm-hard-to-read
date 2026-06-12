import pandas as pd
from typing import Optional

from schema.records import ParquetSchema as PCol

def calculate(df_clean: pd.DataFrame) -> Optional[float]:
    if df_clean.empty or PCol.IS_STATEMENT_START not in df_clean.columns or PCol.METRIC_ENTROPY not in df_clean.columns:
        return None

    statement_starts = df_clean[df_clean[PCol.IS_STATEMENT_START] == True].copy()
    if statement_starts.empty:
        return 0.0

    statement_starts[PCol.NESTING_DEPTH] = statement_starts[PCol.NESTING_DEPTH].fillna(0)
    complexities = (1 + statement_starts[PCol.NESTING_DEPTH]) * statement_starts[PCol.METRIC_ENTROPY]

    return float(complexities.sum())