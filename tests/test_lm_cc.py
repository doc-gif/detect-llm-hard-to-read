import pandas as pd

from analysis.macro import lm_cc, loc, perplexity
from analysis.macro.lm_cc_helper.calculate_code_with_boundaries import get_code_with_boundaries
from analysis.macro.lm_cc_helper.get_lm_cc import get_lmcc
from schema.records import ParquetSchema as PCol

# CodeLlama (SentencePiece) 形式のトークン列: "▁" は空白、"<0x0A>" は改行
TOKENS = ["def", "▁f", "(x):", "<0x0A>", "▁▁▁", "▁if", "▁x", ":", "<0x0A>", "▁▁▁▁▁▁▁", "▁return", "▁1", "<0x0A>", "▁▁▁", "▁return", "▁0"]


def _entropies(high_idx):
    return [2.0 if i in high_idx else 0.1 for i in range(len(TOKENS))]


def test_boundaries_count_semantic_units():
    _, lines, start_end, n_units = get_code_with_boundaries(TOKENS, _entropies({5, 10}), threshold=1.0)
    assert lines[0] == "def f(x):\n"
    assert start_end[0] == (0, 3)
    assert n_units == 3  # 境界 2 本で 3 ユニット


def test_lmcc_formula():
    tree = {"children": [{"children": [{"children": []}]}, {"children": []}]}
    # depth_sum = 1 + 2 + 3 + 2 = 8, branch = 3 -> 8 * 0.2 + 3 * 0.8
    assert get_lmcc(tree) == 8 * 0.2 + 3 * 0.8


def test_calculate_returns_pair_even_when_skipped():
    assert lm_cc.calculate(pd.DataFrame()) == (None, None)


def test_calculate_on_tokens():
    df = pd.DataFrame({PCol.TOKEN_STR: TOKENS, PCol.METRIC_ENTROPY: _entropies({5})})
    score, n_units = lm_cc.calculate(df, threshold=1.0)
    assert n_units == 2
    assert score > 0


def test_perplexity_and_loc():
    df = pd.DataFrame({PCol.METRIC_SURPRISAL: [0.0, 0.0, None], PCol.LINE: [1, 3, None]})
    assert perplexity.calculate(df) == 1.0
    assert loc.calculate(df) == 3
