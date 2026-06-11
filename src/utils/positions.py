"""Helpers to translate character offsets into (line, column) positions.

Tree-sitter uses 0-based rows and columns measured in *bytes*. HuggingFace
offset mappings are in *character* offsets over the decoded string. To keep
the two worlds consistent we work on the UTF-8 byte representation of the
source and expose both byte points (for Tree-sitter) and human-friendly
1-based lines / 0-based columns (for the schema).
"""
from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(slots=True)
class OffsetIndex:
    """Index over a source string enabling O(log n) offset lookups."""

    text: str
    _line_start_chars: List[int]

    @classmethod
    def build(cls, text: str) -> "OffsetIndex":
        """Build the index from raw source text."""
        starts: List[int] = [0]
        for i, ch in enumerate(text):
            if ch == "\n":
                starts.append(i + 1)
        return cls(text=text, _line_start_chars=starts)

    def char_to_line_column(self, char_offset: int) -> Tuple[int, int]:
        """Convert a character offset to a 1-based line and 0-based column.

        Args:
            char_offset: Index into the source string.

        Returns:
            A ``(line, column)`` tuple.
        """
        if char_offset < 0:
            char_offset = 0
        line_idx = bisect_right(self._line_start_chars, char_offset) - 1
        line_idx = max(line_idx, 0)
        column = char_offset - self._line_start_chars[line_idx]
        return line_idx + 1, column

    def char_to_byte(self, char_offset: int) -> int:
        """Convert a character offset to a UTF-8 byte offset."""
        clamped = max(0, min(char_offset, len(self.text)))
        return len(self.text[:clamped].encode("utf-8"))