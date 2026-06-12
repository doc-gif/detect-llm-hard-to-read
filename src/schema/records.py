"""Dataclasses describing the raw data collected in Phase 1.

These structures are intentionally *flat and extensible*. Token-level
features live inside ``TokenRecord.token_metrics`` so that future metrics
(e.g. ``hidden_norm``, ``attention_entropy``) can be added without changing
the schema shape.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

COLLECTOR_VERSION = "1.0.0"


class Fields:
    IDX = "idx"
    TOKEN_ID = "token_id"
    TOKEN_STR = "token_str"
    LINE = "line"
    COLUMN = "column"
    AST_TYPE = "ast_type"
    NESTING_DEPTH = "nesting_depth"
    FUNCTION_ID = "function_id"
    IS_STATEMENT_START = "is_statement_start"
    IS_FUNCTION_START = "is_function_start"

    # metrics 辞書内で使われるキー
    METRIC_KEY_SURPRISAL = "surprisal"
    METRIC_KEY_ENTROPY = "entropy"
    METRIC_KEY_ISOLATED_SURPRISAL = "isolated_surprisal"

    # Parquet保存時に付与されるプレフィックス
    METRIC_PREFIX = "metric_"


@dataclass(slots=True)
class TokenRecord:
    """A single token observation.

    Attributes:
        idx: Position of the token within the full tokenized sequence.
        token_id: Tokenizer vocabulary id.
        token_str: Decoded string representation of the token.
        line: 1-based source line (or ``None`` for special tokens).
        column: 0-based source column (or ``None`` for special tokens).
        ast_type: Tree-sitter node type covering the token.
        nesting_depth: Structural nesting depth of the token in the AST.
        function_id: Identifier of the enclosing function, if any.
        is_statement_start: Whether the token starts a statement.
        token_metrics: Open-ended mapping of scalar metrics. Phase 1 fills
            ``surprisal``, ``entropy`` and ``isolated_surprisal``.
    """

    idx: int
    token_id: int
    token_str: str

    line: Optional[int] = None
    column: Optional[int] = None

    ast_type: Optional[str] = None
    nesting_depth: Optional[int] = None
    function_id: Optional[str] = None

    is_statement_start: bool = False
    is_function_start: bool = False

    token_metrics: Dict[str, Optional[float]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_flat_dict(self) -> Dict[str, Any]:
        """Return a flattened representation (one record per token)."""
        # 💡 Fields の定数を使って辞書を構築し、名前のズレを防ぐ
        base: Dict[str, Any] = {
            Fields.IDX: self.idx,
            Fields.TOKEN_ID: self.token_id,
            Fields.TOKEN_STR: self.token_str,
            Fields.LINE: self.line,
            Fields.COLUMN: self.column,
            Fields.AST_TYPE: self.ast_type,
            Fields.NESTING_DEPTH: self.nesting_depth,
            Fields.FUNCTION_ID: self.function_id,
            Fields.IS_STATEMENT_START: self.is_statement_start,
            Fields.IS_FUNCTION_START: self.is_function_start,
        }
        # metrics をフラット化 (metric_ プレフィックスを付与)
        for key, value in self.token_metrics.items():
            base[f"{Fields.METRIC_PREFIX}{key}"] = value
        return base


@dataclass(slots=True)
class FileMetadata:
    """Metadata describing the analyzed file and the collection run."""

    project: str
    file: str
    language: str

    model_name: str
    model_revision: Optional[str]
    tokenizer_name: str

    context_strategy: str

    total_tokens: int

    created_at: str
    collector_version: str = COLLECTOR_VERSION

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)


@dataclass(slots=True)
class CollectionResult:
    """The full payload produced for a single source file."""

    metadata: FileMetadata
    tokens: List[TokenRecord]

    def to_dict(self) -> Dict[str, Any]:
        """Return a nested JSON-serializable representation."""
        return {
            "metadata": self.metadata.to_dict(),
            "tokens": [t.to_dict() for t in self.tokens],
        }

class ParquetSchema:
    """
    Parquetファイルとして保存された後の、DataFrameのカラム名を定義するスキーマ。
    """
    # 💡 Fields の定数をそのまま引き継ぐことで、完全な一元管理を実現
    IDX = Fields.IDX
    TOKEN_ID = Fields.TOKEN_ID
    TOKEN_STR = Fields.TOKEN_STR
    LINE = Fields.LINE
    COLUMN = Fields.COLUMN
    AST_TYPE = Fields.AST_TYPE
    NESTING_DEPTH = Fields.NESTING_DEPTH
    FUNCTION_ID = Fields.FUNCTION_ID
    IS_STATEMENT_START = Fields.IS_STATEMENT_START
    IS_FUNCTION_START = Fields.IS_FUNCTION_START

    # 💡 フラット化されたメトリクスのカラム名を動的に生成して定義
    METRIC_SURPRISAL = f"{Fields.METRIC_PREFIX}{Fields.METRIC_KEY_SURPRISAL}"
    METRIC_ENTROPY = f"{Fields.METRIC_PREFIX}{Fields.METRIC_KEY_ENTROPY}"
    METRIC_ISOLATED_SURPRISAL = f"{Fields.METRIC_PREFIX}{Fields.METRIC_KEY_ISOLATED_SURPRISAL}"

    # --- Phase 2 で追加される拡張メトリクス ---
    CALC_SURPRISAL_GAP = "surprisal_gap"


class SummarySchema:
    """
    Phase 2 の分析結果として出力されるサマリーCSV (`analysis_summary.csv`) のカラム名定義。

    【📊 CSVデータの構造イメージ (1行 = 1ソースコードファイル)】
    +----------+------------+-------+------------+------------------+---------------------------+---------------------------+--------------+---------------+
    | uid      | dataset    | ppl   | lm_cc      | lm_cc_density    | avg_first_token_surprisal | avg_context_surprisal_gap | total_tokens | num_functions |
    +----------+------------+-------+------------+------------------+---------------------------+---------------------------+--------------+---------------+
    | 0a4af5.. | apr        | 1.05  | 12.4       | 6.2              | 0.12                      | 0.05                      | 150          | 2             |
    | HumanE_0 | humaneval  | 2.10  | 8.5        | 8.5              | 0.88                      | 0.10                      | 45           | 1             |
    +----------+------------+-------+------------+------------------+---------------------------+---------------------------+--------------+---------------+
    """
    UID = "uid"
    DATASET = "dataset"
    PPL = "ppl"
    LM_CC = "lm_cc"
    LM_CC_DENSITY = "lm_cc_density"
    AVG_FIRST_TOKEN_SURPRISAL = "avg_first_token_surprisal"
    AVG_CONTEXT_SURPRISAL_GAP = "avg_context_surprisal_gap"
    TOTAL_TOKENS = "total_tokens"
    NUM_FUNCTIONS = "num_functions"