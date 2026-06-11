"""Java language adapter."""
from __future__ import annotations

from typing import Optional

import tree_sitter_java
from tree_sitter import Language, Node, Parser

from .base import LanguageAdapter


class JavaAdapter(LanguageAdapter):
    """LanguageAdapter implementation for Java (.java)."""

    extensions = frozenset({".java"})
    language_name = "java"

    _FUNCTION_TYPES = frozenset({"method_declaration", "constructor_declaration"})

    _STATEMENT_TYPES = frozenset(
        {
            "local_variable_declaration",
            "expression_statement",
            "if_statement",
            "for_statement",
            "enhanced_for_statement",
            "while_statement",
            "do_statement",
            "switch_expression",
            "return_statement",
            "break_statement",
            "continue_statement",
            "throw_statement",
            "try_statement",
            "synchronized_statement",
            "block",
            "labeled_statement",
            "yield_statement",
            "assert_statement",
        }
    )

    def create_parser(self) -> Parser:
        """Create a Tree-sitter parser configured for Java."""
        language = Language(tree_sitter_java.language())
        return Parser(language)

    def is_function_node(self, node: Node) -> bool:
        """Java functions are method/constructor declarations."""
        return node.type in self._FUNCTION_TYPES

    def extract_function_id(self, node: Node, source_bytes: bytes) -> str:
        """Extract the method/constructor name from the ``name`` field."""
        name_node = node.child_by_field_name("name")
        if name_node is not None:
            return source_bytes[name_node.start_byte : name_node.end_byte].decode(
                "utf-8", errors="replace"
            )
        return f"anonymous@{node.start_point[0] + 1}"

    def is_statement_start_node(self, node: Node) -> bool:
        """Return True for Java statement-level node types."""
        return node.type in self._STATEMENT_TYPES

    def _is_nesting_node(self, node: Node) -> bool:
        return node.type == "block"