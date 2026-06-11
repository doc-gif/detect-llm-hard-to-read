"""pathlib-based safe IO helpers."""
from __future__ import annotations

from pathlib import Path

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False


def read_text(path: Path) -> str:
    """Read a UTF-8 text file.

    Args:
        path: File path.

    Returns:
        The file content as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {path}")
    if not path.is_file():
        raise ValueError(f"Not a regular file: {path}")
    return path.read_text(encoding="utf-8")


def ensure_parent(path: Path) -> None:
    """Ensure the parent directory of ``path`` exists."""
    path.parent.mkdir(parents=True, exist_ok=True)

def read_parquet(path: Path) -> "pd.DataFrame":
    """Read a Parquet file into a pandas DataFrame.

    Args:
        path: File path.

    Returns:
        The file content as a pandas DataFrame.

    Raises:
        ImportError: If pandas or pyarrow is not installed.
        FileNotFoundError: If the file does not exist.
        ValueError: If the path is not a regular file.
    """
    if not _PANDAS_AVAILABLE:
        raise ImportError(
            "pandas and pyarrow are required to read Parquet files. "
            "Install them with: pip install pandas pyarrow"
        )
    if not path.exists():
        raise FileNotFoundError(f"Parquet file not found: {path}")
    if not path.is_file():
        raise ValueError(f"Not a regular file: {path}")
    return pd.read_parquet(path)