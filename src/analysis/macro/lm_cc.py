import pandas as pd
from typing import Optional, Tuple
import logging

from macro.lm_cc_helper.calculate_code_with_boudaries import get_code_with_boundaries
from macro.lm_cc_helper.code_block_processor import CodeBlockProcessor
from macro.lm_cc_helper.get_lm_cc import get_lmcc
from schema.records import ParquetSchema as PCol

logger = logging.getLogger(__name__)


def calculate(df_clean: pd.DataFrame, threshold: float = 1.2515) -> Optional[Tuple[float, int]]:
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

        # 2. 境界の決定 (エントロピーが閾値1.2515nats(80th percentile)を超えた場所で境界線を引く)
        # 先行研究では、誤って67 percentileと解釈し論文を記載、ただしコードは0.67nats以上のトークンを閾値としていた。
        code_with_boundaries, _, start_end_tokens, semantic_unit_count = get_code_with_boundaries(
            tokens=tokens,
            entropies=entropies,
            threshold=threshold
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

        return float(score), semantic_unit_count

    except Exception as e:
        # Tree-sitter のパースエラーや境界処理で失敗した場合は None を返す
        logger.error(f"Failed to calculate LM-CC: {e}")
        return None