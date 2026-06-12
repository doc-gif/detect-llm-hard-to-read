import pandas as pd
from typing import Optional

from schema.records import ParquetSchema as PCol

def calculate(df_clean: pd.DataFrame) -> Optional[float]:
    if df_clean.empty or PCol.IS_STATEMENT_START not in df_clean.columns or PCol.FUNCTION_ID not in df_clean.columns or PCol.METRIC_ENTROPY not in df_clean.columns:
        return None

    statements = df_clean[(df_clean[PCol.IS_STATEMENT_START] == True) & (df_clean[PCol.FUNCTION_ID].notnull())].copy()
    if statements.empty:
        return 0.0

    statements[PCol.NESTING_DEPTH] = statements[PCol.NESTING_DEPTH].fillna(0)
    statements['stmt_complexity'] = (1 + statements[PCol.NESTING_DEPTH]) * statements[PCol.METRIC_ENTROPY]

    unit_lmcc_series = statements.groupby(PCol.FUNCTION_ID)['stmt_complexity'].sum()

    num_units = len(unit_lmcc_series)
    total_unit_lmcc = unit_lmcc_series.sum()

    return float(total_unit_lmcc / num_units) if num_units > 0 else 0.0