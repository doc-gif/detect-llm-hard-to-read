import pandas as pd
import numpy as np


def add_contextual_surprisal_gap(df: pd.DataFrame) -> pd.DataFrame:
    """
    トークンごとに「文脈的サプライザル・ギャップ」を算出し、新しいカラムとして追加する。

    【算出式】
    Contextual_Surprisal_Gap_t = isolated_surprisal_t - surprisal_t
    """
    res_df = df.copy()
    if 'isolated_surprisal' in res_df.columns and 'surprisal' in res_df.columns:
        res_df['surprisal_gap'] = res_df['isolated_surprisal'] - res_df['surprisal']
    else:
        res_df['surprisal_gap'] = np.nan

    return res_df