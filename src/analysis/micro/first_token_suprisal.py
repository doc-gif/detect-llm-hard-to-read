import pandas as pd


def extract_first_token_surprisal(df_clean: pd.DataFrame) -> pd.DataFrame:
    """
    関数の「第一トークン・サプライザル」を抽出するミクロ(局所)抽出モジュール。

    【算出式】
    First_Token_Surprisal(f) = surprisal_t  (where is_function_start == True)
    """
    if 'is_function_start' not in df_clean.columns or 'function_id' not in df_clean.columns:
        return pd.DataFrame(columns=['function_id', 'first_token_surprisal'])

    first_tokens = df_clean[df_clean['is_function_start'] == True].copy()
    return first_tokens[['function_id', 'surprisal']].rename(
        columns={'surprisal': 'first_token_surprisal'}
    )