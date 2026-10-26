"""Model adapter registry and factory.

Adapters are registered as ``"module:ClassName"`` strings and imported lazily,
so that importing this package (e.g. from tests or analysis code) does not
require ``torch`` / ``transformers`` to be installed.
"""
from __future__ import annotations

import importlib
from typing import Dict, Type, Union

from .base import InferenceOutput, ModelAdapter, TokenizedSequence

_REGISTRY: Dict[str, Union[str, Type[ModelAdapter]]] = {}


def register_model(kind: str, adapter_cls: Union[str, Type[ModelAdapter]]) -> None:
    """Register a ModelAdapter implementation under ``kind``.

    ``adapter_cls`` may be the class itself or a lazy ``"module:ClassName"``
    reference (module path relative to this package when it starts with ``.``).
    """
    _REGISTRY[kind] = adapter_cls


def _resolve(ref: Union[str, Type[ModelAdapter]]) -> Type[ModelAdapter]:
    if not isinstance(ref, str):
        return ref
    module_name, class_name = ref.split(":")
    module = importlib.import_module(module_name, package=__name__)
    return getattr(module, class_name)


def create_model_adapter(kind: str, **kwargs) -> ModelAdapter:
    """Instantiate a model adapter by registry key.

    Raises:
        ValueError: If ``kind`` is not registered.
    """
    if kind not in _REGISTRY:
        supported = ", ".join(sorted(_REGISTRY))
        raise ValueError(f"Unknown model kind '{kind}'. Supported: {supported}")
    return _resolve(_REGISTRY[kind])(**kwargs)


register_model("hf_causal_lm", ".hf_causal_lm:HFCausalLMAdapter")
# 動作確認専用 (値に意味は無い)。torch が無い環境で Phase 1 以降を通しで試すときに使う
register_model("dummy", ".dummy:DummyAdapter")


def __getattr__(name: str):
    # Backward compatibility: ``from model import HFCausalLMAdapter``
    if name == "HFCausalLMAdapter":
        return _resolve(_REGISTRY["hf_causal_lm"])
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "InferenceOutput",
    "ModelAdapter",
    "TokenizedSequence",
    "HFCausalLMAdapter",
    "register_model",
    "create_model_adapter",
]
