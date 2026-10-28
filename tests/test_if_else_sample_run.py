"""Regression checks for gates, recovery and integrity of the 13-pair runner."""
import json
from pathlib import Path

import pytest

import paths
from equivalence.sample_run import SampleRun, read, sha, write


@pytest.fixture
def run(tmp_path):
    source = paths.PROJECT_ROOT / "experiments/if_else_swap_translation_20261026"
    original_manifest = read(source / "manifest.json")
    sample = dict(original_manifest["samples"][-3])  # the trusted positive minimal example
    package = tmp_path / "inputs"
    folder = package / sample["path"]
    folder.mkdir(parents=True)
    for p in (source / sample["path"]).iterdir():
        if p.is_file():
            (folder / p.name).write_bytes(p.read_bytes())
    manifest = {"samples": [sample], "files": {str(p.relative_to(package)): sha(p)
                                               for p in folder.iterdir() if p.is_file()}}
    write(package / "manifest.json", manifest)
    (tmp_path / "src").mkdir()
    (tmp_path / "src/signature.py").write_text("# code signature\n")
    config = tmp_path / "config.toml"
    config.write_text('''[experiment]
package = "inputs"
output = "outputs"
[experiment.expected_counts]
minimal = 1
[behavior]
timeout_sec = 2.0
workers = 2
require_expected_output = true
[measure]
model = "test-double"
model_kind = "hf_causal_lm"
revision = "fixture-revision"
device = "mps"
dtype = "float16"
context_strategy = "function_scope"
[thresholds]
p67 = 0.6813
p80_saved = 1.3238
[remote]
compute_hostname = "TEST-M2"
''')
    return SampleRun(config, tmp_path)


@pytest.mark.parametrize("mode", ["crash", "wrong_output"])
def test_failed_processes_are_not_successful_even_if_errors_match(run, monkeypatch, mode):
    from equivalence import behavior

    def failed(source, cases, *args, **kwargs):
        return [{"returncode": 1 if mode == "crash" else 0, "stdout": "wrong", "exception": "same error", "matches_expected": False}
                for _ in cases]

    monkeypatch.setattr(behavior, "observe_all", failed)
    with run.locked(), pytest.raises(RuntimeError, match="Behavior checks failed"):
        run.behavior()
    result = read(run.output / "behavior/minimal/positive.json")
    assert result["status"] == "match"
    assert not result["ready_for_measurement"]
    with pytest.raises(RuntimeError, match="Run behavior successfully"):
        run.require_behavior()


def test_measure_never_loads_a_model_before_behavior_passes(run, monkeypatch):
    monkeypatch.setattr(run, "require_compute_host", lambda: None)
    calls = []
    with pytest.raises(RuntimeError, match="Run behavior successfully"):
        run.measure(loader=lambda cfg: calls.append(cfg), collector=lambda *a, **kw: None)
    assert calls == []


def test_measure_rejects_a_host_other_than_m2(run):
    with pytest.raises(RuntimeError, match="M2 host"):
        run.measure(loader=lambda _: None, collector=lambda *a, **kw: None)


def test_inputs_and_conditions_cannot_change_after_start(run):
    with run.locked():
        pass
    text = run.config_path.read_text()
    run.config_path.write_text(text.replace('dtype = "float16"', 'dtype = "bfloat16"'))
    with pytest.raises(ValueError, match="Conditions, inputs or code changed"):
        SampleRun(run.config_path, run.project)
    run.config_path.write_text(text)
    (run.package / run.samples[0]["path"] / "original.py").write_text("changed")
    with pytest.raises(ValueError, match="Input hash mismatch"):
        SampleRun(run.config_path, run.project)


def test_dummy_pipeline_resumes_compares_and_verifies_received_files(run, monkeypatch):
    # These files live only in pytest's temporary directory. No real model is loaded.
    from model.dummy import DummyAdapter
    from equivalence.measure import measure_file

    with run.locked():
        run.behavior()
    monkeypatch.setattr(run, "require_compute_host", lambda: None)
    calls = []

    def load(config):
        calls.append("load")
        return DummyAdapter(model_name=config["model"], revision=config["revision"])

    with run.locked():
        run.measure(loader=load, collector=measure_file)
        run.measure(loader=load, collector=measure_file)
        run.compare()
        run.compare()
        receipt = run.receipt()
    assert calls == ["load"]
    assert run.status()["measure"] == {"expected": 2, "ok": 2}
    assert run.status()["compare"] == {"expected": 1, "ok": 1}
    assert (run.output / "compare/minimal/positive/report.html").is_file()
    assert run.verify_receipt()["verified_files"] == len(receipt["files"])
    parquet = run.parquet("minimal/positive", "original")
    parquet.write_bytes(b"tampered")
    with pytest.raises(ValueError, match="Received file hash mismatch"):
        run.verify_receipt()
    with pytest.raises(ValueError, match="Output hash mismatch"):
        run.cached("measure", "minimal/positive/original")


def test_exclusive_lock_prevents_parallel_stages(run):
    another = SampleRun(run.config_path, run.project)
    with run.locked():
        with pytest.raises(RuntimeError, match="Another stage is running"):
            with another.locked():
                pass


def test_status_does_not_create_outputs(run):
    assert run.status()["measure"] == {"expected": 2, "not_run": 2}
    assert not run.output.exists()


def test_expected_output_diagnostics_do_not_override_equivalence_mode(run, monkeypatch):
    from equivalence import behavior
    run.config["behavior"]["require_expected_output"] = False

    def same_normal_output(source, cases, *args, **kwargs):
        return [{"returncode": 0, "stdout": "different from saved reference", "exception": None,
                 "matches_expected": False} for _ in cases]

    monkeypatch.setattr(behavior, "observe_all", same_normal_output)
    with run.locked():
        run.behavior()
    result = read(run.output / "behavior/minimal/positive.json")
    assert result["ready_for_measurement"]
    assert result["baseline_runtime_failures"] == 0
    assert result["baseline_expected_mismatches"] == 3
    assert not result["expected_output_matches"]
    assert run.status()["behavior"]["expected_output_warning_samples"] == 1
