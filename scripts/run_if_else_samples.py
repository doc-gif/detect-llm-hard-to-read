"""M4 entry point for the frozen 13-pair experiment. No stage runs implicitly."""
from __future__ import annotations

import argparse
from contextlib import redirect_stderr, redirect_stdout
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import traceback

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import paths
from equivalence.sample_run import SampleRun, environment, sha


class Tee:
    def __init__(self, terminal, log):
        self.terminal, self.log = terminal, log

    def write(self, text):
        self.terminal.write(text)
        self.log.write(text)
        self.flush()
        return len(text)

    def flush(self):
        self.terminal.flush()
        self.log.flush()


def command(args, *, cwd=None):
    subprocess.run(args, cwd=cwd, check=True)


def remote_settings(run):
    cfg = run.config["remote"]
    for name in ("host", "root", "venv_source"):
        if not re.fullmatch(r"[A-Za-z0-9_./-]+", cfg[name]) or cfg[name].startswith("-"):
            raise ValueError(f"Unsupported remote path or host: {name}")
    relative_config = run.config_path.resolve().relative_to(run.project.resolve()).as_posix()
    return cfg, relative_config


def ssh(run, text):
    cfg, _ = remote_settings(run)
    command(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "-o", "ServerAliveInterval=30",
             "-o", "ServerAliveCountMax=3", cfg["host"], text])


def remote(run, stage):
    cfg, relative_config = remote_settings(run)
    invocation = [".venv/bin/python", "scripts/run_if_else_samples.py", stage,
                  "--config", relative_config, "--on-m2"]
    ssh(run, f"cd {shlex.quote(cfg['root'])} && "
             "HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 MPLBACKEND=Agg " + shlex.join(invocation))


def stage(run):
    run.require_behavior()
    cfg, relative_config = remote_settings(run)
    # A managed snapshot may be refreshed only if its previously deployed files were not edited on M2.
    check = '''from pathlib import Path
import hashlib,json
r=Path(ROOT)
marker=r/'deployment.json'
if r.exists() and any(r.iterdir()):
 if not marker.exists(): raise SystemExit('Remote directory is not a managed snapshot; choose a new remote.root')
 previous=json.loads(marker.read_text())
 for rel,expected in previous['files'].items():
  p=r/rel
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
   raise SystemExit('Remote file was modified: '+rel)
r.mkdir(parents=True,exist_ok=True)
'''.replace("ROOT", repr(cfg["root"]))
    ssh(run, "python3 -c " + shlex.quote(check))
    files = list(run.binding["code_sha256"])
    files.append(relative_config)
    package_rel = run.package.relative_to(run.project)
    files += [str(package_rel / p) for p in run.manifest["files"]]
    files.append(str(package_rel / "manifest.json"))
    files = sorted(set(files))
    deployment = {"files": {p: sha(run.project / p) for p in files},
                  "input_manifest_sha256": sha(run.manifest_path)}
    behavior_files = [run.output / "run.json", run.output / "status/behavior.json"]
    behavior_files += sorted((run.output / "behavior").rglob("*.json"))
    sync_files = files + [str(p.relative_to(run.project)) for p in behavior_files]
    command(["rsync", "-a", "--relative", *sync_files, f"{cfg['host']}:{cfg['root']}/"], cwd=run.project)
    with tempfile.TemporaryDirectory() as temp:
        marker = Path(temp) / "deployment.json"
        marker.write_text(json.dumps(deployment, indent=2) + "\n")
        command(["rsync", "-a", str(marker), f"{cfg['host']}:{cfg['root']}/deployment.json"])
    setup = (f"cd {shlex.quote(cfg['root'])} && "
             f"test -x {shlex.quote(cfg['venv_source'])}/bin/python && "
             f"(test -e .venv || ln -s {shlex.quote(cfg['venv_source'])} .venv)")
    ssh(run, setup)
    remote(run, "check")
    print("M2 snapshot staged and verified. No measurement started.", flush=True)


def fetch(run):
    cfg, _ = remote_settings(run)
    remote(run, "receipt")
    run.output.mkdir(parents=True, exist_ok=True)
    output_rel = run.output.relative_to(run.project)
    command(["rsync", "-a", "--exclude", "run.lock",
             f"{cfg['host']}:{cfg['root']}/{output_rel}/", str(run.output) + "/"])
    run.check_binding()
    print(json.dumps(run.verify_receipt(), ensure_ascii=False, indent=2))


def execute_local(run, stage_name):
    if stage_name == "status":
        print(json.dumps(run.status(), ensure_ascii=False, indent=2))
        return
    if stage_name == "check":
        run.require_compute_host()
        run.require_behavior()
        print(json.dumps({"inputs_verified": len(run.manifest["files"]),
                          "status": run.status(), "environment": environment()}, indent=2))
        return
    with run.locked():
        if stage_name == "receipt":
            value = run.receipt()
            print(json.dumps({"files": len(value["files"]), "status": value["status"]}, indent=2))
            return
        log = run.output / "logs" / f"{stage_name}.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("a", encoding="utf-8") as stream:
            with redirect_stdout(Tee(sys.stdout, stream)), redirect_stderr(Tee(sys.stderr, stream)):
                try:
                    getattr(run, stage_name)()
                    print(json.dumps(run.status(), ensure_ascii=False, indent=2))
                except Exception:
                    traceback.print_exc()
                    raise


def main(argv=None):
    parser = argparse.ArgumentParser(description="13組の動作確認とM2での計測・比較・結果取得")
    parser.add_argument("stage", choices=["behavior", "stage", "measure", "compare", "fetch", "status", "check", "receipt"])
    parser.add_argument("--config", type=Path, default=paths.PROJECT_ROOT / "configs/equivalence/if_else_samples.toml")
    parser.add_argument("--remote", action="store_true", help="status: M2側の状態を表示する")
    parser.add_argument("--on-m2", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    run = SampleRun(args.config.resolve())
    if args.on_m2:
        run.require_compute_host()
        if args.stage not in ("measure", "compare", "status", "check", "receipt"):
            raise ValueError("Unsupported stage on M2")
        execute_local(run, args.stage)
    elif args.stage == "stage":
        with run.locked():
            stage(run)
    elif args.stage == "fetch":
        with run.locked():
            fetch(run)
    elif args.stage in ("measure", "compare") or (args.stage == "status" and args.remote):
        remote(run, args.stage)
    elif args.stage in ("behavior", "status"):
        execute_local(run, args.stage)
    else:
        raise ValueError("check and receipt are internal M2 stages")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
