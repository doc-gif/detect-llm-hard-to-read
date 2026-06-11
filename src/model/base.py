"""Abstract base class for model adapters."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass(slots=True)
class TokenizedSequence:
    """Tokenization output aligned with character offsets."""
    token_ids: List[int]
    token_strs: List[str]
    offsets: List[Tuple[int, int]]


@dataclass(slots=True)
class InferenceOutput:
    """Per-token scalar metrics from a single forward pass."""
    surprisal: List[Optional[float]]
    entropy: List[Optional[float]]


class ModelAdapter(ABC):
    """Encapsulates tokenizer/model loading and scalar metric computation."""

    #: Registry key (e.g. ``"hf_causal_lm"``).
    model_kind: str = "abstract"

    @abstractmethod
    def load(self) -> None:
        """Load tokenizer and model weights into memory."""

    @abstractmethod
    def tokenize(self, text: str) -> TokenizedSequence:
        """Tokenize ``text`` with character offset mapping."""

    @abstractmethod
    def infer(self, token_ids: List[int]) -> InferenceOutput:
        """Compute surprisal and entropy for a single token id sequence."""

    @abstractmethod
    def infer_batch(self, batch_token_ids: List[List[int]]) -> List[InferenceOutput]:
        """Compute surprisal and entropy for a batch of token id sequences.

        This is crucial for efficiently calculating 'isolated_surprisal'
        for multiple functions in a single forward pass.
        """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Resolved model name/identifier."""

    @property
    @abstractmethod
    def model_revision(self) -> Optional[str]:
        """Resolved model revision/commit, if available."""

    @property
    @abstractmethod
    def tokenizer_name(self) -> str:
        """Resolved tokenizer name/identifier."""