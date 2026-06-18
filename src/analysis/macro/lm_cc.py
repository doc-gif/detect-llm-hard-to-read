import pandas as pd
from typing import Optional
import logging

from .lm_cc_calculation import get_code_with_boundaries, CodeBlockProcessor, get_lmcc
from schema.records import ParquetSchema as PCol

logger = logging.getLogger(__name__)


def calculate(df_clean: pd.DataFrame) -> Optional[float]:
    """
    データフレーム内のトークンとエントロピー情報を用いて、
    先行研究のアルゴリズム (Tree-sitter AST解析) で LM-CC スコアを算出します。
    """
    # 必須カラムが存在するかチェック
    if df_clean.empty or PCol.TOKEN_STR not in df_clean.columns or PCol.METRIC_ENTROPY not in df_clean.columns:
        logger.warning("LM-CC calculation skipped: Missing required columns (TOKEN or METRIC_ENTROPY).")
        return None

    try:
        # 1. データフレームからトークンとエントロピーのリストを抽出
        tokens = df_clean[PCol.TOKEN_STR].tolist()
        entropies = df_clean[PCol.METRIC_ENTROPY].tolist()

        # 2. 境界の決定 (エントロピーが閾値0.67を超えた場所で境界線を引く)
        code_with_boundaries, _, start_end_tokens = get_code_with_boundaries(
            tokens=tokens,
            entropies=entropies,
            threshold=0.67
        )

        # 3. 構文解析 (Tree-sitter) によるブロック階層(ツリー構造)の構築
        processor = CodeBlockProcessor()
        block_tree_dict = processor.parse_code_blocks(
            code_with_boundaries=code_with_boundaries,
            tokens=tokens,
            start_end_tokens=start_end_tokens
        )

        # 4. ツリー構造から LM-CC スコアを計算 (深さと分岐の重み付け加算)
        score = get_lmcc(block_tree_dict)

        return float(score)

    except Exception as e:
        # Tree-sitter のパースエラーや境界処理で失敗した場合は None を返す
        logger.error(f"Failed to calculate LM-CC: {e}")
        return None