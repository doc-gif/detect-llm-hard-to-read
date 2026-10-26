"""if/else 入れ替え変換のテスト (構文・行数・行対応と、いくつかの入力での実行結果)。"""
import pytest

from equivalence.transforms import STATUS_FAILED, STATUS_NOT_APPLICABLE, STATUS_OK, create_transformation


def _apply_all(source, **options):
    t = create_transformation("if_else_swap", **options)
    return [t.apply(source, c) for c in t.find_candidates(source)]


def _run(source, fn, *args):
    ns = {}
    exec(source, ns)
    return ns[fn](*args)


SIMPLE = '''def f(x):
    if x > 0:
        y = 1
        z = 2
    else:
        y = -1
        z = -2
    return y + z
'''


def test_simple_swap_keeps_lines_and_behavior():
    (out,) = _apply_all(SIMPLE)
    assert out.status == STATUS_OK
    assert out.transformed_source == '''def f(x):
    if not (x > 0):
        y = -1
        z = -2
    else:
        y = 1
        z = 2
    return y + z
'''
    assert out.checks["line_count_equal"] and out.checks["ast_matches_expected"]
    for x in (-3, 0, 5, float("nan")):  # NaN でも比較演算子を反転しないので同じ結果
        assert _run(SIMPLE, "f", x) == _run(out.transformed_source, "f", x)


def test_line_map_follows_moved_bodies():
    (out,) = _apply_all(SIMPLE)
    m = {(lm.orig_line): (lm.new_line, lm.region) for lm in out.line_map}
    assert m[2] == (2, "if_header")
    assert m[3] == (6, "then_body") and m[4] == (7, "then_body")
    assert m[5] == (5, "between")
    assert m[6] == (3, "else_body") and m[7] == (4, "else_body")
    assert m[8] == (8, "after")
    new_lines = out.transformed_source.split("\n")
    old_lines = SIMPLE.split("\n")
    for lm in out.line_map:
        if lm.region not in ("if_header",):
            assert old_lines[lm.orig_line - 1] == new_lines[lm.new_line - 1]


def test_not_condition_is_unwrapped_or_wrapped():
    src = "def f(a):\n    if not a:\n        return 1\n    else:\n        return 2\n"
    (out,) = _apply_all(src)
    assert "    if a:\n        return 2\n" in out.transformed_source
    assert out.edits[0]["method"] == "remove_not"
    (out2,) = _apply_all(src, unwrap_not=False)
    assert "if not (not a):" in out2.transformed_source
    for a in (0, 1, [], [0], None):
        assert _run(src, "f", a) == _run(out.transformed_source, "f", a) == _run(out2.transformed_source, "f", a)


def test_atomic_condition_and_keyword_without_space():
    src = "def f(a, b):\n    if(a < b):\n        return a\n    else:\n        return b\n"
    (out,) = _apply_all(src)
    assert "    if not (a < b):\n" in out.transformed_source
    (out2,) = _apply_all("def g(xs):\n    if all(xs):\n        return 1\n    else:\n        return 0\n")
    assert "if not all(xs):" in out2.transformed_source


def test_boolean_operators_are_parenthesized():
    src = "def f(a, b):\n    if a and b or not a:\n        return 1\n    else:\n        return 0\n"
    (out,) = _apply_all(src)
    assert "if not (a and b or not a):" in out.transformed_source
    for a in (0, 1):
        for b in (0, 1):
            assert _run(src, "f", a, b) == _run(out.transformed_source, "f", a, b)


def test_walrus_and_multiline_condition():
    src = ("def f(xs):\n    if (n := len(xs)) > 2 and (\n            xs[0] > 0):\n        return n\n"
           "    else:\n        return -1\n")
    (out,) = _apply_all(src)
    assert out.status == STATUS_OK
    assert out.transformed_source.count("\n") == src.count("\n")
    for xs in ([1, 2, 3], [-1, 2, 3], [1]):
        assert _run(src, "f", xs) == _run(out.transformed_source, "f", xs)


def test_comments_and_blank_lines_outside_bodies_stay_in_place():
    src = ("def f(x):\n    if x:  # cond\n        a = 1\n\n    # before else\n    else:  # else\n"
           "        a = 2\n    return a\n")
    (out,) = _apply_all(src)
    assert out.transformed_source == ("def f(x):\n    if not x:  # cond\n        a = 2\n\n    # before else\n"
                                      "    else:  # else\n        a = 1\n    return a\n")


def test_nested_if_in_body_and_each_candidate_is_separate():
    src = ("def f(a, b):\n    if a:\n        if b:\n            r = 1\n        else:\n            r = 2\n"
           "    else:\n        r = 3\n    return r\n")
    outs = _apply_all(src)
    assert [o.status for o in outs] == [STATUS_OK, STATUS_OK]
    assert [o.candidate.variant_id for o in outs] == ["ifelse_L2", "ifelse_L3"]
    for o in outs:
        # 1か所ずつ、元コードに対して変換している
        assert sum(a != b for a, b in zip(src.split("\n"), o.transformed_source.split("\n"))) >= 1
        for a in (0, 1):
            for b in (0, 1):
                assert _run(src, "f", a, b) == _run(o.transformed_source, "f", a, b)


def test_last_line_without_newline():
    src = "x = 1\nif x:\n    y = 1\nelse:\n    y = 2"
    (out,) = _apply_all(src)
    assert out.transformed_source == "x = 1\nif not x:\n    y = 2\nelse:\n    y = 1"


@pytest.mark.parametrize("src, reason", [
    ("if a:\n    x = 1\n", "else 節が無い"),
    ("if a:\n    x = 1\nelif b:\n    x = 2\nelse:\n    x = 3\n", "elif"),
    ("if a: x = 1\nelse:\n    x = 2\n", "1行形式"),
    ("if a:\n    x = 1\nelse: x = 2\n", "1行形式"),
])
def test_not_applicable_with_reason(src, reason):
    (out,) = _apply_all(src)
    assert out.status == STATUS_NOT_APPLICABLE
    assert reason in out.reason


def test_python2_source_fails_with_reason():
    src = "if a:\n    print 'x'\nelse:\n    print 'y'\n"
    outs = _apply_all(src)
    assert outs and all(o.status in (STATUS_FAILED, STATUS_NOT_APPLICABLE) for o in outs)
    assert any("構文解析できない" in (o.reason or "") or "構文エラー" in (o.reason or "") for o in outs)


def test_not_spanning_lines_fails_instead_of_raising():
    # not を外すと行継続 (バックスラッシュ改行) ごと消えて行数が減るケースは failed として記録する
    src = "def f(x):\n    if not \\\n            x:\n        a = 1\n    else:\n        a = 2\n    return a\n"
    (out,) = _apply_all(src)
    assert out.status == STATUS_FAILED and "行数" in out.reason
    (out2,) = _apply_all(src, unwrap_not=False)  # not (...) を付ける方法なら行数は変わらない
    assert out2.status == STATUS_OK
    for x in (0, 1):
        assert _run(src, "f", x) == _run(out2.transformed_source, "f", x)
