"""HuggingFace AutoModelForCausalLM adapter."""
from __future__ import annotations

import math
import time
from typing import List, Optional, Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from utils.logging_config import get_logger

from .base import InferenceOutput, ModelAdapter, TokenizedSequence

LOGGER = get_logger(__name__)


class HFCausalLMAdapter(ModelAdapter):
    """ModelAdapter backed by ``AutoModelForCausalLM``.

    Computes, per token position, the surprisal ``-ln p(token)`` and the
    predictive distribution entropy ``-Σ p ln p``. Full vocabulary
    distributions are never stored; only scalar values are returned.
    """

    model_kind = "hf_causal_lm"

    def __init__(
        self,
        model_name: str,
        revision: Optional[str] = None,
        device: Optional[str] = None,
        dtype: Optional[str] = None,
    ) -> None:
        """Initialize the adapter.

        Args:
            model_name: HuggingFace model id or local path.
            revision: Optional git revision/commit for reproducibility.
            device: ``"cuda"``, ``"cpu"`` or ``None`` (auto-detect).
            dtype: ``"float16"``, ``"bfloat16"`` or ``None``.
        """
        self._model_name = model_name
        self._revision = revision
        if device is not None:
            self._device = device
        elif torch.cuda.is_available():
            self._device = "cuda"
        elif torch.backends.mps.is_available():
            self._device = "mps"
        else:
            self._device = "cpu"
        self._dtype = dtype
        self._tokenizer = None
        self._model = None

    # ----- loading --------------------------------------------------------

    def load(self) -> None:
        """Load tokenizer and model onto the configured device."""
        LOGGER.info("Loading tokenizer: %s", self._model_name)
        self._tokenizer = AutoTokenizer.from_pretrained(
            self._model_name, revision=self._revision
        )

        torch_dtype = None
        if self._dtype == "float16":
            torch_dtype = torch.float16
        elif self._dtype == "bfloat16":
            torch_dtype = torch.bfloat16

        LOGGER.info("Loading model: %s (device=%s)", self._model_name, self._device)
        self._model = AutoModelForCausalLM.from_pretrained(
            self._model_name,
            revision=self._revision,
            torch_dtype=torch_dtype,
        )
        self._model.to(self._device)
        self._model.eval()

    def _ensure_loaded(self) -> None:
        if self._model is None or self._tokenizer is None:
            raise RuntimeError("Model is not loaded. Call load() first.")

    # ----- tokenization ---------------------------------------------------

    def tokenize(self, text: str) -> TokenizedSequence:
        """Tokenize text with character offset mapping."""
        self._ensure_loaded()
        encoded = self._tokenizer(
            text,
            return_offsets_mapping=True,
            add_special_tokens=False,
        )
        token_ids: List[int] = list(encoded["input_ids"])
        offsets: List[Tuple[int, int]] = [
            (int(s), int(e)) for s, e in encoded["offset_mapping"]
        ]
        token_strs = self._tokenizer.convert_ids_to_tokens(token_ids)
        return TokenizedSequence(
            token_ids=token_ids,
            token_strs=token_strs,
            offsets=offsets,
        )

    # ----- inference ------------------------------------------------------

    @torch.no_grad()
    def infer(self, token_ids: List[int]) -> InferenceOutput:
        """Compute per-token surprisal and entropy."""
        self._ensure_loaded()
        n = len(token_ids)
        if n == 0:
            return InferenceOutput(surprisal=[], entropy=[])

        # 💡 追記: 処理開始のログと時間計測スタート
        LOGGER.info("  -> [Full-sequence] Starting inference for %d tokens...", n)
        start_time = time.time()

        input_ids = torch.tensor([token_ids], device=self._device)
        outputs = self._model(input_ids=input_ids)
        # logits: (1, seq_len, vocab) -> distribution predicting position t+1.
        logits = outputs.logits[0].float()
        log_probs = torch.log_softmax(logits, dim=-1)
        probs = log_probs.exp()

        # Entropy of the predictive distribution at each position.
        entropy_all = -(probs * log_probs).sum(dim=-1)  # (seq_len,)

        surprisal: List[Optional[float]] = [None] * n
        entropy: List[Optional[float]] = [None] * n

        for t in range(1, n):
            target = token_ids[t]
            # Distribution at position t-1 predicts the token at position t.
            surprisal[t] = float(-log_probs[t - 1, target].item())
            entropy[t] = float(entropy_all[t - 1].item())

        # Guard against numerical issues.
        surprisal = [None if (v is not None and math.isnan(v)) else v for v in surprisal]
        entropy = [None if (v is not None and math.isnan(v)) else v for v in entropy]

        # 💡 追記: 経過時間の計算と終了ログ
        elapsed = time.time() - start_time
        LOGGER.info("  -> [Full-sequence] Finished inference in %.2f seconds.", elapsed)

        return InferenceOutput(surprisal=surprisal, entropy=entropy)

    @torch.no_grad()
    def infer_batch(self, batch_token_ids: List[List[int]], batch_size: int = 8) -> List[InferenceOutput]:
        """Compute surprisal and entropy for a batch of token id sequences."""
        self._ensure_loaded()
        total_batches = len(batch_token_ids)
        if total_batches == 0:
            return []

        LOGGER.info("  -> Starting TRUE batched inference for %d windows (batch_size=%d)...", total_batches, batch_size)
        start_time = time.time()

        # パディング用のトークンIDを取得（設定されていなければEOSを使う）
        pad_token_id = self._tokenizer.pad_token_id
        if pad_token_id is None:
            pad_token_id = self._tokenizer.eos_token_id or 0

        results: List[InferenceOutput] = []

        # 指定したバッチサイズ（例: 8件）ごとにチャンクとして処理し、メモリ爆発(OOM)を防ぐ
        for i in range(0, total_batches, batch_size):
            chunk = batch_token_ids[i: i + batch_size]
            max_len = max(len(seq) for seq in chunk)

            padded_inputs = []
            attention_masks = []
            for seq in chunk:
                pad_len = max_len - len(seq)
                # 後ろにパディングを追加し、マスクを設定 (1: 有効, 0: 無視)
                padded_inputs.append(seq + [pad_token_id] * pad_len)
                attention_masks.append([1] * len(seq) + [0] * pad_len)

            input_ids = torch.tensor(padded_inputs, device=self._device)
            attention_mask = torch.tensor(attention_masks, device=self._device)

            outputs = self._model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits.float()
            log_probs = torch.log_softmax(logits, dim=-1)
            probs = log_probs.exp()
            entropy_all = -(probs * log_probs).sum(dim=-1)

            # 結果を元の各シーケンスの長さに合わせて切り出し
            for j, seq in enumerate(chunk):
                n = len(seq)
                surprisal: List[Optional[float]] = [None] * n
                entropy: List[Optional[float]] = [None] * n

                for t in range(1, n):
                    target = seq[t]
                    surprisal[t] = float(-log_probs[j, t - 1, target].item())
                    entropy[t] = float(entropy_all[j, t - 1].item())

                surprisal = [None if (v is not None and math.isnan(v)) else v for v in surprisal]
                entropy = [None if (v is not None and math.isnan(v)) else v for v in entropy]
                results.append(InferenceOutput(surprisal=surprisal, entropy=entropy))

        elapsed = time.time() - start_time
        LOGGER.info("  -> [Batched] Finished %d windows in %.2f seconds.", total_batches, elapsed)

        return results

    # ----- metadata -------------------------------------------------------

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def model_revision(self) -> Optional[str]:
        return self._revision

    @property
    def tokenizer_name(self) -> str:
        return self._model_name