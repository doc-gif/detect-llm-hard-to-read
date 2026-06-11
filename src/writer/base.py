"""Abstract base class for output writers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from schema import CollectionResult


class OutputWriter(ABC):
    """Persists a :class:`CollectionResult` to disk."""

    #: Registry key / format name (e.g. ``"json"``).
    format_name: str = "abstract"

    @abstractmethod
    def write(self, result: CollectionResult, path: Path) -> None:
        """Write ``result`` to ``path``."""