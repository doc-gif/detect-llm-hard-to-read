"""変換前後の比較 (SU・LOC・トークン対応) と動作確認の判定のテスト。"""
import pandas as pd
import pytest

import paths
from equivalence import behavior, compare
from equivalence.transforms import create_transformation


@pytest.mark.parametrize("uid", ["HumanEval_0", "HumanEval_7", "HumanEval_120"])
def test_file_metrics_match_existing_summary(uid):
    """SU 数・LOC・トークン数が Phase 2 の summary CSV と同じ定義になっている。"""
    parquet = paths.OUT_DIR / "humaneval" / f"result_{uid}.parquet"
    csv = paths.summary_csv("_p67")
    if not parquet.exists() or not csv.exists():
        pytest.skip("コミット済みの out/ / summary が無い")
    row = pd.read_csv(csv).set_index(["dataset", "uid"]).loc[("humaneval", uid)]
    m = compare.file_metrics(compare.clean(pd.read_parquet(parquet)), {"p67": 0.6813})["metrics"]
    assert m["su_count_p67"] == row["num_semantic_units"]
    assert m["loc"] == row["loc"]
    assert m["total_tokens"] == row["total_tokens"]
    assert m["lm_cc_p67"] == pytest.approx(row["lm_cc"])
    assert m["ppl"] == pytest.approx(row["ppl"])


def _fake_tokens(source, entropy_of):
    """1行を「語ごと + 改行」のトークンにした Phase 1 風の表。"""
    rows = []
    for ln, text in enumerate(source.split("\n"), 1):
        parts = text.split(" ")
        col = 0
        for k, p in enumerate(parts):
            tok = ("\u2581" if k else "") + p
            if tok:
                rows.append({"token_str": tok, "line": ln, "column": col})
            col += len(p) + 1
        if ln < len(source.split("\n")):
            rows.append({"token_str": "<0x0A>", "line": ln, "column": len(text)})
    df = pd.DataFrame(rows)
    df["idx"] = range(len(df))
    df["metric_entropy"] = [entropy_of(r) for _, r in df.iterrows()]
    df["metric_surprisal"] = df["metric_entropy"]
    return df


SRC = "def f(x):\n    if x:\n        a = 1\n    else:\n        a = 2\n    return a\n"


def test_compare_pair_aligns_by_line_map_not_by_index():
    t = create_transformation("if_else_swap")
    (cand,) = t.find_candidates(SRC)
    out = t.apply(SRC, cand)
    line_map = [m.__dict__ for m in out.line_map]
    # "1" を含む行だけエントロピーが高い → 変換前は3行目、変換後は5行目に SU 境界
    high = lambda r: 2.0 if r["token_str"].endswith("1") else 0.1  # noqa: E731
    before, after = _fake_tokens(SRC, high), _fake_tokens(out.transformed_source, high)
    res = compare.compare_pair(before, after, SRC, out.transformed_source, line_map, {"p67": 0.6813})
    s = res["summary"]
    assert s["loc_equal"] and s["su_count_p67_delta"] == 0 and s["su_change_p67"] == "unchanged"
    units_b = res["units"]["p67"]["before"]
    units_a = res["units"]["p67"]["after"]
    assert [u["start_line"] for u in units_b] == [1, 3]
    assert [u["start_line"] for u in units_a] == [1, 5]
    lines = res["lines"].set_index("orig_line")
    assert lines.loc[3, "new_line"] == 5 and lines.loc[3, "boundary_p67_before"] and lines.loc[3, "boundary_p67_after"]
    al = res["token_alignment"]
    # if の行: "not" だけが変換後のみのトークン
    hdr = al[al["region"] == "if_header"]
    assert list(hdr.loc[hdr["match"] == "only_after", "after_token"]) == ["\u2581not"]
    # 移動した本体はトークンが同じ並びで対応している
    body = al[al["region"].isin(["then_body", "else_body"])]
    assert (body["match"] == "equal").all() and (body["line_alignment"] == "identical_tokens").all()
    # トークン番号は一致していない (番号同士で対応づけていない)
    assert (body["before_idx"] != body["after_idx"]).any()


def test_su_count_change_is_recorded_for_increase():
    t = create_transformation("if_else_swap")
    (cand,) = t.find_candidates(SRC)
    out = t.apply(SRC, cand)
    high_not = lambda r: 2.0 if r["token_str"] == "\u2581not" else 0.1  # noqa: E731
    res = compare.compare_pair(_fake_tokens(SRC, high_not), _fake_tokens(out.transformed_source, high_not),
                               SRC, out.transformed_source, [m.__dict__ for m in out.line_map], {"p67": 0.6813})
    assert res["summary"]["su_count_p67_delta"] == 1
    assert res["summary"]["su_change_p67"] == "increased"
    reg = res["regions"].set_index("region")
    assert reg.loc["if_header", "n_boundary_lines_p67_delta"] == 1


def test_behavior_compare_detects_mismatch_and_match():
    cases = [{"case_id": "hidden:0", "kind": "stdin", "input": "3\n", "expected": ["6"]},
             {"case_id": "hidden:1", "kind": "stdin", "input": "-1\n", "expected": ["-2"]}]
    orig = "n = int(input())\nif n > 0:\n    print(n * 2)\nelse:\n    print(n * 2)\n"
    good = "n = int(input())\nif not (n > 0):\n    print(n * 2)\nelse:\n    print(n * 2)\n"
    bad = "n = int(input())\nif not (n > 0):\n    print(n * 3)\nelse:\n    print(n * 2)\n"
    o = behavior.observe_all(orig, cases, 10)
    assert all(x["matches_expected"] for x in o)
    assert behavior.compare(cases, o, behavior.observe_all(good, cases, 10))["status"] == behavior.STATUS_MATCH
    res = behavior.compare(cases, o, behavior.observe_all(bad, cases, 10))
    assert res["status"] == behavior.STATUS_MISMATCH and res["n_equal"] == 1
    assert behavior.compare([], [], [])["status"] == behavior.STATUS_UNVERIFIED


def test_behavior_timeout_is_unverified():
    cases = [{"case_id": "hidden:0", "kind": "stdin", "input": "", "expected": []}]
    loop = "while True:\n    pass\n"
    o = behavior.observe_all(loop, cases, 1)
    assert o[0]["timeout"]
    assert behavior.compare(cases, o, o)["status"] == behavior.STATUS_UNVERIFIED
