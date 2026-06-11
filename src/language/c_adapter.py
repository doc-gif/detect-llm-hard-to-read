"""C language adapter."""
from __future__ import annotations

from typing import Optional

import tree_sitter_c
from tree_sitter import Language, Node, Parser

from .base import LanguageAdapter


class CAdapter(LanguageAdapter):
    """LanguageAdapter implementation for C (.c, .h)."""

    extensions = frozenset({".c", ".h"})
    language_name = "c"

    _STATEMENT_TYPES = frozenset(
        {
            "declaration",
            "expression_statement",
            "if_statement",
            "for_statement",
            "while_statement",
            "do_statement",
            "switch_statement",
            "return_statement",
            "break_statement",
            "continue_statement",
            "goto_statement",
            "labeled_statement",
            "compound_statement",
        }
    )

    def create_parser(self) -> Parser:
        """Create a Tree-sitter parser configured for C."""
        language = Language(tree_sitter_c.language())
        return Parser(language)

    def is_function_node(self, node: Node) -> bool:
        """C functions are ``function_definition`` nodes."""
        return node.type == "function_definition"

    def extract_function_id(self, node: Node, source_bytes: bytes) -> str:
        """Extract the declared function name from the declarator subtree."""
        declarator = node.child_by_field_name("declarator")
        name = self._find_identifier(declarator, source_bytes)
        return name or f"anonymous@{node.start_point[0] + 1}"

    def is_statement_start_node(self, node: Node) -> bool:
        """Return True for C statement-level node types."""
        return node.type in self._STATEMENT_TYPES

    def _is_nesting_node(self, node: Node) -> bool:
        return node.type == "compound_statement"

    @staticmethod
    def _find_identifier(node: Optional[Node], source_bytes: bytes) -> Optional[str]:
        """Depth-first search for the first ``identifier`` token."""
        if node is None:
            return None
        stack = [node]
        while stack:
            current = stack.pop()
            if current.type == "identifier":
                return source_bytes[current.start_byte : current.end_byte].decode(
                    "utf-8", errors="replace"
                )
            stack.extend(current.children)
        return None