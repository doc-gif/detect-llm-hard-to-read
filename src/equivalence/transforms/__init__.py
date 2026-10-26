"""等価変換の登録と生成。"""
from __future__ import annotations

from typing import Any, Dict, List, Type

from .base import (
    STATUS_FAILED,
    STATUS_NOT_APPLICABLE,
    STATUS_OK,
    Candidate,
    LineMapping,
    Transformation,
    TransformOutcome,
)
from .if_else_swap import IfElseSwap

_REGISTRY: Dict[str, Type[Transformation]] = {}


def register_transformation(cls: Type[Transformation]) -> Type[Transformation]:
    _REGISTRY[cls.name] = cls
    return cls


def create_transformation(name: str, **options: Any) -> Transformation:
    if name not in _REGISTRY:
        raise ValueError(f"未登録の変換: {name!r} (登録済み: {', '.join(sorted(_REGISTRY))})")
    return _REGISTRY[name](**options)


def available_transformations() -> List[str]:
    return sorted(_REGISTRY)


register_transformation(IfElseSwap)

__all__ = [
    "STATUS_OK", "STATUS_NOT_APPLICABLE", "STATUS_FAILED",
    "Candidate", "LineMapping", "Transformation", "TransformOutcome",
    "IfElseSwap", "register_transformation", "create_transformation", "available_transformations",
]
