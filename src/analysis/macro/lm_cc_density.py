import pandas as pd
from typing import Optional


def calculate_lmcc_density_per_function(df_clean: pd.DataFrame) -> Optional[float]:
    """
    ファイル全体における Semantic Unit (関数) あたりの LM-CC 密度を算出するマクロ指標。

    【算出式】
    LM-CC_Density = Total_LM-CC_in_units / N  (Nはファイル内の関数ユニット総数)
    """
    if df_clean.empty or 'is_statement_start' not in df_clean.columns or 'function_id' not in df_clean.columns:
        return None

    # 関数ブロック内に存在するステートメントの開始トークンのみ抽出
    statements = df_clean[(df_clean['is_statement_start'] == True) & (df_clean['function_id'].notnull())].copy()
    if statements.empty:
        return 0.0

    statements['nesting_depth'] = statements['nesting_depth'].fillna(0)
    statements['stmt_complexity'] = (1 + statements['nesting_depth']) * statements['entropy']

    # 各関数ごとのLM-CCの総和を算出
    unit_lmcc_series = statements.groupby('function_id')['stmt_complexity'].sum()

    num_units = len(unit_lmcc_series)
    total_unit_lmcc = unit_lmcc_series.sum()

    # 🌟 総スコアをユニット数で割ることで、マクロな「密度」とする
    return float(total_unit_lmcc / num_units) if num_units > 0 else 0.0