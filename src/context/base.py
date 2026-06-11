"""Abstract base class for context strategies used in isolated inference."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from language import FunctionSpan


@dataclass(slots=True)
class ContextWindow:
    """A contiguous source slice to be re-inferred in isolation.

    Attributes:
        name: Identifier of the window (typically the function id).
        char_start: Inclusive character start offset in the source.
        char_end: Exclusive character end offset in the source.
    """

    name: str
    char_start: int
    char_end: int


class ContextStrategy(ABC):
    """Decides how source code is sliced for isolated_surprisal."""

    #: Registry key (e.g. ``"function_scope"``).
    strategy_name: str = "abstract"

    @abstractmethod
    def build_windows(
        self, source: str, functions: List[FunctionSpan]
    ) -> List[ContextWindow]:
        """Return the list of isolated context windows for a source file."""