"""Recalculate saved metrics without loading a model or replacing old outputs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "analysis")]
from macro.lm_cc_helper.calculate_code_with_boudaries import get_code_with_boundaries
from macro.lm_cc_helper.code_block_processor import CodeBlockProcessor
from macro.lm_cc_helper.get_lm_cc import get_lmcc
from macro.loc import calculate as calculate_loc
from thresholds import SAVED_SUMMARY_THRESHOLDS


def recalculate(frame: pd.DataFrame, threshold: float, processor: CodeBlockProcessor) -> dict:
    clean = frame[frame["metric_surprisal"].notna()]
    tokens = clean["token_str"].tolist()
    text, _, spans, count = get_code_with_boundaries(
        tokens, clean["metric_entropy"].tolist(), threshold
    )
    tree = processor.parse_code_blocks(text, tokens, spans)
    return {"num_semantic_units": count, "lm_cc": get_lmcc(tree), "loc": calculate_loc(clean)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True, help="New directory; existing paths are refused.")
    parser.add_argument("--labels", nargs="+", choices=list(SAVED_SUMMARY_THRESHOLDS), default=list(SAVED_SUMMARY_THRESHOLDS))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    summaries = {}
    report = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "note": "Labels pXX are historical names. Effective numeric thresholds are recorded below.",
        "summaries": {},
    }
    for label in args.labels:
        path = ROOT / "results" / "summaries" / f"analysis_summary_{label}.csv"
        summary = pd.read_csv(path).set_index(["dataset", "uid"])
        if not summary.index.is_unique:
            raise ValueError(f"Duplicate summary keys: {path}")
        summaries[label] = summary
        report["summaries"][label] = {
            "path": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "threshold": SAVED_SUMMARY_THRESHOLDS[label],
            "rows": len(summary), "checked": 0,
            "matches": {metric: 0 for metric in ["num_semantic_units", "lm_cc", "loc"]},
        }
    processor = CodeBlockProcessor()
    mismatches = []
    input_manifest = []
    for path in sorted((ROOT / "out").rglob("result_*.parquet")):
        key = (path.parent.name, path.stem.removeprefix("result_"))
        frame = pd.read_parquet(path)
        input_manifest.append({"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        for label, summary in summaries.items():
            if key not in summary.index:
                continue
            values = recalculate(frame, SAVED_SUMMARY_THRESHOLDS[label], processor)
            saved = summary.loc[key]
            counts = report["summaries"][label]
            counts["checked"] += 1
            for metric, actual in values.items():
                expected = float(saved[metric])
                if math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-10):
                    counts["matches"][metric] += 1
                else:
                    mismatches.append({"label": label, "dataset": key[0], "uid": key[1], "metric": metric, "saved": expected, "recomputed": actual})
    for label, summary in summaries.items():
        checked = report["summaries"][label]["checked"]
        if checked != len(summary):
            raise ValueError(f"{label}: found {checked} Parquet inputs for {len(summary)} saved rows")
    (args.output_dir / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    (args.output_dir / "input_manifest.json").write_text(json.dumps(input_manifest, indent=2) + "\n")
    pd.DataFrame(mismatches, columns=["label", "dataset", "uid", "metric", "saved", "recomputed"]).to_csv(args.output_dir / "mismatches.csv", index=False)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
