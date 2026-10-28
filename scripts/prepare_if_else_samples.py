"""Select, copy and transform samples without loading a language model."""
from __future__ import annotations

import argparse
import ast
import csv
import difflib
import hashlib
import json
import platform
import random
import re
import sys
import warnings
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from importlib import metadata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import paths
from equivalence.transforms import IfElseSwap

SEED = 20261026
QUOTAS = {"short": 3, "medium": 4, "long": 3}
MINIMAL = {
    "positive": ("x = int(input())\nif x > 0:\n    print(1)\nelse:\n    print(0)\n",
                 [("-1\n", "0\n"), ("0\n", "0\n"), ("1\n", "1\n")]),
    "even": ("x = int(input())\nif x % 2 == 0:\n    print(1)\nelse:\n    print(0)\n",
             [("-2\n", "1\n"), ("0\n", "1\n"), ("1\n", "0\n")]),
    "both_positive": (
        "a, b = map(int, input().split())\nif a > 0 and b > 0:\n    print(1)\nelse:\n    print(0)\n",
        [("1 1\n", "1\n"), ("1 0\n", "0\n"), ("0 1\n", "0\n"), ("-1 -1\n", "0\n")]),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def quantile(values: list[int], probability: Fraction) -> Fraction:
    """Linear interpolation at (N - 1) * p; preserve exact boundaries."""
    values = sorted(values)
    position = (len(values) - 1) * probability
    index = position.numerator // position.denominator
    if index == len(values) - 1:
        return Fraction(values[index])
    return values[index] + (position - index) * (values[index + 1] - values[index])


def select(rows: list[dict], seed: int) -> tuple[list[dict], dict]:
    eligible = [r for r in rows if r["eligible"]]
    if not eligible:
        raise ValueError("No eligible Python inputs")
    cuts = [quantile([r["selection_loc"] for r in eligible], p)
            for p in [Fraction(1, 3), Fraction(2, 3)]]
    groups = {name: [] for name in QUOTAS}
    for row in eligible:
        row["group"] = ("short" if row["selection_loc"] <= cuts[0]
                        else "medium" if row["selection_loc"] <= cuts[1] else "long")
        groups[row["group"]].append(row)
    rng = random.Random(seed)
    selected, orders = [], {}
    for name, quota in QUOTAS.items():
        pool = sorted(groups[name], key=lambda r: r["uid"])
        if len(pool) < quota:
            raise ValueError(f"Insufficient candidates in {name}: {len(pool)} < {quota}")
        rng.shuffle(pool)
        orders[name] = [r["uid"] for r in pool]
        for rank, row in enumerate(pool, 1):
            row.update(draw_rank=rank, selected=rank <= quota)
        selected.extend(pool[:quota])
    return selected, {"quantile_method": "linear at (N-1)*p; exact rational arithmetic",
                      "cutpoints": [str(c) for c in cuts], "cutpoint_values": [float(c) for c in cuts],
                      "group_sizes": {k: len(v) for k, v in groups.items()},
                      "draw_order_including_reserves": orders}


def first_outcome(source: str, transform: IfElseSwap):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        ast.parse(source)
    candidates = transform.find_candidates(source)
    candidates.sort(key=lambda c: (c.start_line, c.index))
    candidate = next((c for c in candidates if c.status == "ok"), None)
    return candidates, None if candidate is None else transform.apply(source, candidate)


def save_pair(root: Path, uid: str, source: str, outcome, cases: list, record=None) -> dict:
    root.mkdir(parents=True)
    original = source.encode("utf-8")
    swapped = outcome.transformed_source.encode("utf-8")
    assert source != outcome.transformed_source
    assert len(source.splitlines()) == len(outcome.transformed_source.splitlines())
    (root / "original.py").write_bytes(original)
    (root / "swapped.py").write_bytes(swapped)
    diff = difflib.unified_diff(source.splitlines(keepends=True),
                                outcome.transformed_source.splitlines(keepends=True),
                                fromfile="original.py", tofile="swapped.py")
    (root / "diff.patch").write_text("".join(
        line if line.endswith("\n") else line + "\n\\ No newline at end of file\n"
        for line in diff), encoding="utf-8")
    write_json(root / "transform.json", outcome.to_record())
    write_json(root / "tests.json", {"cases": cases, "execution_status": "not_run"})
    if record is not None:
        write_json(root / "source_record.json", record)
    return {"uid": uid, "path": str(root), "original_sha256": digest(original),
            "swapped_sha256": digest(swapped), "if_line": outcome.candidate.start_line,
            "variant_id": outcome.candidate.variant_id, "selection_loc": len(source.splitlines()),
            "syntax_ast_line_checks": outcome.checks, "behavior_status": "not_run",
            "measurement_status": "not_run", "n_tests": len(cases)}


def prepare(source_jsonl: Path, output_dir: Path, seed: int = SEED) -> dict:
    if output_dir.exists():
        raise FileExistsError(f"Output already exists: {output_dir}")
    raw = source_jsonl.read_bytes()
    transform = IfElseSwap(unwrap_not=True, negation_style="auto")
    rows, payloads, seen = [], {}, set()
    for line_number, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        uid = record["code_uid"]
        if not isinstance(uid, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", uid) or uid in seen:
            raise ValueError(f"Invalid or duplicate ID at line {line_number}: {uid}")
        seen.add(uid)
        source = record["source_code"]
        row = {"uid": uid, "source_jsonl_line": line_number, "selection_loc": len(source.splitlines()),
               "source_sha256": digest(source.encode("utf-8")), "eligible": False,
               "reason": "", "if_line": "", "group": "", "draw_rank": "", "selected": False}
        rows.append(row)
        if record.get("lang_cluster") != "Python":
            row["reason"] = "not_python"
            continue
        try:
            candidates, outcome = first_outcome(source, transform)
        except SyntaxError as exc:
            row["reason"] = f"python_parse_failed: {exc.msg} (line {exc.lineno})"
            continue
        if outcome is None:
            reasons = sorted({c.reason for c in candidates if c.reason})
            row["reason"] = "no_applicable_if_else: " + ("; ".join(reasons) or "no_if")
            continue
        row["if_line"] = outcome.candidate.start_line
        if outcome.status != "ok":
            row["reason"] = "first_candidate_failed: " + str(outcome.reason)
            continue
        cases = record.get("hidden_unit_tests") or []
        if isinstance(cases, str):
            cases = json.loads(cases)
        if not isinstance(cases, list) or not cases or any(
            not isinstance(c, dict) or not isinstance(c.get("input"), str)
            or not (isinstance(c.get("output"), str) or (isinstance(c.get("output"), list)
                    and all(isinstance(value, str) for value in c["output"]))) for c in cases
        ):
            row["reason"] = "missing_or_invalid_hidden_tests"
            continue
        row["eligible"], row["reason"] = True, "eligible"
        payloads[uid] = (record, source, outcome, cases)
    selected, selection = select(rows, seed)
    # Freeze the IDs before copying selected inputs or creating the minimal examples.
    output_dir.mkdir(parents=True)
    selection.update(seed=seed, quotas=QUOTAS, random_generator="random.Random / Mersenne Twister",
                     python=platform.python_version(),
                     selected_ids=[r["uid"] for r in selected],
                     replacements_applied=False, selection_uses_model_metrics=False)
    write_json(output_dir / "selection.json", selection)
    write_csv(output_dir / "candidates.csv", sorted(rows, key=lambda r: r["uid"]))
    samples = []
    for row in selected:
        record, source, outcome, cases = payloads[row["uid"]]
        sample = save_pair(output_dir / "xcodeeval" / row["uid"], row["uid"], source, outcome, cases, record)
        sample.update(dataset="xcodeeval_code_translation", group=row["group"], draw_rank=row["draw_rank"],
                      source_jsonl_line=row["source_jsonl_line"])
        sample["path"] = str(Path(sample["path"]).relative_to(output_dir))
        samples.append(sample)
    for uid, (source, tests) in MINIMAL.items():
        _, outcome = first_outcome(source, transform)
        assert outcome is not None and outcome.status == "ok"
        cases = [{"input": x, "output": y} for x, y in tests]
        sample = save_pair(output_dir / "minimal" / uid, uid, source, outcome, cases)
        sample.update(dataset="minimal", group="minimal", draw_rank="", source_jsonl_line="")
        sample["path"] = str(Path(sample["path"]).relative_to(output_dir))
        samples.append(sample)
    write_csv(output_dir / "samples.csv", [{k: s[k] for k in [
        "dataset", "uid", "group", "selection_loc", "if_line", "path", "original_sha256", "swapped_sha256"
    ]} for s in samples])
    manifest = {"schema_version": 1, "created_at": datetime.now(timezone.utc).isoformat(),
                "source_jsonl": str(source_jsonl), "source_jsonl_sha256": digest(raw),
                "source_records": len(rows), "eligible_records": sum(r["eligible"] for r in rows),
                "exclusion_counts": dict(Counter(r["reason"].split(":")[0] for r in rows if not r["eligible"])),
                "selection_loc_definition": "len(source_code.splitlines()); blank/comment lines included",
                "transform": transform.describe(), "samples": samples,
                "behavior_status": "not_run", "measurement_status": "not_run",
                "script_sha256": digest(Path(__file__).read_bytes()),
                "transform_impl_sha256": digest((paths.PROJECT_ROOT / "src/equivalence/transforms/if_else_swap.py").read_bytes()),
                "runtime": {"python": platform.python_version(), "tree-sitter": metadata.version("tree-sitter"),
                            "tree-sitter-python": metadata.version("tree-sitter-python")},
                "files": {str(p.relative_to(output_dir)): digest(p.read_bytes())
                          for p in sorted(output_dir.rglob("*")) if p.is_file()}}
    write_json(output_dir / "manifest.json", manifest)
    assert digest(source_jsonl.read_bytes()) == manifest["source_jsonl_sha256"]
    return manifest


def verify(output_dir: Path) -> dict:
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    for relative, expected in manifest["files"].items():
        if digest((output_dir / relative).read_bytes()) != expected:
            raise ValueError(f"Hash mismatch: {relative}")
    for sample in manifest["samples"]:
        original = (output_dir / sample["path"] / "original.py").read_text(encoding="utf-8")
        swapped = (output_dir / sample["path"] / "swapped.py").read_text(encoding="utf-8")
        assert len(original.splitlines()) == len(swapped.splitlines())
        ast.parse(original)
        ast.parse(swapped)
    return {"samples": len(manifest["samples"]), "verified_files": len(manifest["files"]),
            "behavior_status": manifest["behavior_status"], "measurement_status": manifest["measurement_status"]}


def main() -> None:
    parser = argparse.ArgumentParser(description="if-else実験用の13組を準備する。モデルは読み込まない。")
    parser.add_argument("--source-jsonl", type=Path, default=paths.LM_CC_ROOT /
                        "dataset/xcodeeval/code_translation/xcodeeval_codetranslation_test_filtered.jsonl")
    parser.add_argument("--output-dir", type=Path, default=paths.PROJECT_ROOT /
                        "experiments/if_else_swap_translation_20261026")
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--verify", action="store_true", help="既存の出力のハッシュと構文を確認する")
    args = parser.parse_args()
    if not args.verify:
        prepare(args.source_jsonl, args.output_dir, args.seed)
    print(json.dumps(verify(args.output_dir), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
