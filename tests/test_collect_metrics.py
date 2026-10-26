"""Phase 1 (collect_metrics.collect) をダミーモデルで検証する。torch / transformers は不要。"""
import re
from typing import List, Optional

import pandas as pd

import collect_metrics
from model.base import InferenceOutput, ModelAdapter, TokenizedSequence
from writer import create_writer

SOURCE = '''import os


def add(a, b):
    s = "é"
    return a + b


x = add(1, 2)
'''


class WhitespaceModel(ModelAdapter):
    """空白以外の連続文字列を 1 トークンとみなし、surprisal = 文脈内の位置 とするダミー。"""

    model_kind = "fake"

    def load(self) -> None:
        pass

    def tokenize(self, text: str) -> TokenizedSequence:
        spans = [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]
        return TokenizedSequence(
            token_ids=list(range(len(spans))),
            token_strs=[text[s:e] for s, e in spans],
            offsets=spans,
        )

    def infer(self, token_ids: List[int]) -> InferenceOutput:
        values = [float(i) for i in range(len(token_ids))]
        return InferenceOutput(surprisal=values, entropy=[v / 10 for v in values])

    def infer_batch(self, batch_token_ids):
        return [self.infer(ids) for ids in batch_token_ids]

    @property
    def model_name(self) -> str:
        return "fake"

    @property
    def model_revision(self) -> Optional[str]:
        return None

    @property
    def tokenizer_name(self) -> str:
        return "fake"


def _collect(tmp_path):
    src = tmp_path / "sample.py"
    src.write_text(SOURCE, encoding="utf-8")
    return collect_metrics.collect(src, WhitespaceModel(), "function_scope", project="t")


def test_records_have_positions_and_ast_info(tmp_path):
    result = _collect(tmp_path)
    by_str = {}
    for r in result.tokens:
        by_str.setdefault(r.token_str, r)

    assert result.metadata.total_tokens == len(result.tokens)
    assert by_str["import"].line == 1 and by_str["import"].function_id is None
    assert by_str["def"].is_function_start and by_str["def"].function_id == "add"
    assert by_str["return"].function_id == "add" and by_str["return"].is_statement_start
    assert by_str["return"].nesting_depth == 1
    # 非 ASCII 文字 "é" の後ろでも正しいノードを指す (Tree-sitter はバイト列で数える)
    assert by_str['"é"'].ast_type in {"string", "string_start"}


def test_isolated_surprisal_is_aligned_to_function_window(tmp_path):
    result = _collect(tmp_path)
    in_func = [r for r in result.tokens if r.function_id == "add"]
    outside = [r for r in result.tokens if r.function_id is None]
    # 関数ウィンドウ内で再推論した値 = ウィンドウ内での位置 (0, 1, 2, ...)
    assert [r.token_metrics["isolated_surprisal"] for r in in_func] == [float(i) for i in range(len(in_func))]
    assert all(r.token_metrics["isolated_surprisal"] is None for r in outside)


def test_parquet_writer_roundtrip(tmp_path):
    result = _collect(tmp_path)
    out = tmp_path / "result_sample.parquet"
    create_writer("parquet").write(result, out)
    df = pd.read_parquet(out)
    assert len(df) == len(result.tokens)
    assert {"metric_surprisal", "metric_isolated_surprisal", "meta_file", "is_function_start"} <= set(df.columns)
    assert df["meta_file"].iloc[0] == str(tmp_path / "sample.py")


class LeadingSpaceModel(WhitespaceModel):
    """SentencePiece 風に、直前の空白をトークンの先頭に含めるダミー ("▁return" 相当)。"""

    def tokenize(self, text: str) -> TokenizedSequence:
        spans = [(m.start(), m.end()) for m in re.finditer(r"\s*\S+", text)]
        return TokenizedSequence(
            token_ids=list(range(len(spans))),
            token_strs=[text[s:e] for s, e in spans],
            offsets=spans,
        )


def test_statement_start_with_leading_space_tokens(tmp_path):
    src = tmp_path / "sample.py"
    src.write_text("def f(x):\n    if x:\n        return 1\n    y = 2\n", encoding="utf-8")
    result = collect_metrics.collect(src, LeadingSpaceModel(), "function_scope", project="t")
    flags = {r.token_str.strip(): r for r in result.tokens}

    assert flags["if"].is_statement_start and flags["if"].ast_type == "if"
    assert flags["return"].is_statement_start
    assert flags["y"].is_statement_start  # 代入文 (expression_statement) の先頭
    assert not flags["x:"].is_statement_start  # if 条件の途中は文の先頭ではない
    assert flags["if"].nesting_depth == 1 and flags["return"].nesting_depth == 2
