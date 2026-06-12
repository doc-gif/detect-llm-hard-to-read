import pandas as pd

from schema.records import ParquetSchema as PCol


def extract_first_token_surprisal(df_clean: pd.DataFrame) -> pd.DataFrame:
    out_col = "first_token_surprisal"

    if PCol.IS_FUNCTION_START not in df_clean.columns or PCol.FUNCTION_ID not in df_clean.columns or PCol.METRIC_SURPRISAL not in df_clean.columns:
        return pd.DataFrame(columns=[PCol.FUNCTION_ID, out_col])

    first_tokens = df_clean[df_clean[PCol.IS_FUNCTION_START] == True].copy()

    return first_tokens[[PCol.FUNCTION_ID, PCol.METRIC_SURPRISAL]].rename(
        columns={PCol.METRIC_SURPRISAL: out_col}
    )