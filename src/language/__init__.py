"""Language adapter registry and factory.

New languages are added by implementing :class:`LanguageAdapter` and
registering the class here (or via :func:`register_language`).
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Type

from .base import FunctionSpan, LanguageAdapter
from .c_adapter import CAdapter
from .java_adapter import JavaAdapter
from .python_adapter import PythonAdapter

_REGISTRY: Dict[str, Type[LanguageAdapter]] = {}


def register_language(adapter_cls: Type[LanguageAdapter]) -> Type[LanguageAdapter]:
    """Register a LanguageAdapter for each of its file extensions."""
    for ext in adapter_cls.extensions:
        _REGISTRY[ext.lower()] = adapter_cls
    return adapter_cls


def get_adapter_for_path(path: Path) -> LanguageAdapter:
    """Return a fresh adapter instance for the file extension of ``path``.

    Raises:
        ValueError: If the extension is not supported.
    """
    ext = path.suffix.lower()
    if ext not in _REGISTRY:
        supported = ", ".join(sorted(_REGISTRY))
        raise ValueError(
            f"Unsupported file extension '{ext}'. Supported: {supported}"
        )
    return _REGISTRY[ext]()


def supported_extensions() -> list[str]:
    """Return the sorted list of supported extensions."""
    return sorted(_REGISTRY)


# Built-in registrations.
register_language(CAdapter)
register_language(JavaAdapter)
register_language(PythonAdapter)

__all__ = [
    "FunctionSpan",
    "LanguageAdapter",
    "CAdapter",
    "JavaAdapter",
    "PythonAdapter",
    "register_language",
    "get_adapter_for_path",
    "supported_extensions",
]