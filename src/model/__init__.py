"""Model adapter registry and factory."""
from __future__ import annotations

from typing import Dict, Type

from .base import InferenceOutput, ModelAdapter, TokenizedSequence
from .hf_causal_lm import HFCausalLMAdapter

_REGISTRY: Dict[str, Type[ModelAdapter]] = {}


def register_model(kind: str, adapter_cls: Type[ModelAdapter]) -> None:
    """Register a ModelAdapter implementation under ``kind``."""
    _REGISTRY[kind] = adapter_cls


def create_model_adapter(kind: str, **kwargs) -> ModelAdapter:
    """Instantiate a model adapter by registry key.

    Raises:
        ValueError: If ``kind`` is not registered.
    """
    if kind not in _REGISTRY:
        supported = ", ".join(sorted(_REGISTRY))
        raise ValueError(f"Unknown model kind '{kind}'. Supported: {supported}")
    return _REGISTRY[kind](**kwargs)


register_model("hf_causal_lm", HFCausalLMAdapter)

__all__ = [
    "InferenceOutput",
    "ModelAdapter",
    "TokenizedSequence",
    "HFCausalLMAdapter",
    "register_model",
    "create_model_adapter",
]