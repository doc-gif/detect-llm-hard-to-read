"""Function-scope context strategy."""
from __future__ import annotations

from typing import List

from language import FunctionSpan

from .base import ContextStrategy, ContextWindow


class FunctionScopeStrategy(ContextStrategy):
    """One isolated window per function, spanning the function body.

    Offsets are derived from the function byte span by decoding the source's
    UTF-8 prefix length. We pass character offsets so the orchestrator can
    align them with tokenizer offset mappings.
    """

    strategy_name = "function_scope"

    def build_windows(
        self, source: str, functions: List[FunctionSpan]
    ) -> List[ContextWindow]:
        """Create one window per function span."""
        source_bytes = source.encode("utf-8")
        windows: List[ContextWindow] = []
        for span in functions:
            char_start = len(source_bytes[: span.start_byte].decode("utf-8", "replace"))
            char_end = len(source_bytes[: span.end_byte].decode("utf-8", "replace"))
            windows.append(
                ContextWindow(
                    name=span.function_id,
                    char_start=char_start,
                    char_end=char_end,
                )
            )
        return windows