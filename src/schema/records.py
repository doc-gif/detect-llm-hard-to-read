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
        """Return a JSON-serializable representation."""
        return asdict(self)

    def to_flat_dict(self) -> Dict[str, Any]:
        """Return a flattened representation (one record per token).

        ``token_metrics`` keys are prefixed with ``metric_`` so the columnar
        layout (Parquet) stays self-describing and collision-free.
        """
        base: Dict[str, Any] = {
            "idx": self.idx,
            "token_id": self.token_id,
            "token_str": self.token_str,
            "line": self.line,
            "column": self.column,
            "ast_type": self.ast_type,
            "nesting_depth": self.nesting_depth,
            "function_id": self.function_id,
            "is_statement_start": self.is_statement_start,
            "is_function_start": self.is_function_start,
        }
        for key, value in self.token_metrics.items():
            base[f"metric_{key}"] = value
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