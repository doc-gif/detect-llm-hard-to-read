"""JSON output writer (nested metadata + tokens)."""
from __future__ import annotations

import json
from pathlib import Path

from schema import CollectionResult
from utils.io import ensure_parent
from utils.logging_config import get_logger

from .base import OutputWriter

LOGGER = get_logger(__name__)


class JsonWriter(OutputWriter):
    """Writes a single nested JSON document: ``{metadata, tokens}``."""

    format_name = "json"

    def write(self, result: CollectionResult, path: Path) -> None:
        """Serialize the result as UTF-8 JSON."""
        ensure_parent(path)
        payload = result.to_dict()
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        LOGGER.info("Wrote JSON output: %s", path)