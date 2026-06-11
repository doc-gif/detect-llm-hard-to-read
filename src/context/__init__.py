"""Context strategy registry and factory."""
from __future__ import annotations

from typing import Dict, Type

from .base import ContextStrategy, ContextWindow
from .function_scope import FunctionScopeStrategy

_REGISTRY: Dict[str, Type[ContextStrategy]] = {}


def register_strategy(strategy_cls: Type[ContextStrategy]) -> Type[ContextStrategy]:
    """Register a ContextStrategy under its ``strategy_name``."""
    _REGISTRY[strategy_cls.strategy_name] = strategy_cls
    return strategy_cls


def create_context_strategy(name: str) -> ContextStrategy:
    """Instantiate a context strategy by name.

    Raises:
        ValueError: If ``name`` is not registered.
    """
    if name not in _REGISTRY:
        supported = ", ".join(sorted(_REGISTRY))
        raise ValueError(f"Unknown context strategy '{name}'. Supported: {supported}")
    return _REGISTRY[name]()


register_strategy(FunctionScopeStrategy)

__all__ = [
    "ContextStrategy",
    "ContextWindow",
    "FunctionScopeStrategy",
    "register_strategy",
    "create_context_strategy",
]