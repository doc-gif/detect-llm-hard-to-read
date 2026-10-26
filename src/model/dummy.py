"""動作確認専用のダミーモデル (研究の計測には使わない)。

torch / transformers やモデルの重みが無い環境 (Windows の解析用 PC、CI など) で
Phase 1 以降の処理を通しで確認するためのもの。CodeLlama 風のトークン文字列
(空白は ``▁``、改行は ``<0x0A>``) を返し、エントロピー・surprisal は直前2トークンと
現在のトークンの文字列から決まる疑似乱数 (OS や実行回に依らず同じ値) にする。
値に意味は無い。
"""
from __future__ import annotations

import re
import zlib
from typing import List, Optional

from .base import InferenceOutput, ModelAdapter, TokenizedSequence

# 改行 / 空白の連続 + 語 / 空白の連続 / 記号1文字
_TOKEN_RE = re.compile(r"\n| *[A-Za-z_][A-Za-z0-9_]*| *\d+| +|[^\sA-Za-z0-9_]")


class DummyAdapter(ModelAdapter):
    model_kind = "dummy"

    def __init__(self, model_name: str = "dummy", revision: Optional[str] = None,
                 device: Optional[str] = None, dtype: Optional[str] = None) -> None:
        self._model_name = model_name
        self._revision = revision
        self._vocab: dict = {}

    def load(self) -> None:
        pass

    def tokenize(self, text: str) -> TokenizedSequence:
        offsets, strs, ids = [], [], []
        for m in _TOKEN_RE.finditer(text):
            piece = m.group(0)
            tok = "<0x0A>" if piece == "\n" else piece.replace(" ", "▁")
            offsets.append((m.start(), m.end()))
            strs.append(tok)
            ids.append(self._vocab.setdefault(tok, len(self._vocab) + 3))
        return TokenizedSequence(token_ids=ids, token_strs=strs, offsets=offsets)

    def _value(self, ids: List[int], t: int) -> float:
        key = ",".join(str(i) for i in ids[max(0, t - 2):t + 1]).encode()
        return (zlib.crc32(key) % 3000) / 1000.0  # 0.0 - 3.0

    def infer(self, token_ids: List[int]) -> InferenceOutput:
        values = [self._value(token_ids, t) for t in range(len(token_ids))]
        return InferenceOutput(surprisal=[v * 1.5 for v in values], entropy=values)

    def infer_batch(self, batch_token_ids: List[List[int]]) -> List[InferenceOutput]:
        return [self.infer(ids) for ids in batch_token_ids]

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def model_revision(self) -> Optional[str]:
        return self._revision

    @property
    def tokenizer_name(self) -> str:
        return self._model_name
