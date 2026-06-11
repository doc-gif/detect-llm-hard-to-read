"""Parquet output writer (one record per token)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from schema import CollectionResult
from utils.io import ensure_parent
from utils.logging_config import get_logger

from .base import OutputWriter

LOGGER = get_logger(__name__)


class ParquetWriter(OutputWriter):
    """Writes a flat columnar table (one row per token).

    File-level metadata is attached to every row (denormalized) so the
    Parquet file is self-contained for Phase 2 consumption.
    """

    format_name = "parquet"

    def write(self, result: CollectionResult, path: Path) -> None:
        """Serialize the result as a Parquet table."""
        ensure_parent(path)
        meta = result.metadata.to_dict()
        rows = []
        for token in result.tokens:
            row = token.to_flat_dict()
            for key, value in meta.items():
                row[f"meta_{key}"] = value
            rows.append(row)

        frame = pd.DataFrame(rows)
        frame.to_parquet(path, engine="pyarrow", index=False)
        LOGGER.info("Wrote Parquet output: %s (%d rows)", path, len(frame))