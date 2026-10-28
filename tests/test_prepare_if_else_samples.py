"""Checks for reproducible sample selection and isolated preparation."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/prepare_if_else_samples.py"
spec = importlib.util.spec_from_file_location("prepare_if_else_samples", SCRIPT)
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


def rows():
    return [{"uid": f"task_{i:02d}", "selection_loc": loc, "eligible": True}
            for i, loc in enumerate([5] * 4 + [10] * 4 + [20] * 4)]


def test_selection_is_reproducible_and_does_not_split_equal_loc():
    chosen, info = prepare.select(rows(), prepare.SEED)
    reversed_chosen, reversed_info = prepare.select(list(reversed(rows())), prepare.SEED)
    assert [r["uid"] for r in chosen] == [r["uid"] for r in reversed_chosen]
    assert info == reversed_info
    assert {group: sum(r["group"] == group for r in chosen) for group in prepare.QUOTAS} == prepare.QUOTAS
    assert {r["selection_loc"]: r["group"] for r in chosen} == {5: "short", 10: "medium", 20: "long"}


def test_tied_boundaries_with_too_few_candidates_stop_selection():
    tied = [{"uid": str(i), "selection_loc": 5, "eligible": True} for i in range(12)]
    with pytest.raises(ValueError, match="Insufficient candidates"):
        prepare.select(tied, prepare.SEED)


def test_prepare_preserves_exact_inputs_and_detects_modified_copies(tmp_path):
    source = tmp_path / "source.jsonl"
    records = []
    for i in range(15):
        code = "\n" * i + "x = int(input())\nif x > 0:\n    print(1)\nelse:\n    print(0)\n"
        code = code.rstrip("\n")
        records.append({"code_uid": f"task_{i:02d}", "source_code": code, "lang_cluster": "Python",
                        "hidden_unit_tests": json.dumps([{"input": "1\n", "output": ["1"]}])})
    original = "\n".join(json.dumps(r) for r in records).encode()
    source.write_bytes(original)
    output = tmp_path / "output"
    manifest = prepare.prepare(source, output)
    assert source.read_bytes() == original
    assert prepare.verify(output)["samples"] == 13
    assert manifest["measurement_status"] == "not_run"
    assert not list(output.rglob("*.parquet"))
    by_id = {r["code_uid"]: r for r in records}
    for item in manifest["samples"][:10]:
        assert (output / item["path"] / "original.py").read_bytes() == by_id[item["uid"]]["source_code"].encode()
        assert "No newline at end of file" in (output / item["path"] / "diff.patch").read_text()
    with pytest.raises(FileExistsError):
        prepare.prepare(source, output)
    (output / manifest["samples"][0]["path"] / "original.py").write_text("changed")
    with pytest.raises(ValueError, match="Hash mismatch"):
        prepare.verify(output)


@pytest.mark.parametrize("uid", list(prepare.MINIMAL))
def test_minimal_examples_exercise_both_branches_with_expected_results(tmp_path, uid):
    source, cases = prepare.MINIMAL[uid]
    _, outcome = prepare.first_outcome(source, prepare.IfElseSwap())
    assert outcome.status == "ok"
    assert set(expected for _, expected in cases) == {"0\n", "1\n"}
    for version, code in [("original", source), ("swapped", outcome.transformed_source)]:
        program = tmp_path / f"{version}.py"
        program.write_text(code)
        for stdin, expected in cases:
            result = subprocess.run([sys.executable, str(program)], input=stdin, text=True,
                                    capture_output=True, timeout=2, check=True)
            assert result.stdout == expected
