"""コミット済みの out/ と results/summaries を使った回帰テスト。

pipeline.process_file を実データで回し、既存の summary CSV と同じ値になることを確認する。
cyclomatic_complexity は Lizard のバージョンで値が揺れるので比較しない。
"""
import math

import pandas as pd
import pytest

import paths

pipeline = pytest.importorskip("analysis.pipeline")

CASES = [
    ("humaneval", "HumanEval_7"),
    ("humaneval", "HumanEval_120"),
    ("xcodeeval_apr", None),
    ("xcodeeval_code_translation", None),
]
COMPARE = ["ppl", "lm_cc", "lm_cc_density", "loc", "num_semantic_units", "total_tokens", "num_functions",
           "avg_first_token_surprisal", "avg_context_surprisal_gap", "cognitive_complexity"]


@pytest.fixture(scope="module")
def expected():
    csv = paths.summary_csv("_p67")
    if not csv.exists():
        pytest.skip(f"{csv} がありません")
    return pd.read_csv(csv)


@pytest.mark.parametrize("dataset,uid", CASES)
def test_process_file_matches_committed_summary(tmp_path, expected, dataset, uid):
    if uid is None:
        uid = sorted(p.stem.replace("result_", "") for p in (paths.OUT_DIR / dataset).glob("result_*.parquet"))[0]
    parquet = paths.OUT_DIR / dataset / f"result_{uid}.parquet"
    if not parquet.exists():
        pytest.skip(f"{parquet} がありません")

    got = pipeline.process_file(parquet, paths.OUT_DIR, pipeline.DEFAULT_THRESHOLD, enriched_dir=tmp_path)
    row = expected[(expected["dataset"] == dataset) & (expected["uid"] == uid)].iloc[0]

    for col in COMPARE:
        a, b = got[col], row[col]
        if b is None or (isinstance(b, float) and math.isnan(b)):
            assert a is None or (isinstance(a, float) and math.isnan(a)), col
        else:
            assert a == pytest.approx(b, rel=1e-9), col
    assert (tmp_path / dataset / parquet.name).exists()
