"""実験ディレクトリの管理: 設定の固定、実行記録、段階ごとの進捗 (失敗分だけの再実行)。

- ``config.json``: 最初の実行時の設定。計測条件 (変換・モデル・閾値など) が異なる設定で
  同じディレクトリを使おうとするとエラーにする (既存結果を別条件で上書きしないため)。
  対象 ID の追加は許す。
- ``manifest.json``: 作成時の環境 (コードの版、Python・主要パッケージの版、OS)
- ``runs.jsonl``: 実行ごとの記録 (段階、開始・終了時刻、件数、コードの版)
- ``status/<stage>.json``: 対象ごとの状態 (ok / failed / skipped と理由)
"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any, Dict, Optional

import paths

#: 同じ実験ディレクトリ内で変えてもよい設定 (対象の追加など)
MUTABLE_KEYS = {("experiment", "ids"), ("experiment", "targets"), ("experiment", "limit"), ("behavior", "workers")}

_PACKAGES = ["torch", "transformers", "tree-sitter", "tree-sitter-python", "pandas", "numpy", "pyarrow", "openai"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_info(repo: Path) -> Dict[str, Any]:
    def run(*args: str) -> Optional[str]:
        try:
            out = subprocess.run(["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                 timeout=10, check=True)
            return out.stdout.decode("utf-8", errors="replace").strip()
        except (OSError, subprocess.SubprocessError):
            return None

    status = run("status", "--porcelain")
    return {"path": str(repo), "commit": run("rev-parse", "HEAD"), "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
            "dirty": None if status is None else bool(status)}


def environment() -> Dict[str, Any]:
    versions = {}
    for name in _PACKAGES:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = None
    return {"python": sys.version.split()[0], "platform": platform.platform(), "packages": versions}


def _conditions(config: Dict[str, Any]) -> Dict[str, Any]:
    out = json.loads(json.dumps(config))
    for section, key in MUTABLE_KEYS:
        out.get(section, {}).pop(key, None)
    return out


def _atomic_write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    tmp.replace(path)


class RunState:
    def __init__(self, run_dir: Path, config: Dict[str, Any]) -> None:
        self.run_dir = run_dir
        self.config = config
        run_dir.mkdir(parents=True, exist_ok=True)
        config_path = run_dir / "config.json"
        if config_path.exists():
            saved = json.loads(config_path.read_text(encoding="utf-8"))
            if _conditions(saved) != _conditions(config):
                raise ValueError(
                    f"{run_dir} は別の条件で作られている。条件を変えるなら experiment.name を変えて別ディレクトリにする "
                    f"(差分は {config_path} と比較)")
            if saved != config:
                _atomic_write_json(config_path, config)  # 対象 ID の追加を反映
        else:
            _atomic_write_json(config_path, config)
            _atomic_write_json(run_dir / "manifest.json", {
                "created_at": now(), "code": git_info(paths.PROJECT_ROOT), "lm_cc": git_info(paths.LM_CC_ROOT),
                "environment": environment(),
            })
        self._status: Dict[str, Dict[str, Any]] = {}

    # ----- 段階ごとの状態 --------------------------------------------------
    def _status_path(self, stage: str) -> Path:
        return self.run_dir / "status" / f"{stage}.json"

    def status(self, stage: str) -> Dict[str, Any]:
        if stage not in self._status:
            path = self._status_path(stage)
            self._status[stage] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        return self._status[stage]

    def is_ok(self, stage: str, key: str) -> bool:
        return self.status(stage).get(key, {}).get("status") == "ok"

    def set(self, stage: str, key: str, status: str, **info: Any) -> None:
        self.status(stage)[key] = {"status": status, "updated_at": now(), **info}
        _atomic_write_json(self._status_path(stage), self.status(stage))

    # ----- 実行記録 --------------------------------------------------------
    def log_run(self, record: Dict[str, Any]) -> None:
        record = {**record, "code": git_info(paths.PROJECT_ROOT), "python": sys.version.split()[0]}
        with open(self.run_dir / "runs.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
