"""Run the frozen if-else sample package; reuse the existing metric definitions."""
from __future__ import annotations

from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import csv
import fcntl
import hashlib
from importlib import metadata
import json
import math
from pathlib import Path
import platform
import tomllib

import paths


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False,
                               default=lambda v: v.item() if hasattr(v, "item") else str(v)) + "\n",
                    encoding="utf-8")
    temp.replace(path)


def environment():
    versions = {}
    for name in ("torch", "transformers", "pandas", "pyarrow", "tree-sitter", "tree-sitter-python"):
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = None
    return {"host": platform.node(), "python": platform.python_version(), "packages": versions}


def safe_child(root: Path, relative: str) -> Path:
    p = root / relative
    if not p.resolve().is_relative_to(root.resolve()) or Path(relative).is_absolute():
        raise ValueError(f"Path outside package: {relative}")
    return p


class SampleRun:
    def __init__(self, config_path: Path, project_root: Path = paths.PROJECT_ROOT):
        self.project = project_root
        self.config_path = config_path
        self.config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        exp = self.config["experiment"]
        self.package = safe_child(project_root, exp["package"])
        self.output = safe_child(project_root, exp["output"])
        if self.output.resolve().is_relative_to(self.package.resolve()):
            raise ValueError("Output must be outside the frozen input package")
        self.manifest_path = self.package / "manifest.json"
        self.manifest = read(self.manifest_path)
        if not self.manifest:
            raise FileNotFoundError(self.manifest_path)
        self.samples = self.manifest["samples"]
        self.keys = [f'{s["dataset"]}/{s["uid"]}' for s in self.samples]
        if len(set(self.keys)) != len(self.keys):
            raise ValueError("Duplicate dataset/uid in sample manifest")
        if dict(Counter(s["dataset"] for s in self.samples)) != exp["expected_counts"]:
            raise ValueError("Unexpected sample count or dataset")
        for key in self.keys:
            safe_child(self.output, key)
        code_paths = list((project_root / "src").rglob("*.py"))
        code_paths += [project_root / "scripts/run_if_else_samples.py"]
        self.binding = {"config": self.config, "input_manifest_sha256": sha(self.manifest_path),
                        "code_sha256": {str(p.relative_to(project_root)): sha(p)
                                        for p in sorted(code_paths) if p.is_file()}}
        self.verify_inputs()
        self.check_binding()

    def verify_inputs(self):
        for rel, expected in self.manifest["files"].items():
            p = safe_child(self.package, rel)
            if not p.is_file() or sha(p) != expected:
                raise ValueError(f"Input hash mismatch: {rel}")
        for s in self.samples:
            folder = safe_child(self.package, s["path"])
            for version in ("original", "swapped"):
                if sha(folder / f"{version}.py") != s[f"{version}_sha256"]:
                    raise ValueError(f"Input hash mismatch: {s['uid']}/{version}")

    def check_binding(self):
        existing = read(self.output / "run.json")
        if existing is not None and existing != self.binding:
            raise ValueError("Conditions, inputs or code changed; use a new experiment.output")

    @contextmanager
    def locked(self):
        self.output.mkdir(parents=True, exist_ok=True)
        with (self.output / "run.lock").open("a+") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise RuntimeError("Another stage is running; wait for it to finish") from exc
            self.check_binding()
            if not (self.output / "run.json").exists():
                write(self.output / "run.json", self.binding)
            yield

    def states(self, stage):
        return read(self.output / "status" / f"{stage}.json", {})

    def set_state(self, stage, key, status, **extra):
        states = self.states(stage)
        states[key] = {"status": status, "updated_at": datetime.now(timezone.utc).isoformat(), **extra}
        write(self.output / "status" / f"{stage}.json", states)

    def cached(self, stage, key):
        state = self.states(stage).get(key, {})
        if state.get("status") != "ok":
            return False
        if not state.get("files"):
            raise ValueError(f"Missing output hashes: {stage}/{key}")
        for rel, expected in state["files"].items():
            p = safe_child(self.output, rel)
            if not p.is_file() or sha(p) != expected:
                raise ValueError(f"Output hash mismatch: {rel}")
        return True

    def done(self, stage, key, files, **extra):
        self.set_state(stage, key, "ok", files={str(p.relative_to(self.output)): sha(p) for p in files}, **extra)

    def log(self, stage, **extra):
        with (self.output / "runs.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"stage": stage, "at": datetime.now(timezone.utc).isoformat(),
                                     "environment": environment(), **extra}, ensure_ascii=False) + "\n")

    def behavior(self):
        from equivalence import behavior

        failures = []
        cfg = self.config["behavior"]
        for s, key in zip(self.samples, self.keys):
            if self.cached("behavior", key):
                continue
            folder = self.package / s["path"]
            raw_cases = read(folder / "tests.json")["cases"]
            cases = []
            for i, case in enumerate(raw_cases):
                expected = case["output"]
                if isinstance(expected, str):
                    expected = [expected.strip()] if expected.strip() else []
                cases.append({"case_id": str(i), "kind": "stdin", "input": case["input"], "expected": expected})
            sources = [(folder / f"{v}.py").read_bytes().decode("utf-8") for v in ("original", "swapped")]
            original = behavior.observe_all(sources[0], cases, cfg["timeout_sec"], cfg["workers"])
            swapped = behavior.observe_all(sources[1], cases, cfg["timeout_sec"], cfg["workers"],
                                           skip=[bool(o.get("timeout")) for o in original])
            result = behavior.compare(cases, original, swapped)
            result["baseline_runtime_failures"] = sum(o.get("returncode") != 0 for o in original)
            result["swapped_runtime_failures"] = sum(o.get("returncode") != 0 for o in swapped)
            result["baseline_expected_mismatches"] = sum(not o.get("matches_expected") for o in original)
            result["swapped_expected_mismatches"] = sum(not o.get("matches_expected") for o in swapped)
            result["expected_output_matches"] = (result["baseline_expected_mismatches"] ==
                                                   result["swapped_expected_mismatches"] == 0)
            result["ready_for_measurement"] = (
                result["status"] == "match" and
                result["baseline_runtime_failures"] == result["swapped_runtime_failures"] == 0 and
                (not cfg["require_expected_output"] or result["expected_output_matches"]))
            result["environment"] = environment()
            file = self.output / "behavior" / f"{key}.json"
            write(file, result)
            if result["ready_for_measurement"]:
                self.done("behavior", key, [file], n_cases=len(cases),
                          expected_output_matches=result["expected_output_matches"])
            else:
                self.set_state("behavior", key, "failed", result=result["status"],
                               reason="Outputs differ, a process failed, timed out, or expected output was not matched")
                failures.append(key)
            print(f"behavior {key}: {'ok' if result['ready_for_measurement'] else 'failed'} ({len(cases)} cases)", flush=True)
        summary = []
        for sample, key in zip(self.samples, self.keys):
            result = read(self.output / "behavior" / f"{key}.json")
            summary.append({"dataset": sample["dataset"], "uid": sample["uid"],
                            **{name: result[name] for name in ("status", "n_cases", "n_equal", "n_timeout",
                                  "baseline_runtime_failures", "swapped_runtime_failures",
                                  "baseline_expected_mismatches", "swapped_expected_mismatches",
                                  "expected_output_matches", "ready_for_measurement")}})
        with (self.output / "behavior/summary.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summary[0]))
            writer.writeheader()
            writer.writerows(summary)
        self.log("behavior", failed=failures)
        if failures:
            raise RuntimeError("Behavior checks failed: " + ", ".join(failures))

    def require_behavior(self):
        missing = [key for key in self.keys if not self.cached("behavior", key)]
        if missing:
            raise RuntimeError("Run behavior successfully for all samples first: " + ", ".join(missing))

    def require_compute_host(self):
        if platform.node() != self.config["remote"]["compute_hostname"]:
            raise RuntimeError("Measurement is allowed only on the configured M2 host")

    def parquet(self, key, version):
        return self.output / "measure" / key / f"{version}.parquet"

    def validate_parquet(self, file):
        import pandas as pd
        from schema.records import ParquetSchema as C

        frame = pd.read_parquet(file)
        if frame.empty:
            raise ValueError(f"Empty token table: {file}")
        for column in (C.METRIC_ENTROPY, C.METRIC_SURPRISAL):
            if not frame[column].map(lambda x: x is not None and math.isfinite(float(x))).all():
                raise ValueError(f"Non-finite token metric: {file}/{column}")
        for column, expected in ((C.META_MODEL_NAME, self.config["measure"]["model"]),
                                 (C.META_MODEL_REVISION, self.config["measure"]["revision"])):
            if not frame[column].eq(expected).all():
                raise ValueError(f"Unexpected model metadata: {file}/{column}")
        return len(frame)

    def measure(self, loader=None, collector=None):
        self.require_compute_host()
        self.require_behavior()
        todo = []
        for s, key in zip(self.samples, self.keys):
            for version in ("original", "swapped"):
                item = f"{key}/{version}"
                if not self.cached("measure", item):
                    todo.append((s, key, version, item))
        if not todo:
            return
        if loader is None or collector is None:
            from equivalence import measure
            loader, collector = measure.load_model, measure.measure_file
        model = loader(self.config["measure"])
        failures = []
        for sample, key, version, item in todo:
            output = self.parquet(key, version)
            output.parent.mkdir(parents=True, exist_ok=True)
            try:
                collector(model, self.package / sample["path"] / f"{version}.py", output,
                          self.config["measure"], project=item)
                n_tokens = self.validate_parquet(output)
                self.done("measure", item, [output], tokens=n_tokens,
                          source_sha256=sample[f"{version}_sha256"])
                print(f"measure {item}: ok ({n_tokens} tokens)", flush=True)
            except Exception as exc:
                self.set_state("measure", item, "failed", reason=f"{type(exc).__name__}: {exc}")
                failures.append(item)
                print(f"measure {item}: failed: {exc}", flush=True)
        self.log("measure", failed=failures)
        if failures:
            raise RuntimeError("Measurement failed: " + ", ".join(failures))

    def compare(self):
        import pandas as pd
        from equivalence import compare, report
        from schema.records import ParquetSchema as C

        self.require_behavior()
        for key in self.keys:
            for version in ("original", "swapped"):
                if not self.cached("measure", f"{key}/{version}"):
                    raise RuntimeError(f"Measurement missing: {key}/{version}")
        thresholds = self.config["thresholds"]
        all_rows = []
        for sample, key in zip(self.samples, self.keys):
            folder = self.output / "compare" / key
            if not self.cached("compare", key):
                try:
                    frames = [pd.read_parquet(self.parquet(key, v)) for v in ("original", "swapped")]
                    sources = [(self.package / sample["path"] / f"{v}.py").read_bytes().decode("utf-8")
                               for v in ("original", "swapped")]
                    transform = read(self.package / sample["path"] / "transform.json")
                    result = compare.compare_pair(*frames, *sources, transform["line_map"], thresholds)
                    behavior_result = read(self.output / "behavior" / f"{key}.json")
                    summary = {"expected_output_matches": behavior_result["expected_output_matches"],
                               "baseline_expected_mismatches": behavior_result["baseline_expected_mismatches"],
                               "swapped_expected_mismatches": behavior_result["swapped_expected_mismatches"],
                               "dataset": sample["dataset"], "uid": sample["uid"], "group": sample["group"],
                               "if_line": sample["if_line"], "behavior_status": "match", **result["summary"]}
                    for version, frame in zip(("before", "after"), frames):
                        summary[f"mean_surprisal_{version}"] = float(compare.clean(frame)[C.METRIC_SURPRISAL].mean())
                    summary["mean_surprisal_delta"] = summary["mean_surprisal_after"] - summary["mean_surprisal_before"]
                    if not summary["loc_equal"]:
                        raise ValueError(f"LOC differs after transformation: {key}")
                    folder.mkdir(parents=True, exist_ok=True)
                    for name in ("tokens_before", "tokens_after", "lines", "token_alignment", "regions"):
                        result[name].to_csv(folder / f"{name}.csv", index=False)
                    write(folder / "summary.json", {"summary": summary, "thresholds": thresholds,
                          "metrics_before": result["metrics_before"], "metrics_after": result["metrics_after"],
                          "units": result["units"]})
                    meta = {"item": key, "transform": f"if_else_swap (L{sample['if_line']})",
                            "behavior": "match", "model": self.config["measure"]["model"], "thresholds": thresholds}
                    (folder / "report.html").write_text(report.render_html(key, result, meta, list(thresholds)), encoding="utf-8")
                    (folder / "report.md").write_text(report.render_markdown(key, result, meta, list(thresholds)), encoding="utf-8")
                    self.done("compare", key, list(folder.iterdir()))
                    print(f"compare {key}: ok", flush=True)
                except Exception as exc:
                    self.set_state("compare", key, "failed", reason=f"{type(exc).__name__}: {exc}")
                    raise
            all_rows.append(read(folder / "summary.json")["summary"])
        table = pd.DataFrame(all_rows)
        table.to_csv(self.output / "compare/summary.csv", index=False)
        for dataset, rows in table.groupby("dataset", sort=False):
            rows.to_csv(self.output / "compare" / f"{dataset}.csv", index=False)
        self.log("compare", rows=len(all_rows))

    def status(self):
        result = {}
        for stage in ("behavior", "measure", "compare"):
            expected = self.keys if stage != "measure" else [f"{k}/{v}" for k in self.keys for v in ("original", "swapped")]
            states = self.states(stage)
            counts = Counter(states.get(k, {}).get("status", "not_run") for k in expected)
            result[stage] = {"expected": len(expected), **dict(counts)}
            if stage == "behavior":
                result[stage]["expected_output_warning_samples"] = sum(
                    states.get(k, {}).get("expected_output_matches") is False for k in expected)
        return result

    def receipt(self):
        files = {str(p.relative_to(self.output)): sha(p) for p in sorted(self.output.rglob("*"))
                 if p.is_file() and p.name not in ("run.lock", "receipt.json") and not p.name.endswith(".tmp")}
        value = {"input_manifest_sha256": sha(self.manifest_path), "files": files, "status": self.status()}
        write(self.output / "receipt.json", value)
        return value

    def verify_receipt(self):
        receipt = read(self.output / "receipt.json")
        if not receipt or receipt["input_manifest_sha256"] != sha(self.manifest_path):
            raise ValueError("Missing or mismatched receipt")
        for relative, expected in receipt["files"].items():
            p = safe_child(self.output, relative)
            if not p.is_file() or sha(p) != expected:
                raise ValueError(f"Received file hash mismatch: {relative}")
        return {"verified_files": len(receipt["files"]), "status": receipt["status"]}
