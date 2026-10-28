"""loc_variation_9pairs 専用の入口 (既存の if/else 入れ替え実験とは別)。

同じ処理でコードの書式と LOC を変えた 9 組を、変換前後で計測して比較する。
再利用する既存部品 (定義は変更しない):
  - ``collect_metrics.collect`` + ``ParquetWriter``: ``equivalence.measure.measure_file`` 経由
  - ``equivalence.compare.file_metrics`` / ``semantic_units``: LOC・トークン数・SU 数・境界・原因トークン
  - ``compare.token_table``: トークン表

この実験で別に作るもの:
  - 入力の取り込み: manifest.json の配列、original/transformed、tests.json をそのまま読む (zip も可)
  - 動作検証: tests.json の ``args`` を ``entry`` 関数 (既定 ``run``) に渡し、``expected`` と比べる。
    LOC が変わることは失敗にしない。
  - 文の対応: ``statement_alignment`` (位置情報を除いた AST の一致。``token_alignment`` は使わない)
  - 条件・反復ごとの保存と再開

保存先 (出力ルートの下。既存の data/ out/ results/ の既存ディレクトリには書かない)::

    <output>/loc_variation_run.json            この実験の出力ルートである印
    <output>/<条件キー>/condition.json         条件 (モデル・revision・device・dtype・閾値・入力 manifest の SHA-256)
    <output>/<条件キー>/inputs/<case>/{original,transformed}.py   入力の複製 (SHA-256 を検証)
    <output>/<条件キー>/behavior/<case>.json   tests.json の結果
    <output>/<条件キー>/rep_NNN/measure/...    反復 NNN の Parquet と measurement.json (実入力全文・ハッシュ・環境)
    <output>/<条件キー>/rep_NNN/compare/<case>/...  トークン表・文の表・SU・原因トークン
    <output>/<条件キー>/rep_NNN/summary.csv, summary_all.csv, summary.md

再開と別反復:
  - 条件キーは「モデル・revision・device・dtype・文脈戦略・閾値・収集器の版・入力 manifest の SHA-256」から決める。
    対象ケースの選択 (最初の 3 組 / 全 9 組) は条件に含めないので、3 組の後に 9 組へ広げると 3 組は再開される。
  - 同じ条件キーと同じ反復 ID で成功済み (ok、かつ出力のハッシュが一致) の項目は計測し直さない (再開)。
  - 反復 ID が違えば別の保存先に計測する (別反復)。再開では出力を上書きしない。
  - 条件が違えば条件キーが変わり、別ディレクトリになる。
  - 出力のハッシュが保存済みの値と違う場合は、上書きせずにエラーにする。
"""
from __future__ import annotations

import csv
import fcntl
import hashlib
import json
import math
import posixpath
import re
import subprocess
import sys
import tempfile
import time
import tomllib
import zipfile
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

import paths
from equivalence import runstate
from equivalence import statement_alignment as sa
from schema.records import COLLECTOR_VERSION
from schema.records import ParquetSchema as PCol

VERSIONS = ("original", "transformed")
MARKER = "loc_variation_run.json"
KIND = "loc_variation_9pairs"
REQUIRED_KEYS = ("case_id", "category", "title", "original", "transformed", "original_LOC", "transformed_LOC",
                 "test_count", "original_sha256", "transformed_sha256")
_RUNNER = Path(__file__).with_name("_run_cases.py")


# ----------------------------------------------------------------------
# 小さな道具
# ----------------------------------------------------------------------
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _plain(value: Any) -> Any:
    """JSON に書ける値へ変える (numpy の値、NaN と無限大を含む)。"""
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if hasattr(value, "item") and not isinstance(value, (str, bytes)):
        try:
            value = value.item()
        except (ValueError, TypeError):
            return str(value)
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(_plain(value), ensure_ascii=False, indent=1, allow_nan=False, default=str) + "\n",
                   encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(_plain(rows))
    tmp.replace(path)


def _safe_relative(rel: str) -> str:
    norm = posixpath.normpath(rel)
    if posixpath.isabs(rel) or norm.startswith("..") or "\\" in rel:
        raise ValueError(f"パッケージの外を指すパス: {rel}")
    return norm


def rep_label(repetition: int) -> str:
    if not isinstance(repetition, int) or repetition < 1:
        raise ValueError(f"反復 ID は 1 以上の整数: {repetition!r}")
    return f"rep_{repetition:03d}"


# ----------------------------------------------------------------------
# 計測結果 (Parquet) の指標列の検査
# ----------------------------------------------------------------------
def check_token_metrics(frame: Any, allow_leading_surprisal_missing: bool = False, label: str = "") -> None:
    """entropy と surprisal の列を検査する。規則は列ごとに別である。

    - entropy: 欠損 (None / NaN) を 1 つも許さない。全件欠損・一部欠損・非有限値 (inf) をそれぞれ別のエラーにする。
    - surprisal: 既定では entropy と同じ。``allow_leading_surprisal_missing=True`` のときだけ、
      先頭トークン (``idx`` が最小の行) の欠損を許す。それ以外の欠損と非有限値は許さない。
      全件欠損はどちらの規則でもエラーである (先頭だけ欠けるのとは区別する)。
    """
    import numpy as np
    import pandas as pd

    where = f"{label}" if label else ""
    leading = frame[PCol.IDX].idxmin() if allow_leading_surprisal_missing and PCol.IDX in frame else frame.index[0]
    for column, name, allow_leading in ((PCol.METRIC_ENTROPY, "entropy", False),
                                        (PCol.METRIC_SURPRISAL, "surprisal", allow_leading_surprisal_missing)):
        if column not in frame:
            raise ValueError(f"{name} の列がない: {where}")
        try:
            values = pd.to_numeric(frame[column], errors="raise").astype(float)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{name} に数値でない値: {where}: {exc}") from exc
        missing = values.isna()
        n, n_missing = len(values), int(missing.sum())
        if n_missing == n:
            raise ValueError(f"{name} が全件欠損 ({n} 件): {where}")
        if allow_leading:
            missing = missing.copy()
            missing.loc[leading] = False
            n_missing = int(missing.sum())
        if n_missing:
            rule = "先頭以外が欠損" if allow_leading else "一部欠損"
            raise ValueError(f"{name} が{rule} ({n_missing}/{n} 件): {where}")
        present = values[values.notna()]
        if not np.isfinite(present.to_numpy()).all():
            raise ValueError(f"{name} に非有限値: {where}")


# ----------------------------------------------------------------------
# 入力パッケージ (zip または展開済みディレクトリ)
# ----------------------------------------------------------------------
@dataclass
class Case:
    order: int
    case_id: str
    category: str
    title: str
    entry: str
    sources: Dict[str, str]
    sha256: Dict[str, str]
    declared_loc: Dict[str, int]
    source_loc: Dict[str, int]
    tests: List[Dict[str, Any]]
    tests_sha256: str
    diff_text: Optional[str]
    manifest_row: Dict[str, Any]

    def source_bytes(self, version: str) -> bytes:
        return self.sources[version].encode("utf-8")


@dataclass
class Package:
    path: Path
    kind: str  # "zip" or "directory"
    file_sha256: Optional[str]
    manifest_sha256: str
    cases: List[Case] = field(default_factory=list)

    def case(self, case_id: str) -> Case:
        for case in self.cases:
            if case.case_id == case_id:
                return case
        raise KeyError(case_id)


class _Reader:
    def read(self, rel: str) -> bytes:  # pragma: no cover - interface
        raise NotImplementedError

    def exists(self, rel: str) -> bool:  # pragma: no cover - interface
        raise NotImplementedError


class _ZipReader(_Reader):
    def __init__(self, path: Path) -> None:
        self.zf = zipfile.ZipFile(path)
        names = [n for n in self.zf.namelist() if not n.endswith("/")]
        for name in names:
            _safe_relative(name)
        manifests = [n for n in names if posixpath.basename(n) == "manifest.json" and n.count("/") <= 1]
        if len(manifests) != 1:
            raise ValueError(f"manifest.json が 1 つに決まらない: {manifests}")
        self.prefix = posixpath.dirname(manifests[0])
        self.names = set(names)

    def _full(self, rel: str) -> str:
        rel = _safe_relative(rel)
        return posixpath.join(self.prefix, rel) if self.prefix else rel

    def read(self, rel: str) -> bytes:
        return self.zf.read(self._full(rel))

    def exists(self, rel: str) -> bool:
        return self._full(rel) in self.names


class _DirReader(_Reader):
    def __init__(self, path: Path) -> None:
        self.root = path
        if not (path / "manifest.json").is_file():
            children = [p for p in path.iterdir() if p.is_dir() and (p / "manifest.json").is_file()]
            if len(children) != 1:
                raise ValueError(f"manifest.json が見つからない: {path}")
            self.root = children[0]

    def read(self, rel: str) -> bytes:
        return (self.root / _safe_relative(rel)).read_bytes()

    def exists(self, rel: str) -> bool:
        return (self.root / _safe_relative(rel)).is_file()


def load_package(path: Path, entry: str = "run") -> Package:
    """manifest.json の配列と各ケースの original / transformed / tests.json を、そのまま読み込む。

    SHA-256 が manifest と合わないファイルはエラーにする。manifest の LOC と実際の行数の差、
    original と transformed の LOC の差はエラーにしない (記録する)。
    """
    path = Path(path)
    if path.is_file():
        reader: _Reader = _ZipReader(path)
        kind, file_sha = "zip", sha256_file(path)
    elif path.is_dir():
        reader, kind, file_sha = _DirReader(path), "directory", None
    else:
        raise FileNotFoundError(path)
    manifest_bytes = reader.read("manifest.json")
    rows = json.loads(manifest_bytes.decode("utf-8-sig"))
    if not isinstance(rows, list) or not rows:
        raise ValueError("manifest.json は空でない配列である必要がある")
    package = Package(path=path, kind=kind, file_sha256=file_sha, manifest_sha256=sha256_bytes(manifest_bytes))
    seen = set()
    for order, row in enumerate(rows):
        missing = [k for k in REQUIRED_KEYS if k not in row]
        if missing:
            raise ValueError(f"manifest の項目が足りない ({row.get('case_id')}): {missing}")
        case_id = row["case_id"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", case_id) or case_id in seen:
            raise ValueError(f"case_id が不正または重複: {case_id!r}")
        seen.add(case_id)
        sources, hashes, declared, actual = {}, {}, {}, {}
        for version in VERSIONS:
            raw = reader.read(row[version])
            if sha256_bytes(raw) != row[f"{version}_sha256"]:
                raise ValueError(f"SHA-256 が manifest と一致しない: {case_id}/{version}")
            sources[version] = raw.decode("utf-8")
            hashes[version] = sha256_bytes(raw)
            declared[version] = int(row[f"{version}_LOC"])
            actual[version] = len(sources[version].splitlines())
        tests_rel = posixpath.join(posixpath.dirname(row["original"]), "tests.json")
        tests_raw = reader.read(tests_rel)
        tests = json.loads(tests_raw.decode("utf-8"))
        if not isinstance(tests, list) or any("args" not in t or "expected" not in t for t in tests):
            raise ValueError(f"tests.json の形式が不正: {case_id}")
        if len(tests) != int(row["test_count"]):
            raise ValueError(f"tests.json の件数が manifest と違う: {case_id}")
        diff_rel = posixpath.join(posixpath.dirname(row["original"]), "change.diff")
        diff_text = reader.read(diff_rel).decode("utf-8") if reader.exists(diff_rel) else None
        package.cases.append(Case(
            order=order, case_id=case_id, category=row["category"], title=row["title"],
            entry=row.get("entry", entry), sources=sources, sha256=hashes, declared_loc=declared,
            source_loc=actual, tests=tests, tests_sha256=sha256_bytes(tests_raw), diff_text=diff_text,
            manifest_row=row))
    return package


def select_cases(package: Package, spec: str) -> List[Case]:
    """``all`` / ``first3`` (``first:N``) / ``id1,id2`` から対象ケースを選ぶ。順序は manifest の順。"""
    spec = spec.strip()
    if spec == "all":
        return list(package.cases)
    match = re.fullmatch(r"first:?(\d+)", spec)
    if match:
        n = int(match.group(1))
        if not 1 <= n <= len(package.cases):
            raise ValueError(f"件数が範囲外: {n}")
        return package.cases[:n]
    ids = [x.strip() for x in spec.split(",") if x.strip()]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError(f"ケースの指定が不正: {spec!r}")
    known = {c.case_id: c for c in package.cases}
    unknown = [i for i in ids if i not in known]
    if unknown:
        raise ValueError(f"manifest にないケース: {unknown}")
    return sorted((known[i] for i in ids), key=lambda c: c.order)


# ----------------------------------------------------------------------
# 動作検証 (tests.json の args / expected)
# ----------------------------------------------------------------------
def run_tests(source: str, entry: str, tests: List[Dict[str, Any]], timeout: float) -> Dict[str, Any]:
    """``entry(*args)`` を子プロセスで実行し、JSON 往復後の値を ``expected`` と比べる。"""
    with tempfile.TemporaryDirectory() as tmp:
        spec_path, result_path = Path(tmp) / "spec.json", Path(tmp) / "result.json"
        spec_path.write_text(json.dumps({"code": source, "entry": entry,
                                         "cases": [{"args": t["args"]} for t in tests]}), encoding="utf-8")
        try:
            subprocess.run([sys.executable, str(_RUNNER), str(spec_path), str(result_path)], cwd=tmp,
                           timeout=timeout, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return {"timeout": True, "load_error": None, "results": [], "n_passed": 0}
        if not result_path.exists():
            return {"timeout": False, "load_error": "子プロセスが結果を書かなかった", "results": [], "n_passed": 0}
        raw = json.loads(result_path.read_text(encoding="utf-8"))
    results = []
    for index, (test, got) in enumerate(zip(tests, raw["results"])):
        matches = got["error"] is None and got["value"] == test["expected"]
        results.append({"index": index, "args": test["args"], "expected": test["expected"],
                        "value": got["value"], "error": got["error"], "matches": matches})
    n_passed = sum(r["matches"] for r in results)
    ok = raw["load_error"] is None and len(results) == len(tests) and n_passed == len(tests)
    return {"timeout": False, "load_error": raw["load_error"], "results": results, "n_passed": n_passed, "ok": ok}


def check_case(case: Case, timeout: float) -> Dict[str, Any]:
    """1 ケースの動作検証。LOC の違いは失敗にしない。AST が等しいかは記録するだけで失敗にしない。"""
    result: Dict[str, Any] = {"case_id": case.case_id, "n_tests": len(case.tests), "versions": {}}
    syntax_ok = True
    for version in VERSIONS:
        try:
            sa.parse_statements(case.sources[version])
        except SyntaxError as exc:
            syntax_ok = False
            result["versions"][version] = {"ok": False, "load_error": f"SyntaxError: {exc}", "results": [],
                                           "n_passed": 0, "timeout": False}
            continue
        result["versions"][version] = run_tests(case.sources[version], case.entry, case.tests, timeout)
    result["syntax_ok"] = syntax_ok
    result["ast_equal"] = sa.ast_equal(*[case.sources[v] for v in VERSIONS]) if syntax_ok else None
    result["loc_declared"] = case.declared_loc
    result["loc_source"] = case.source_loc
    result["loc_changed"] = case.source_loc["original"] != case.source_loc["transformed"]
    result["manifest_loc_matches"] = case.declared_loc == case.source_loc
    result["status"] = "ok" if syntax_ok and all(result["versions"][v].get("ok") for v in VERSIONS) else "failed"
    return result


# ----------------------------------------------------------------------
# 実行の管理
# ----------------------------------------------------------------------
def _is_within(child: Path, parent: Path) -> bool:
    return child == parent or parent in child.parents


class LocVariationRun:
    def __init__(self, config_path: Path, project_root: Path = paths.PROJECT_ROOT,
                 package_path: Optional[Path] = None, output_root: Optional[Path] = None) -> None:
        self.project = Path(project_root)
        self.config_path = Path(config_path)
        self.config = tomllib.loads(self.config_path.read_text(encoding="utf-8"))
        exp = self.config["experiment"]
        self.entry = exp.get("entry", "run")
        self.timeout = float(self.config.get("behavior", {}).get("timeout_sec", 10.0))
        self.allow_leading_surprisal_missing = bool(
            self.config.get("validation", {}).get("allow_leading_surprisal_missing", False))
        self.measure_cfg = dict(self.config["measure"])
        self.thresholds = {k: float(v) for k, v in self.config["thresholds"].items()}
        self.labels = list(self.thresholds)
        self.package_path = Path(package_path) if package_path else self.project / exp["package"]
        self.output_root = Path(output_root) if output_root else self.project / exp["output"]
        self._check_output_root()
        self.package = load_package(self.package_path, self.entry)
        self.condition = {
            "kind": KIND,
            "package_manifest_sha256": self.package.manifest_sha256,
            "model": {"kind": self.measure_cfg.get("model_kind", "hf_causal_lm"), "name": self.measure_cfg["model"],
                      "revision": self.measure_cfg.get("revision") or None,
                      "device": self.measure_cfg.get("device") or None,
                      "dtype": self.measure_cfg.get("dtype") or None},
            "context_strategy": self.measure_cfg.get("context_strategy", "function_scope"),
            "thresholds": self.thresholds,
            "collector_version": COLLECTOR_VERSION,
        }
        canonical = json.dumps(self.condition, sort_keys=True, ensure_ascii=False)
        self.key = sha256_bytes(canonical.encode("utf-8"))[:16]
        self.dir = self.output_root / self.key
        self._status: Dict[str, Dict[str, Any]] = {}

    # ----- 出力先の安全確認 --------------------------------------------
    def _check_output_root(self) -> None:
        out = self.output_root.resolve()
        protected = [paths.DATA_DIR, paths.OUT_DIR, paths.ENRICHED_DIR, paths.SUMMARIES_DIR, paths.PLOTS_DIR,
                     paths.EXPERIMENTS_DIR, paths.RESULTS_DIR / "semantic_unit_binning",
                     paths.RESULTS_DIR / "semantic_unit_model_comparison", paths.PROJECT_ROOT / "experiments",
                     paths.RESULTS_DIR / "equivalence"]
        for directory in protected:
            directory = directory.resolve()
            if _is_within(out, directory) or _is_within(directory, out):
                raise ValueError(f"出力先が既存のデータ・結果と重なる: {out} と {directory}")
        if _is_within(self.package_path.resolve(), out) or _is_within(out, self.package_path.resolve()):
            raise ValueError("出力先が入力パッケージと重なる")
        if out.exists() and any(out.iterdir()) and not (out / MARKER).exists():
            raise ValueError(f"空でない出力先で、この実験の印 ({MARKER}) がない: {out}")

    @contextmanager
    def locked(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        if not (self.output_root / MARKER).exists():
            write_json(self.output_root / MARKER, {"kind": KIND, "created_at": runstate.now()})
        condition_path = self.dir / "condition.json"
        record = {"condition": self.condition, "condition_key": self.key}
        saved = read_json(condition_path)
        if saved is not None and saved.get("condition") != self.condition:
            raise ValueError(f"条件キーが同じなのに条件が違う: {condition_path}")
        if saved is None:
            write_json(condition_path, {**record, "created_at": runstate.now(),
                                        "package": {"path": str(self.package_path), "kind": self.package.kind,
                                                    "file_sha256": self.package.file_sha256,
                                                    "manifest_sha256": self.package.manifest_sha256},
                                        "code": runstate.git_info(paths.PROJECT_ROOT),
                                        "environment": runstate.environment()})
        with (self.dir / "run.lock").open("a+") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise RuntimeError("別の実行が進行中") from exc
            yield

    # ----- 段階ごとの状態 ------------------------------------------------
    def states(self, stage: str) -> Dict[str, Any]:
        if stage not in self._status:
            self._status[stage] = read_json(self.dir / "status" / f"{stage}.json", {})
        return self._status[stage]

    def set_state(self, stage: str, key: str, status: str, **extra: Any) -> None:
        self.states(stage)[key] = {"status": status, "updated_at": runstate.now(), **extra}
        write_json(self.dir / "status" / f"{stage}.json", self.states(stage))

    def cached(self, stage: str, key: str, expected_sources: Optional[Dict[str, str]] = None) -> bool:
        """成功済みで、保存した出力のハッシュが一致するか。不一致は上書きせずエラーにする。"""
        state = self.states(stage).get(key, {})
        if state.get("status") != "ok":
            return False
        for name, expected in (expected_sources or {}).items():
            if state.get(name) != expected:
                raise ValueError(f"保存済みの入力ハッシュが現在の入力と違う: {stage}/{key}/{name}")
        for rel, expected in state.get("files", {}).items():
            file = self.dir / rel
            if not file.is_file() or sha256_file(file) != expected:
                raise ValueError(f"出力のハッシュが保存値と違う (上書きしない): {rel}")
        return True

    def done(self, stage: str, key: str, files: Sequence[Path], **extra: Any) -> None:
        self.set_state(stage, key, "ok", files={str(p.relative_to(self.dir)): sha256_file(p) for p in files}, **extra)

    def log(self, stage: str, **extra: Any) -> None:
        record = {"stage": stage, "at": runstate.now(), "condition_key": self.key,
                  "code": runstate.git_info(paths.PROJECT_ROOT), "python": sys.version.split()[0], **extra}
        with (self.dir / "runs.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(_plain(record), ensure_ascii=False) + "\n")

    # ----- 入力 ------------------------------------------------------------
    def input_path(self, case: Case, version: str) -> Path:
        """入力の複製を返す。なければ書き、あれば SHA-256 を確認する (上書きしない)。"""
        path = self.dir / "inputs" / case.case_id / f"{version}.py"
        if path.exists():
            if sha256_file(path) != case.sha256[version]:
                raise ValueError(f"保存済みの入力が manifest のハッシュと違う: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(case.source_bytes(version))
        return path

    def rep_dir(self, repetition: int) -> Path:
        return self.dir / rep_label(repetition)

    # ----- 段階 1: 動作検証 -----------------------------------------------
    @staticmethod
    def behavior_inputs(case: Case, manifest_sha256: str) -> Dict[str, str]:
        """動作検証の成功を再利用してよい入力。1 つでも違えば古い成功は使わず、検証し直す。

        manifest の SHA-256 は original / transformed の中身を表す。tests.json の中身 (args・expected) は
        manifest に入らないので ``tests_sha256`` を、呼ぶ関数は manifest の ``entry`` か設定の ``entry`` で
        決まるので、そのケースで実際に使う ``entry`` を加える。件数が同じでも変更を検出できる。
        """
        return {"manifest_sha256": manifest_sha256, "tests_sha256": case.tests_sha256, "entry": case.entry}

    def behavior_cached(self, case: Case) -> bool:
        """同じ入力 (``behavior_inputs``) で成功済みで、出力のハッシュも一致するときだけ True。

        入力が違う成功は再利用しない (False)。保存済みの出力が壊れている場合は、これまで通りエラーにする。
        """
        if not self._behavior_state_current(case):
            return False
        return self.cached("behavior", case.case_id, self.behavior_inputs(case, self.package.manifest_sha256))

    def _behavior_state_current(self, case: Case) -> bool:
        """成功済みの状態の入力が、現在の入力 (``behavior_inputs``) と全て同じか。成功済みでなければ True。"""
        expected = self.behavior_inputs(case, self.package.manifest_sha256)
        state = self.states("behavior").get(case.case_id, {})
        return state.get("status") != "ok" or all(state.get(k) == v for k, v in expected.items())

    def _retire_behavior_file(self, file: Path) -> None:
        """入力が変わった後の再検証で、前の結果を上書きせずに ``behavior/superseded/`` へ移す。"""
        if file.is_file():
            target = file.parent / "superseded" / f"{file.stem}.{sha256_file(file)[:12]}.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                file.replace(target)

    def behavior(self, cases: Sequence[Case]) -> List[Dict[str, Any]]:
        failures, rows = [], []
        for case in cases:
            file = self.dir / "behavior" / f"{case.case_id}.json"
            if self.behavior_cached(case):
                result = read_json(file)
            else:
                result = check_case(case, self.timeout)
                result["tests_sha256"] = case.tests_sha256
                result["entry"] = case.entry
                self._retire_behavior_file(file)
                write_json(file, result)
                if result["status"] == "ok":
                    self.done("behavior", case.case_id, [file],
                              **self.behavior_inputs(case, self.package.manifest_sha256))
                else:
                    self.set_state("behavior", case.case_id, "failed",
                                   reason="tests.json の期待値と一致しない、実行に失敗した、または構文エラー")
                    failures.append(case.case_id)
                print(f"behavior {case.case_id}: {result['status']} "
                      f"(original {result['versions']['original'].get('n_passed')}/{result['n_tests']}, "
                      f"transformed {result['versions']['transformed'].get('n_passed')}/{result['n_tests']}, "
                      f"LOC {case.source_loc['original']}->{case.source_loc['transformed']})", flush=True)
            rows.append({"case_id": case.case_id, "status": result["status"], "n_tests": result["n_tests"],
                         "passed_original": result["versions"]["original"].get("n_passed"),
                         "passed_transformed": result["versions"]["transformed"].get("n_passed"),
                         "ast_equal": result.get("ast_equal"), "loc_original": case.source_loc["original"],
                         "loc_transformed": case.source_loc["transformed"],
                         "loc_changed": result.get("loc_changed"),
                         "manifest_loc_matches": result.get("manifest_loc_matches")})
        write_csv(self.dir / "behavior" / "summary.csv", rows)
        self.log("behavior", cases=[c.case_id for c in cases], failed=failures)
        if failures:
            raise RuntimeError("動作検証に失敗: " + ", ".join(failures))
        return rows

    def require_behavior(self, cases: Sequence[Case]) -> None:
        missing = [c.case_id for c in cases if not self.behavior_cached(c)]
        if missing:
            raise RuntimeError("先に動作検証を成功させる必要がある: " + ", ".join(missing))

    # ----- 段階 2: 計測 -----------------------------------------------------
    def validate_parquet(self, file: Path) -> int:
        import pandas as pd

        frame = pd.read_parquet(file)
        if frame.empty:
            raise ValueError(f"空のトークン表: {file}")
        check_token_metrics(frame, self.allow_leading_surprisal_missing, label=str(file))
        for column, expected in ((PCol.META_MODEL_NAME, self.measure_cfg["model"]),
                                 (PCol.META_MODEL_REVISION, self.measure_cfg.get("revision"))):
            if expected and not frame[column].eq(expected).all():
                raise ValueError(f"モデルのメタデータが設定と違う: {file}/{column}")
        return len(frame)

    @staticmethod
    def _model_info(model: Any, measure_cfg: Dict[str, Any]) -> Dict[str, Any]:
        inner = getattr(model, "_model", None)
        return {
            "kind": measure_cfg.get("model_kind", "hf_causal_lm"),
            "name": getattr(model, "model_name", None), "revision": getattr(model, "model_revision", None),
            "tokenizer": getattr(model, "tokenizer_name", None),
            "device_configured": measure_cfg.get("device"), "device_resolved": getattr(model, "_device", None),
            "dtype_configured": measure_cfg.get("dtype"),
            "dtype_loaded": str(getattr(inner, "dtype", None)) if inner is not None else None,
        }

    def measure(self, cases: Sequence[Case], repetitions: Sequence[int], loader: Optional[Callable] = None,
                collector: Optional[Callable] = None, allow_model: bool = False) -> Dict[str, Any]:
        self.require_behavior(cases)
        todo, resumed = [], []
        for repetition in repetitions:
            for case in cases:
                for version in VERSIONS:
                    key = f"{rep_label(repetition)}/{case.case_id}/{version}"
                    if self.cached("measure", key, {"source_sha256": case.sha256[version]}):
                        resumed.append(key)
                    else:
                        todo.append((repetition, case, version, key))
        report = {"resumed": resumed, "measured": [], "failed": []}
        if todo and self.condition["model"]["kind"] != "dummy" and not allow_model:
            raise RuntimeError("モデルを読み込む計測は --run-model を付けたときだけ実行する")
        if todo:
            if loader is None or collector is None:
                from equivalence import measure as measure_module
                loader, collector = loader or measure_module.load_model, collector or measure_module.measure_file
            model = loader(self.measure_cfg)
            info = self._model_info(model, self.measure_cfg)
            for repetition, case, version, key in todo:
                source_path = self.input_path(case, version)
                out_dir = self.rep_dir(repetition) / "measure" / case.case_id
                parquet, record_path = out_dir / f"{version}.parquet", out_dir / f"{version}.json"
                out_dir.mkdir(parents=True, exist_ok=True)
                started, clock = runstate.now(), time.time()
                try:
                    collector(model, source_path, parquet, self.measure_cfg,
                              project=f"{KIND}/{case.case_id}/{version}/{rep_label(repetition)}")
                    n_tokens = self.validate_parquet(parquet)
                    write_json(record_path, {
                        "case_id": case.case_id, "version": version, "category": case.category,
                        "repetition": repetition, "repetition_label": rep_label(repetition),
                        "condition_key": self.key, "condition": self.condition,
                        "input_path": str(source_path.relative_to(self.dir)), "input_sha256": case.sha256[version],
                        "input_n_bytes": len(case.source_bytes(version)), "input_text": case.sources[version],
                        "total_tokens": n_tokens, "model": info, "thresholds": self.thresholds,
                        "validation": {"entropy": "all_finite",
                                       "surprisal": ("leading_missing_allowed"
                                                     if self.allow_leading_surprisal_missing else "all_finite")},
                        "started_at": started, "finished_at": runstate.now(), "elapsed_sec": time.time() - clock,
                        "environment": runstate.environment(), "code": runstate.git_info(paths.PROJECT_ROOT)})
                    self.done("measure", key, [parquet, record_path], tokens=n_tokens,
                              source_sha256=case.sha256[version])
                    report["measured"].append(key)
                    print(f"measure {key}: ok ({n_tokens} tokens)", flush=True)
                except Exception as exc:  # noqa: BLE001
                    self.set_state("measure", key, "failed", reason=f"{type(exc).__name__}: {exc}")
                    report["failed"].append(key)
                    print(f"measure {key}: failed: {exc}", flush=True)
        self.log("measure", repetitions=list(repetitions), cases=[c.case_id for c in cases], **report)
        if report["failed"]:
            raise RuntimeError("計測に失敗: " + ", ".join(report["failed"]))
        return report

    # ----- 段階 3: 比較 -----------------------------------------------------
    def compare(self, cases: Sequence[Case], repetitions: Sequence[int]) -> Dict[str, Any]:
        self.require_behavior(cases)
        report = {"resumed": [], "compared": []}
        for repetition in repetitions:
            for case in cases:
                for version in VERSIONS:
                    if not self.cached("measure", f"{rep_label(repetition)}/{case.case_id}/{version}",
                                       {"source_sha256": case.sha256[version]}):
                        raise RuntimeError(f"計測が成功していない: {rep_label(repetition)}/{case.case_id}/{version}")
                key = f"{rep_label(repetition)}/{case.case_id}"
                if self.cached("compare", key):
                    report["resumed"].append(key)
                    continue
                try:
                    self._compare_case(case, repetition, key)
                    report["compared"].append(key)
                    print(f"compare {key}: ok", flush=True)
                except Exception as exc:  # noqa: BLE001
                    self.set_state("compare", key, "failed", reason=f"{type(exc).__name__}: {exc}")
                    raise
        self.log("compare", repetitions=list(repetitions), cases=[c.case_id for c in cases], **report)
        return report

    def _compare_case(self, case: Case, repetition: int, key: str) -> None:
        import pandas as pd

        from equivalence import compare

        rep = self.rep_dir(repetition)
        folder = rep / "compare" / case.case_id
        frames = {v: pd.read_parquet(rep / "measure" / case.case_id / f"{v}.parquet") for v in VERSIONS}
        clean = {v: compare.clean(frames[v]) for v in VERSIONS}
        metrics = {v: compare.file_metrics(clean[v], self.thresholds) for v in VERSIONS}
        statements = {v: sa.parse_statements(case.sources[v]) for v in VERSIONS}
        owners = {v: sa.assign_tokens(clean[v], case.sources[v], statements[v]) for v in VERSIONS}
        tokens = {}
        for v in VERSIONS:
            table = compare.token_table(clean[v], metrics[v]["su"], {}, {}).drop(columns=["region", "partner_line"])
            tokens[v] = pd.concat([table, owners[v].drop(columns=["pos"])], axis=1)
            if len(tokens[v]) != metrics[v]["metrics"]["total_tokens"] or tokens[v]["owner"].isna().any():
                raise RuntimeError(f"トークンの割り当てが全トークンを覆っていない: {case.case_id}/{v}")
        alignment = sa.align_statements(statements["original"], statements["transformed"])
        table = sa.statement_table(statements["original"], statements["transformed"], case.sources["original"],
                                   case.sources["transformed"], tokens["original"], tokens["transformed"],
                                   alignment, self.labels)
        pair_of = {"original": {p["before_sid"]: p["pair_id"] for p in alignment["pairs"]},
                   "transformed": {p["after_sid"]: p["pair_id"] for p in alignment["pairs"]}}

        unit_rows, trigger_rows, su_json = [], [], {}
        for label in self.labels:
            su_json[label] = {}
            for v in VERSIONS:
                detail = metrics[v]["su"][label]
                su_json[label][v] = {
                    "count": detail["count"],
                    "units": [{k: u[k] for k in ("su_index", "start_line", "end_line", "start_token", "end_token",
                                                 "n_tokens", "trigger_tokens")} for u in detail["units"]],
                    "boundaries": [{"segment": s["segment"], "line": s["line"], "start_token": s["start_token"],
                                    "end_token": s["end_token"], "trigger_positions": s["triggers"]}
                                   for s in detail["segments"] if s["boundary"]],
                }
                for unit in detail["units"]:
                    unit_rows.append({"version": v, "threshold_label": label, "threshold": self.thresholds[label],
                                      **{k: unit[k] for k in ("su_index", "start_line", "end_line", "start_token",
                                                              "end_token", "n_tokens")},
                                      "trigger_tokens": json.dumps(unit["trigger_tokens"], ensure_ascii=False)})
                    for trig in unit["trigger_tokens"]:
                        owner = int(tokens[v]["owner"].iloc[trig["pos"]])
                        trigger_rows.append({
                            "version": v, "threshold_label": label, "threshold": self.thresholds[label],
                            "su_index": unit["su_index"], **trig, "text": compare.display_text(trig["token_str"]),
                            "owner_stmt": owner, "owner_type": tokens[v]["owner_type"].iloc[trig["pos"]],
                            "pair_id": pair_of[v].get(owner)})

        folder.mkdir(parents=True, exist_ok=True)
        for v in VERSIONS:
            tokens[v].to_csv(folder / f"tokens_{v}.csv", index=False)
        table.to_csv(folder / "statements.csv", index=False)
        write_csv(folder / "su_units.csv", unit_rows)
        write_csv(folder / "trigger_tokens.csv", trigger_rows,
                  ["version", "threshold_label", "threshold", "su_index", "pos", "idx", "token_str", "text",
                   "entropy", "line", "owner_stmt", "owner_type", "pair_id"])
        behavior_result = read_json(self.dir / "behavior" / f"{case.case_id}.json")
        summary = {
            "case": {"case_id": case.case_id, "category": case.category, "title": case.title,
                     "repetition": repetition, "repetition_label": rep_label(repetition),
                     "condition_key": self.key},
            "inputs": {v: {"sha256": case.sha256[v], "loc_declared": case.declared_loc[v],
                           "loc_source": case.source_loc[v]} for v in VERSIONS},
            "thresholds": self.thresholds,
            "behavior": {"status": behavior_result["status"], "n_tests": behavior_result["n_tests"],
                         "ast_equal": behavior_result.get("ast_equal"),
                         "passed": {v: behavior_result["versions"][v].get("n_passed") for v in VERSIONS}},
            "metrics": {v: metrics[v]["metrics"] for v in VERSIONS},
            "su": su_json,
            "alignment": {
                "n_statements": {"original": len(statements["original"]), "transformed": len(statements["transformed"])},
                "n_pairs": len(alignment["pairs"]),
                "n_same_subtree": sum(p["match"] == "same_subtree" for p in alignment["pairs"]),
                "n_same_head": sum(p["match"] == "same_head" for p in alignment["pairs"]),
                "unmatched_original": alignment["unmatched_before"],
                "unmatched_transformed": alignment["unmatched_after"],
                "pairs": alignment["pairs"],
            },
            "tokens": {v: {"n": len(tokens[v]), "n_crossing_boundary": int(tokens[v]["crosses_boundary"].sum()),
                           "n_whitespace": int(tokens[v]["is_whitespace"].sum()),
                           "n_outside_statements": int((tokens[v]["owner"] == sa.OUTSIDE).sum())}
                       for v in VERSIONS},
        }
        write_json(folder / "summary.json", summary)
        self.done("compare", key, sorted(p for p in folder.iterdir() if p.is_file() and not p.name.endswith(".tmp")))

    # ----- 段階 4: 一覧 -----------------------------------------------------
    def summary_rows(self, repetitions: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        rows = []
        existing = sorted(int(p.name.split("_")[1]) for p in self.dir.glob("rep_*") if p.is_dir())
        for repetition in (repetitions if repetitions is not None else existing):
            for case in self.package.cases:
                key = f"{rep_label(repetition)}/{case.case_id}"
                if not self.cached("compare", key):
                    continue
                summary = read_json(self.rep_dir(repetition) / "compare" / case.case_id / "summary.json")
                rows.append(summary_row(summary))
        return rows

    def summarize(self, repetitions: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        rows = self.summary_rows(repetitions)
        write_csv(self.dir / "summary_all.csv", rows)
        by_rep: Dict[int, List[Dict[str, Any]]] = {}
        for row in rows:
            by_rep.setdefault(row["repetition"], []).append(row)
        for repetition, rep_rows in by_rep.items():
            write_csv(self.rep_dir(repetition) / "summary.csv", rep_rows)
            (self.rep_dir(repetition) / "summary.md").write_text(render_markdown(rep_rows, self.labels), encoding="utf-8")
        (self.dir / "summary_all.md").write_text(render_markdown(rows, self.labels), encoding="utf-8")
        self.repeatability()
        self.log("summary", rows=len(rows))
        return rows

    def repeatability(self) -> List[Dict[str, Any]]:
        """同じ条件の反復どうしで、トークン列とエントロピーが再現するか (最初の反復との差)。"""
        import pandas as pd

        reps = sorted(int(p.name.split("_")[1]) for p in self.dir.glob("rep_*") if p.is_dir())
        rows = []
        for case in self.package.cases:
            for version in VERSIONS:
                base: Optional[Any] = None
                for repetition in reps:
                    key = f"{rep_label(repetition)}/{case.case_id}/{version}"
                    if not self.cached("measure", key, {"source_sha256": case.sha256[version]}):
                        continue
                    frame = pd.read_parquet(self.rep_dir(repetition) / "measure" / case.case_id / f"{version}.parquet")
                    if base is None:
                        base = (repetition, frame)
                        continue
                    same_tokens = (len(frame) == len(base[1]) and
                                   frame[PCol.TOKEN_STR].tolist() == base[1][PCol.TOKEN_STR].tolist())
                    row = {"case_id": case.case_id, "version": version, "base_repetition": base[0],
                           "repetition": repetition, "same_tokens": same_tokens}
                    for name, column in (("entropy", PCol.METRIC_ENTROPY), ("surprisal", PCol.METRIC_SURPRISAL)):
                        row[f"max_abs_{name}_diff"] = (
                            float((frame[column] - base[1][column]).abs().max()) if same_tokens else None)
                    rows.append(row)
        if rows:
            write_csv(self.dir / "repeatability.csv", rows)
        return rows

    def status(self, cases: Sequence[Case], repetitions: Sequence[int]) -> Dict[str, Any]:
        stale_behavior = {c.case_id for c in cases if not self._behavior_state_current(c)}

        def count(stage: str, keys: List[str]) -> Dict[str, Any]:
            states = self.states(stage)
            counts: Dict[str, int] = {}
            for key in keys:
                name = states.get(key, {}).get("status", "not_run")
                if stage == "behavior" and name == "ok" and key in stale_behavior:
                    name = "stale"  # tests.json か entry が変わり、古い成功は再利用しない
                counts[name] = counts.get(name, 0) + 1
            return {"expected": len(keys), **counts}

        return {
            "condition_key": self.key,
            "behavior": count("behavior", [c.case_id for c in cases]),
            "measure": count("measure", [f"{rep_label(r)}/{c.case_id}/{v}" for r in repetitions for c in cases
                                         for v in VERSIONS]),
            "compare": count("compare", [f"{rep_label(r)}/{c.case_id}" for r in repetitions for c in cases]),
        }


# ----------------------------------------------------------------------
# 一覧表
# ----------------------------------------------------------------------
def _delta(before: Any, after: Any) -> Any:
    return None if before is None or after is None else after - before


def summary_row(summary: Dict[str, Any]) -> Dict[str, Any]:
    case = summary["case"]
    labels = list(summary["thresholds"])
    row: Dict[str, Any] = {
        "repetition": case["repetition"], "condition_key": case["condition_key"], "category": case["category"],
        "case_id": case["case_id"], "title": case["title"],
        "behavior_status": summary["behavior"]["status"], "tests_passed": summary["behavior"]["passed"]["original"],
        "ast_equal": summary["behavior"]["ast_equal"],
    }
    before, after = summary["metrics"]["original"], summary["metrics"]["transformed"]
    names = ["loc", "total_tokens", "mean_entropy", "ppl"] + [f"su_count_{x}" for x in labels] + \
            [f"lm_cc_{x}" for x in labels]
    for name in names:
        row[f"{name}_before"], row[f"{name}_after"] = before.get(name), after.get(name)
        row[f"{name}_delta"] = _delta(before.get(name), after.get(name))
    loc_b, loc_a = summary["inputs"]["original"]["loc_source"], summary["inputs"]["transformed"]["loc_source"]
    row.update({"loc_source_before": loc_b, "loc_source_after": loc_a, "loc_source_delta": loc_a - loc_b})
    align = summary["alignment"]
    row.update({
        "n_statements_before": align["n_statements"]["original"], "n_statements_after": align["n_statements"]["transformed"],
        "n_statement_pairs": align["n_pairs"],
        "n_statements_unmatched": len(align["unmatched_original"]) + len(align["unmatched_transformed"]),
        "n_crossing_tokens_before": summary["tokens"]["original"]["n_crossing_boundary"],
        "n_crossing_tokens_after": summary["tokens"]["transformed"]["n_crossing_boundary"],
    })
    for label in labels:
        row[f"threshold_{label}"] = summary["thresholds"][label]
    return row


def render_markdown(rows: List[Dict[str, Any]], labels: List[str]) -> str:
    """LOC・トークン数・SU 数の前後と差の一覧 (Markdown)。"""
    def cell(row: Dict[str, Any], name: str) -> str:
        b, a, d = row.get(f"{name}_before"), row.get(f"{name}_after"), row.get(f"{name}_delta")
        return "-" if b is None or a is None else f"{b} → {a} ({d:+})"

    head = ["反復", "ケース", "動作", "LOC", "トークン数"] + [f"SU数 {x}" for x in labels]
    lines = ["| " + " | ".join(head) + " |", "| " + " | ".join(["---"] * len(head)) + " |"]
    for row in rows:
        values = [str(row["repetition"]), row["case_id"], row["behavior_status"], cell(row, "loc"),
                  cell(row, "total_tokens")] + [cell(row, f"su_count_{x}") for x in labels]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"
