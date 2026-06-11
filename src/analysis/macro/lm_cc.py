import pandas as pd
from typing import Optional


def calculate_macro_lmcc(df_clean: pd.DataFrame) -> Optional[float]:
    """
    ファイル全体の言語モデルベースコード複雑度(LM-CC)を算出する。

    【算出式】
    LM-CC_macro = Σ_{s ∈ Statements} ( (1 + nesting_depth_s) * entropy_s )
    """
    if df_clean.empty or 'is_statement_start' not in df_clean.columns:
        return None

    statement_starts = df_clean[df_clean['is_statement_start'] == True].copy()
    if statement_starts.empty:
        return 0.0

    statement_starts['nesting_depth'] = statement_starts['nesting_depth'].fillna(0)
    complexities = (1 + statement_starts['nesting_depth']) * statement_starts['entropy']

    return float(complexities.sum())