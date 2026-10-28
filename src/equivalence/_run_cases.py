"""tests.json の args を関数に渡して結果を JSON に書く子プロセス。

``python _run_cases.py <spec.json> <result.json>`` の形で ``loc_variation.py`` から呼ぶ。
対象コードの print が混ざらないよう、結果は stdout ではなくファイルに書く。

spec: {"code": str, "entry": str, "cases": [{"args": [...]}]}
result: {"load_error": str | None, "results": [{"value": JSON値 | None, "error": str | None}]}
値は JSON に往復させて保存する。tuple と list は同じ表現になる。
"""
import json
import sys

MAX_ERROR = 2000


def _err(exc):
    return f"{type(exc).__name__}: {exc}"[:MAX_ERROR]


def main():
    spec_path, result_path = sys.argv[1], sys.argv[2]
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    result = {"load_error": None, "results": []}
    try:
        namespace = {"__name__": "__main__"}
        exec(compile(spec["code"], "<case>", "exec"), namespace)
        function = namespace.get(spec["entry"])
        if not callable(function):
            raise NameError(f"entry function not found: {spec['entry']}")
    except BaseException as exc:  # noqa: BLE001 - コード本体の例外 (SystemExit を含む) も記録する
        result["load_error"] = _err(exc)
        function = None
    if function is not None:
        for case in spec["cases"]:
            try:
                value = json.loads(json.dumps(function(*case["args"]), ensure_ascii=False))
                result["results"].append({"value": value, "error": None})
            except BaseException as exc:  # noqa: BLE001
                result["results"].append({"value": None, "error": _err(exc)})
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
