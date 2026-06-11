"""Abstract base class for language-specific source handling."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from tree_sitter import Node, Parser, Tree


@dataclass(slots=True)
class FunctionSpan:
    """Byte span and identity of an extracted function/method."""

    function_id: str
    start_byte: int
    end_byte: int
    start_point: tuple[int, int]  # (row, column), 0-based
    end_point: tuple[int, int]


class LanguageAdapter(ABC):
    """Encapsulates all language-dependent parsing logic.

    Subclasses provide the Tree-sitter grammar and the language-specific
    rules for function extraction, statement detection and nesting.
    """

    #: File extensions handled by this adapter (e.g. ``{".java"}``).
    extensions: frozenset[str] = frozenset()

    #: Human-readable language name stored in metadata.
    language_name: str = "unknown"

    @abstractmethod
    def create_parser(self) -> Parser:
        """Create and return a configured Tree-sitter parser."""

    def parse(self, source: str) -> Tree:
        """Parse source code into a Tree-sitter tree."""
        parser = self.create_parser()
        return parser.parse(source.encode("utf-8"))

    @abstractmethod
    def is_function_node(self, node: Node) -> bool:
        """Return True if ``node`` represents a function/method definition."""

    @abstractmethod
    def extract_function_id(self, node: Node, source_bytes: bytes) -> str:
        """Return a stable identifier for a function node."""

    @abstractmethod
    def is_statement_start_node(self, node: Node) -> bool:
        """Return True if ``node`` type denotes the start of a statement."""

    # ----- shared, language-agnostic helpers ------------------------------

    def extract_functions(self, tree: Tree, source_bytes: bytes) -> List[FunctionSpan]:
        """Return all function spans found in the tree (DFS order)."""
        spans: List[FunctionSpan] = []
        stack = [tree.root_node]
        while stack:
            node = stack.pop()
            if self.is_function_node(node):
                spans.append(
                    FunctionSpan(
                        function_id=self.extract_function_id(node, source_bytes),
                        start_byte=node.start_byte,
                        end_byte=node.end_byte,
                        start_point=node.start_point,
                        end_point=node.end_point,
                    )
                )
            stack.extend(reversed(node.children))
        return spans

    def node_at_point(self, tree: Tree, row: int, column: int) -> Optional[Node]:
        """Return the smallest named node covering a (row, column) point."""
        point = (row, column)
        node = tree.root_node.descendant_for_point_range(point, point)
        return node

    def ast_type(self, node: Optional[Node]) -> Optional[str]:
        """Return the AST node type string."""
        return node.type if node is not None else None

    def nesting_depth(self, node: Optional[Node]) -> Optional[int]:
        """Compute the structural nesting depth of a node.

        Depth counts the number of ancestor *block/compound/body* nodes,
        approximating the syntactic nesting level used in complexity studies.
        """
        if node is None:
            return None
        depth = 0
        current = node.parent
        while current is not None:
            if self._is_nesting_node(current):
                depth += 1
            current = current.parent
        return depth

    def function_id_for_point(
        self, functions: List[FunctionSpan], byte_offset: int
    ) -> Optional[str]:
        """Return the innermost function id containing ``byte_offset``."""
        best: Optional[FunctionSpan] = None
        for span in functions:
            if span.start_byte <= byte_offset < span.end_byte:
                if best is None or span.start_byte >= best.start_byte:
                    best = span
        return best.function_id if best else None

    def is_function_start_for_point(
            self, functions: List[FunctionSpan], byte_offset: int, token_len: int
    ) -> bool:
        """Return True if the given byte_offset matches the start of any function.

        Args:
            functions: extract_functions で抽出された関数のスパンリスト
            byte_offset: 現在のトークンの開始バイト位置
            token_len: 現在のトークンの長さ (バイト換算、または次のトークンとの境界判定用)
        """
        for span in functions:
            if span.start_byte == byte_offset:
                return True
            if byte_offset <= span.start_byte < (byte_offset + token_len):
                return True
        return False

    def _is_nesting_node(self, node: Node) -> bool:
        """Default heuristic for block-like nodes; overridable per language."""
        return node.type in {"block", "compound_statement", "function_body"}