"""動作確認用の子プロセス: コードを実行し、関数呼び出しの結果や assert の結果を JSON に書く。

``python _call_runner.py <spec.json> <result.json>`` の形で behavior.py から呼ぶ。
対象コードの print が混ざらないよう、結果は stdout ではなくファイルに書く。

spec:
  {"mode": "input", "code": str, "input_expr": str}
      lm-cc の run.py と同じく「コードを実行 → output = <input_expr>」を行い str / repr を記録
  {"mode": "asserts", "code": str, "asserts_src": str, "entry": str}
      asserts.txt の check(candidate) を candidate=<entry> で実行する。各 assert は例外で
      止めずに、真偽と (比較式なら) 左辺の値を順に記録する
"""
import ast
import json
import sys

MAX_REPR = 2000


def _short(value):
    try:
        text = repr(value)
    except Exception as exc:  # noqa: BLE001
        text = f"<repr failed: {type(exc).__name__}>"
    return text if len(text) <= MAX_REPR else text[:MAX_REPR] + "...(truncated)"


def _err(exc):
    return f"{type(exc).__name__}: {exc}"[:MAX_REPR]


def _run_code(code):
    namespace = {"__name__": "__main__"}
    exec(compile(code, "<main>", "exec"), namespace)
    return namespace


class _AssertRecorder(ast.NodeTransformer):
    """``assert test`` を ``__record(i, lineno, ...)`` 呼び出しに置き換える。"""

    def __init__(self):
        self.count = 0

    def visit_Assert(self, node):
        i = self.count
        self.count += 1
        args = [ast.Constant(i), ast.Constant(node.lineno)]
        test = node.test
        if isinstance(test, ast.Compare):
            # 左辺は1回だけ評価し、その値で比較する (副作用・実行時間を元と同じにする)
            left = ast.Lambda(args=_no_args(), body=test.left)
            cmp = ast.Lambda(
                args=_no_args(["__v"]),
                body=ast.Compare(left=ast.Name("__v", ast.Load()), ops=test.ops, comparators=test.comparators),
            )
            call = ast.Call(ast.Name("__record_cmp", ast.Load()), args + [left, cmp], [])
        else:
            call = ast.Call(ast.Name("__record", ast.Load()), args + [ast.Lambda(args=_no_args(), body=test)], [])
        return ast.copy_location(ast.Expr(call), node)


def _no_args(names=()):
    return ast.arguments(posonlyargs=[], args=[ast.arg(n) for n in names], kwonlyargs=[],
                         kw_defaults=[], defaults=[])


def run_input(spec):
    ns = _run_code(spec["code"])
    try:
        output = eval(spec["input_expr"], ns)
    except Exception as exc:  # noqa: BLE001
        return {"error": _err(exc)}
    return {"str": str(output)[:MAX_REPR], "repr": _short(output), "error": None}


def run_asserts(spec):
    ns = _run_code(spec["code"])
    candidate = ns.get(spec["entry"])
    if candidate is None:
        return {"error": f"entry function not found: {spec['entry']}"}
    records = []

    def record(i, lineno, fn):
        try:
            records.append({"i": i, "line": lineno, "ok": bool(fn()), "value": None, "error": None})
        except Exception as exc:  # noqa: BLE001
            records.append({"i": i, "line": lineno, "ok": False, "value": None, "error": _err(exc)})

    def record_cmp(i, lineno, left_fn, cmp_fn):
        try:
            value = left_fn()
        except Exception as exc:  # noqa: BLE001
            records.append({"i": i, "line": lineno, "ok": False, "value": None, "error": _err(exc)})
            return
        try:
            ok = bool(cmp_fn(value))
            records.append({"i": i, "line": lineno, "ok": ok, "value": _short(value), "error": None})
        except Exception as exc:  # noqa: BLE001
            records.append({"i": i, "line": lineno, "ok": False, "value": _short(value), "error": _err(exc)})

    tree = ast.parse(spec["asserts_src"])
    tree = ast.fix_missing_locations(_AssertRecorder().visit(tree))
    check_ns = {"__name__": "__check__", "__record": record, "__record_cmp": record_cmp}
    exec(compile(tree, "<asserts>", "exec"), check_ns)
    check = check_ns.get("check")
    if check is None:
        return {"error": "check() not found in asserts"}
    try:
        check(candidate)
        tail_error = None
    except Exception as exc:  # noqa: BLE001
        tail_error = _err(exc)  # assert 以外の文で例外が出た場合
    return {"asserts": records, "error": tail_error}


def main():
    spec_path, result_path = sys.argv[1], sys.argv[2]
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    try:
        result = run_input(spec) if spec["mode"] == "input" else run_asserts(spec)
    except BaseException as exc:  # noqa: BLE001 - コード本体の例外 (SystemExit を含む) も記録する
        result = {"error": _err(exc), "error_phase": "exec"}
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
