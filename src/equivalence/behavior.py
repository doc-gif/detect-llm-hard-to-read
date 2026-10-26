"""変換前後の動作確認: 既存のテストデータで元コードと変換後コードを実行し、結果を比べる。

使うテスト (いずれも lm-cc の既存データ):
  - HumanEval (IER): 各ケースの ``input.txt`` の式を評価した値 (lm-cc の ``run.py`` と同じ手順) と、
    ``asserts.txt`` の ``check(candidate)`` の各 assert の真偽・左辺の値
  - xcodeeval (APR / CT): ``hidden_unit_tests`` の各入力を stdin に与えたときの stdout・終了コード・例外

判定 (``status``):
  - ``match``      : 全テストで変換前後の観測結果が一致した (= テストで一致を確認できた)
  - ``mismatch``   : 1つ以上のテストで観測結果が異なった
  - ``unverified`` : テストが無い・タイムアウトした等で確認できなかった (理由を記録)
  - ``not_run``    : 未実行

``match`` は「用意されたテスト入力で同じ結果になった」ことしか意味しない。
あらゆる入力に対する等価性の証明ではない。
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional

from equivalence import datasets as ds
from equivalence.scoring import normalize_ier_answer, xcodeeval_output_matches

STATUS_MATCH = "match"
STATUS_MISMATCH = "mismatch"
STATUS_UNVERIFIED = "unverified"
STATUS_NOT_RUN = "not_run"

_RUNNER = Path(__file__).resolve().parent / "_call_runner.py"


def _child_env() -> Dict[str, str]:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"          # set / dict の順序や hash 値を変換前後で揃える
    env["PYTHONIOENCODING"] = "utf-8"    # Windows でも stdout を UTF-8 で受け取る
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _run_call(spec: Dict[str, Any], timeout: float) -> Dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        spec_path, result_path = Path(tmp, "spec.json"), Path(tmp, "result.json")
        spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, str(_RUNNER), str(spec_path), str(result_path)],
                cwd=tmp, env=_child_env(), stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return {"timeout": True}
        if not result_path.exists():
            stderr = proc.stderr.decode("utf-8", errors="replace").strip().splitlines()
            return {"error": f"runner crashed (code {proc.returncode}): {stderr[-1] if stderr else ''}"}
        return json.loads(result_path.read_text(encoding="utf-8"))


def _run_stdin(code: str, stdin: str, timeout: float) -> Dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        code_path = Path(tmp, "main.py")
        code_path.write_bytes(code.encode("utf-8"))
        try:
            proc = subprocess.run(
                [sys.executable, str(code_path)], cwd=tmp, env=_child_env(),
                input=stdin.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return {"timeout": True}
        stderr_lines = proc.stderr.decode("utf-8", errors="replace").strip().splitlines()
        return {
            "stdout": proc.stdout.decode("utf-8", errors="replace"),
            "returncode": proc.returncode,
            "exception": stderr_lines[-1] if (proc.returncode != 0 and stderr_lines) else None,
        }


def _entry_name(input_expr: str) -> Optional[str]:
    try:
        node = ast.parse(input_expr.strip(), mode="eval").body
    except SyntaxError:
        return None
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return node.func.id
    return None


# ----------------------------------------------------------------------
# テストケースの用意
# ----------------------------------------------------------------------
def build_cases(spec: ds.DatasetSpec, uid: str) -> Dict[str, Any]:
    """``{"cases": [...], "notes": [...]}``。テストが無ければ cases は空。"""
    notes: List[str] = []
    cases: List[Dict[str, Any]] = []
    if spec.task == ds.TASK_IER:
        dirs = ds.humaneval_case_dirs(spec, uid)
        if not dirs:
            return {"cases": [], "notes": [f"lm-cc のテストデータが見つからない: {ds.lm_cc_dir(spec) / uid}"]}
        entry = None
        for d in dirs:
            input_path, output_path = d / "input.txt", d / "output.txt"
            if not input_path.exists():
                continue
            # lm-cc ier.py と同じく前後の改行を除く
            input_expr = input_path.read_text(encoding="utf-8").strip("\n")
            entry = entry or _entry_name(input_expr)
            cases.append({
                "case_id": f"input:{d.name}",
                "kind": "input",
                "input_expr": input_expr,
                "expected": output_path.read_text(encoding="utf-8") if output_path.exists() else None,
            })
        asserts_path = dirs[0] / "asserts.txt"
        if asserts_path.exists() and entry:
            cases.append({"case_id": "asserts", "kind": "asserts", "asserts_src": asserts_path.read_text(encoding="utf-8"),
                          "entry": entry})
        elif asserts_path.exists():
            notes.append("input.txt から関数名を特定できないため asserts.txt は使わない")
        return {"cases": cases, "notes": notes}

    record = ds.xcodeeval_record(spec, uid)
    if record is None:
        return {"cases": [], "notes": [f"lm-cc の問題レコードが見つからない: {spec.jsonl} ({uid})"]}
    tests = json.loads(record.get("hidden_unit_tests") or "[]")
    for i, test in enumerate(tests):
        cases.append({"case_id": f"hidden:{i}", "kind": "stdin", "input": test["input"], "expected": test["output"]})
    return {"cases": cases, "notes": notes}


def observe(code: str, case: Dict[str, Any], timeout: float) -> Dict[str, Any]:
    """1ケースを実行して観測結果を返す。"""
    if case["kind"] == "input":
        obs = _run_call({"mode": "input", "code": code, "input_expr": case["input_expr"]}, timeout)
        if case.get("expected") is not None and "str" in obs:
            obs["matches_expected"] = normalize_ier_answer(obs["str"]) == normalize_ier_answer(case["expected"])
        return obs
    if case["kind"] == "asserts":
        return _run_call({"mode": "asserts", "code": code, "asserts_src": case["asserts_src"],
                          "entry": case["entry"]}, timeout)
    obs = _run_stdin(code, case["input"], timeout)
    if "stdout" in obs:
        obs["matches_expected"] = xcodeeval_output_matches(obs["stdout"], case["expected"])
    return obs


def observe_all(code: str, cases: List[Dict[str, Any]], timeout: float, workers: int = 1,
                skip: Optional[List[bool]] = None) -> List[Dict[str, Any]]:
    """全ケースを実行する。各ケースは別プロセスなので ``workers`` 個まで並列に動かす。

    ``skip`` が真のケースは実行せずタイムアウト扱いにする (元コードがタイムアウトしたケースは
    どのみち一致を確認できないので、変換後コードを待たない)。
    """
    skip = skip or [False] * len(cases)

    def run(i: int) -> Dict[str, Any]:
        if skip[i]:
            return {"timeout": True, "skipped": "元コードがタイムアウトしたため実行していない"}
        return observe(code, cases[i], timeout)

    if workers <= 1:
        return [run(i) for i in range(len(cases))]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(run, range(len(cases))))


def _comparable(obs: Dict[str, Any]) -> Dict[str, Any]:
    """一致判定に使う部分 (正解との一致フラグは観測値から決まるので除く)。"""
    return {k: v for k, v in obs.items() if k != "matches_expected"}


def compare(cases: List[Dict[str, Any]], original: List[Dict[str, Any]],
            transformed: List[Dict[str, Any]], notes: Optional[List[str]] = None) -> Dict[str, Any]:
    """元コードと変換後コードの観測結果を比べて判定する。"""
    rows = []
    n_equal = n_timeout = 0
    for case, o, t in zip(cases, original, transformed):
        timeout = bool(o.get("timeout") or t.get("timeout"))
        equal = (not timeout) and _comparable(o) == _comparable(t)
        n_equal += equal
        n_timeout += timeout
        rows.append({
            "case_id": case["case_id"], "kind": case["kind"], "equal": equal, "timeout": timeout,
            "original": o, "transformed": t,
        })
    result: Dict[str, Any] = {"n_cases": len(cases), "n_equal": n_equal, "n_timeout": n_timeout,
                              "cases": rows, "notes": list(notes or [])}
    if not cases:
        result.update(status=STATUS_UNVERIFIED, reason="テストケースが無い")
    elif n_equal + n_timeout < len(cases):
        result.update(status=STATUS_MISMATCH, reason=f"{len(cases) - n_equal - n_timeout} ケースで結果が異なる")
    elif n_timeout:
        result.update(status=STATUS_UNVERIFIED, reason=f"{n_timeout} ケースがタイムアウトした")
    else:
        result.update(status=STATUS_MATCH, reason=None)
    return result
