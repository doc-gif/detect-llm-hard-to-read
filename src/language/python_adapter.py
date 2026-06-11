"""Python language adapter."""
from __future__ import annotations

from typing import Optional

import tree_sitter_python
from tree_sitter import Language, Node, Parser

from .base import LanguageAdapter


class PythonAdapter(LanguageAdapter):
    """LanguageAdapter implementation for Python (.py)."""

    extensions = frozenset({".py", ".pyw"})
    language_name = "python"

    # Tree-sitter Python parser における「文 (Statement)」として扱われるノードのタイプ一覧
    _STATEMENT_TYPES = frozenset(
        {
            "expression_statement",
            "if_statement",
            "for_statement",
            "while_statement",
            "try_statement",
            "with_statement",
            "return_statement",
            "break_statement",
            "continue_statement",
            "pass_statement",
            "raise_statement",
            "import_statement",
            "import_from_statement",
            "global_statement",
            "nonlocal_statement",
            "assert_statement",
            "delete_statement",
            "match_statement",  # Python 3.10+
            "exec_statement",   # Python 2
            "print_statement",  # Python 2
        }
    )

    def create_parser(self) -> Parser:
        """Create a Tree-sitter parser configured for Python."""
        language = Language(tree_sitter_python.language())
        return Parser(language)

    def is_function_node(self, node: Node) -> bool:
        """Python functions are ``function_definition`` nodes."""
        return node.type == "function_definition"

    def extract_function_id(self, node: Node, source_bytes: bytes) -> str:
        """Extract the declared function name from the function_definition."""
        # Pythonの関数定義ノードは直接 "name" というフィールドで関数名(identifier)を持っています
        name_node = node.child_by_field_name("name")
        if name_node is not None:
            return source_bytes[name_node.start_byte : name_node.end_byte].decode(
                "utf-8", errors="replace"
            )
        return f"anonymous@{node.start_point[0] + 1}"

    def is_statement_start_node(self, node: Node) -> bool:
        """Return True for Python statement-level node types."""
        return node.type in self._STATEMENT_TYPES

    def _is_nesting_node(self, node: Node) -> bool:
        """Python uses 'block' to represent a suite of statements."""
        return node.type == "block"