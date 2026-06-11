"""Output writer registry and factory."""
from __future__ import annotations

from typing import Dict, Type

from .base import OutputWriter
from .json_writer import JsonWriter
from .parquet_writer import ParquetWriter

_REGISTRY: Dict[str, Type[OutputWriter]] = {}


def register_writer(writer_cls: Type[OutputWriter]) -> Type[OutputWriter]:
    """Register an OutputWriter under its ``format_name``."""
    _REGISTRY[writer_cls.format_name] = writer_cls
    return writer_cls


def create_writer(format_name: str) -> OutputWriter:
    """Instantiate a writer by format name.

    Raises:
        ValueError: If ``format_name`` is not registered.
    """
    if format_name not in _REGISTRY:
        supported = ", ".join(sorted(_REGISTRY))
        raise ValueError(
            f"Unknown output format '{format_name}'. Supported: {supported}"
        )
    return _REGISTRY[format_name]()


def supported_formats() -> list[str]:
    """Return the sorted list of supported output formats."""
    return sorted(_REGISTRY)


register_writer(JsonWriter)
register_writer(ParquetWriter)

__all__ = [
    "OutputWriter",
    "JsonWriter",
    "ParquetWriter",
    "register_writer",
    "create_writer",
    "supported_formats",
]