"""loc_variation_9pairs 専用入口のテスト。モデルは読み込まない (計測はダミーのアダプタを使う)。"""
import json
import shutil
import zipfile
from pathlib import Path

import pandas as pd
import pytest

import paths
from equivalence import loc_variation as lv
from equivalence import statement_alignment as sa
from schema.records import ParquetSchema as PCol

ZIP = paths.PROJECT_ROOT / "loc_variation_9pairs.zip"
needs_zip = pytest.mark.skipif(not ZIP.exists(), reason="loc_variation_9pairs.zip がない")

CONFIG = """[experiment]
package = "unused.zip"
output = "results/loc_variation_test"
entry = "run"

[behavior]
timeout_sec = 10.0

[measure]
model = "dummy"
model_kind = "dummy"
context_strategy = "function_scope"

[thresholds]
p67 = 0.6813
p80_saved = 1.3238
"""


# ----------------------------------------------------------------------
# 小さなパッケージ (zip) を作る
# ----------------------------------------------------------------------
def make_package(tmp_path, original, transformed, tests, case_id="c01", prefix="pkg"):
    folder = tmp_path / "src_pkg" / prefix / "01_x" / case_id
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "original.py").write_text(original, encoding="utf-8")
    (folder / "transformed.py").write_text(transformed, encoding="utf-8")
    (folder / "tests.json").write_text(json.dumps(tests), encoding="utf-8")
    row = {"case_id": case_id, "category": "01_x", "title": "t",
           "original": f"01_x/{case_id}/original.py", "transformed": f"01_x/{case_id}/transformed.py",
           "original_LOC": len(original.splitlines()), "transformed_LOC": len(transformed.splitlines()),
           "test_count": len(tests), "original_sha256": lv.sha256_bytes(original.encode()),
           "transformed_sha256": lv.sha256_bytes(transformed.encode())}
    (tmp_path / "src_pkg" / prefix / "manifest.json").write_text(json.dumps([row]), encoding="utf-8")
    archive = tmp_path / "pkg.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        for path in sorted((tmp_path / "src_pkg" / prefix).rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(tmp_path / "src_pkg").as_posix())
    return archive


def make_run(tmp_path, package, output="out_root"):
    config = tmp_path / "config.toml"
    config.write_text(CONFIG, encoding="utf-8")
    return lv.LocVariationRun(config, package_path=package, output_root=tmp_path / output)


@pytest.fixture
def real_run(tmp_path):
    return make_run(tmp_path, ZIP)


# ----------------------------------------------------------------------
# 入力の取り込み
# ----------------------------------------------------------------------
@needs_zip
def test_real_zip_is_loaded_as_given():
    package = lv.load_package(ZIP)
    assert [c.case_id for c in package.cases] == [
        "s01_invoice", "s02_time", "s03_sales_report", "i01_absolute", "i02_shipping", "i03_order_report",
        "l01_sum", "l02_statistics", "l03_search_report"]
    for case in package.cases:
        assert len(case.tests) == 5
        assert case.declared_loc == case.source_loc  # manifest の LOC と行数が一致
        assert case.source_loc["transformed"] < case.source_loc["original"]  # LOC は変わる
        assert case.sha256["original"] == case.manifest_row["original_sha256"]
    assert package.file_sha256 and package.manifest_sha256


@needs_zip
def test_case_selection():
    package = lv.load_package(ZIP)
    assert [c.case_id for c in lv.select_cases(package, "first3")] == ["s01_invoice", "s02_time", "s03_sales_report"]
    assert len(lv.select_cases(package, "all")) == 9
    assert [c.case_id for c in lv.select_cases(package, "l01_sum,s01_invoice")] == ["s01_invoice", "l01_sum"]
    with pytest.raises(ValueError):
        lv.select_cases(package, "nothing")
    with pytest.raises(ValueError):
        lv.select_cases(package, "first:0")


def test_hash_mismatch_is_rejected(tmp_path):
    archive = make_package(tmp_path, "def run(x):\n    return x\n", "def run(x): return x\n", [{"args": [1], "expected": 1}])
    broken = tmp_path / "broken.zip"
    with zipfile.ZipFile(archive) as src, zipfile.ZipFile(broken, "w") as dst:
        for info in src.infolist():
            data = src.read(info)
            if info.filename.endswith("transformed.py"):
                data = data + b"# changed\n"
            dst.writestr(info.filename, data)
    with pytest.raises(ValueError, match="SHA-256"):
        lv.load_package(broken)


def test_path_traversal_in_manifest_is_rejected(tmp_path):
    archive = make_package(tmp_path, "def run(x):\n    return x\n", "def run(x): return x\n", [{"args": [1], "expected": 1}])
    evil = tmp_path / "evil.zip"
    with zipfile.ZipFile(archive) as src, zipfile.ZipFile(evil, "w") as dst:
        for info in src.infolist():
            data = src.read(info)
            if info.filename.endswith("manifest.json"):
                data = data.replace(b"01_x/c01/original.py", b"../outside.py")
            dst.writestr(info.filename, data)
    with pytest.raises(ValueError):
        lv.load_package(evil)


# ----------------------------------------------------------------------
# tests.json の args / expected
# ----------------------------------------------------------------------
@needs_zip
def test_all_nine_pairs_pass_their_tests_and_loc_change_is_not_a_failure():
    package = lv.load_package(ZIP)
    for case in package.cases:
        result = lv.check_case(case, timeout=10)
        assert result["status"] == "ok", case.case_id
        assert result["loc_changed"] is True
        assert result["ast_equal"] is True
        assert all(result["versions"][v]["n_passed"] == 5 for v in lv.VERSIONS)


def test_wrong_expected_value_fails(tmp_path):
    archive = make_package(tmp_path, "def run(x):\n    return x + 1\n", "def run(x): return x + 1\n",
                           [{"args": [1], "expected": 2}, {"args": [2], "expected": 99}])
    case = lv.load_package(archive).cases[0]
    result = lv.check_case(case, timeout=10)
    assert result["status"] == "failed"
    assert result["versions"]["original"]["n_passed"] == 1
    assert result["versions"]["original"]["results"][1]["matches"] is False


def test_loc_change_alone_is_not_a_failure_and_list_equals_tuple(tmp_path):
    archive = make_package(tmp_path, "def run(a, b):\n    c = a + b\n    return (c, a)\n",
                           "def run(a, b):\n    c = a + b; return (c, a)\n", [{"args": [1, 2], "expected": [3, 1]}])
    result = lv.check_case(lv.load_package(archive).cases[0], timeout=10)
    assert result["status"] == "ok" and result["loc_changed"] is True


def test_exception_missing_entry_and_timeout(tmp_path):
    archive = make_package(tmp_path, "def run(x):\n    return 1 / x\n", "def run(x): return 1 / x\n",
                           [{"args": [0], "expected": 0}])
    result = lv.check_case(lv.load_package(archive).cases[0], timeout=10)
    assert result["status"] == "failed" and "ZeroDivisionError" in result["versions"]["original"]["results"][0]["error"]
    assert lv.run_tests("def other():\n    pass\n", "run", [{"args": [], "expected": None}], 10)["load_error"]
    assert lv.run_tests("def run():\n    while True:\n        pass\n", "run", [{"args": [], "expected": None}], 1)["timeout"]


# ----------------------------------------------------------------------
# 文の対応 (位置情報を除いた AST)
# ----------------------------------------------------------------------
@needs_zip
def test_statements_are_paired_one_to_one_for_all_pairs():
    for case in lv.load_package(ZIP).cases:
        before = sa.parse_statements(case.sources["original"])
        after = sa.parse_statements(case.sources["transformed"])
        alignment = sa.align_statements(before, after)
        pairs = alignment["pairs"]
        assert len(before) == len(after) == len(pairs), case.case_id
        assert len({p["before_sid"] for p in pairs}) == len(pairs)  # 変換前の文は 1 回だけ
        assert len({p["after_sid"] for p in pairs}) == len(pairs)  # 変換後の文も 1 回だけ (重複使用なし)
        assert not alignment["unmatched_before"] and not alignment["unmatched_after"]
        assert all(p["match"] == "same_subtree" for p in pairs)


def test_alignment_ignores_positions_but_not_structure():
    one_line = "def run(a):\n    x = a; y = x + 1; return y\n"
    many_lines = "def run(a):\n    x = a\n    y = x + 1\n    return y\n"
    before, after = sa.parse_statements(many_lines), sa.parse_statements(one_line)
    assert [s.start_line for s in before] != [s.start_line for s in after]
    assert len(sa.align_statements(before, after)["pairs"]) == 4
    # 文が 1 つ増えると、増えた側だけが対応なしになる
    extra = sa.parse_statements("def run(a):\n    x = a\n    y = x + 1\n    z = 0\n    return y\n")
    alignment = sa.align_statements(before, extra)
    assert len(alignment["pairs"]) == 4 and len(alignment["unmatched_after"]) == 1
    # 同じ文が別の深さにあれば対応させない
    nested = sa.parse_statements("def run(a):\n    if a:\n        x = a\n    return a\n")
    flat = sa.parse_statements("def run(a):\n    x = a\n    if a:\n        pass\n    return a\n")
    pairs = sa.align_statements(nested, flat)["pairs"]
    assert all(nested[p["before_sid"]].depth == flat[p["after_sid"]].depth for p in pairs)


def test_else_branch_and_inline_body_keep_the_same_pairs():
    multi = "def run(s, m):\n    if s >= 5:\n        r = 0\n    else:\n        r = 5\n    return r\n"
    inline = "def run(s, m):\n    if s >= 5: r = 0\n    else: r = 5\n    return r\n"
    before, after = sa.parse_statements(multi), sa.parse_statements(inline)
    assert sa.ast_equal(multi, inline)
    assert [(p["before_sid"], p["after_sid"]) for p in sa.align_statements(before, after)["pairs"]] == [
        (i, i) for i in range(len(before))]


def _positions(source, starts):
    lines = source.split("\n")
    line_starts = [0]
    for line in lines[:-1]:
        line_starts.append(line_starts[-1] + len(line) + 1)
    rows = []
    for s in starts:
        line = max(i for i, ls in enumerate(line_starts) if ls <= s)
        rows.append({PCol.LINE: line + 1, PCol.COLUMN: s - line_starts[line]})
    return pd.DataFrame(rows)


def test_token_crossing_statement_boundary_is_assigned_once_and_recorded():
    source = "a = 1; b = 2\n"
    # "; b" は ";" (文の外) と "b" (2 つ目の文) にまたがる 1 トークン
    df = _positions(source, [0, 1, 3, 5, 8, 10, 12])
    statements = sa.parse_statements(source)
    owners = sa.assign_tokens(df, source, statements)
    assert len(owners) == len(df)  # 複製も分割もしない
    crossing = owners[owners["crosses_boundary"]]
    assert list(crossing["pos"]) == [3]
    assert int(crossing["owner"].iloc[0]) == sa.OUTSIDE  # 先頭の非空白文字 ";" の所有者
    assert crossing["spanned_owners"].iloc[0] == f"{sa.OUTSIDE},1"
    assert owners.loc[owners["pos"] == 6, "is_whitespace"].iloc[0]  # 末尾の改行
    # 各トークンの所有者は 1 つだけなので、所有者ごとの合計は全トークン数に一致する
    assert owners.groupby("owner").size().sum() == len(df)


# ----------------------------------------------------------------------
# 実行の管理 (ダミーのアダプタ。モデルは読み込まない)
# ----------------------------------------------------------------------
@needs_zip
def test_check_stage_creates_no_output(real_run, tmp_path):
    assert not (tmp_path / "out_root").exists()
    assert real_run.key and len(real_run.key) == 16


@needs_zip
def test_full_pipeline_with_dummy_model_resume_and_repetition(real_run, monkeypatch, tmp_path):
    from equivalence import measure as measure_module

    cases = lv.select_cases(real_run.package, "first3")
    calls = []
    original_collect = measure_module.measure_file

    def counting(model, source_path, output_path, cfg, project):
        calls.append(project)
        return original_collect(model, source_path, output_path, cfg, project)

    with real_run.locked():
        with pytest.raises(RuntimeError, match="動作検証"):
            real_run.measure(cases, [1])  # 動作検証の前には計測しない
        real_run.behavior(cases)
        report = real_run.measure(cases, [1], loader=measure_module.load_model, collector=counting)
        assert len(report["measured"]) == 6 and not report["resumed"]
        assert len(calls) == 6
        # 同じ条件・同じ反復は再開 (計測し直さない)
        report = real_run.measure(cases, [1], loader=measure_module.load_model, collector=counting)
        assert not report["measured"] and len(report["resumed"]) == 6 and len(calls) == 6
        # 別反復は別の保存先へ計測する
        report = real_run.measure(cases, [2], loader=measure_module.load_model, collector=counting)
        assert len(report["measured"]) == 6 and len(calls) == 12
        assert "rep_002" in calls[-1]
        # 3 組の後に全 9 組へ広げると、既存の 3 組は再開される
        everything = lv.select_cases(real_run.package, "all")
        real_run.behavior(everything)
        report = real_run.measure(everything, [1], loader=measure_module.load_model, collector=counting)
        assert len(report["resumed"]) == 6 and len(report["measured"]) == 12

        real_run.compare(everything, [1])
        real_run.compare(cases, [2])
        rows = real_run.summarize()

    assert len(rows) == 9 + 3
    row = next(r for r in rows if r["repetition"] == 1 and r["case_id"] == "s02_time")
    assert row["loc_source_before"] == 12 and row["loc_source_after"] == 3 and row["loc_source_delta"] == -9
    assert row["total_tokens_delta"] == row["total_tokens_after"] - row["total_tokens_before"]
    assert row["su_count_p67_before"] >= 1 and row["su_count_p80_saved_after"] >= 1
    assert row["behavior_status"] == "ok" and row["ast_equal"] is True
    assert (real_run.dir / "summary_all.csv").exists() and (real_run.dir / "summary_all.md").exists()

    # 保存内容: 実入力全文・ハッシュ・モデル・環境・条件
    record = json.loads((real_run.rep_dir(1) / "measure/s02_time/transformed.json").read_text(encoding="utf-8"))
    case = real_run.package.case("s02_time")
    assert record["input_text"] == case.sources["transformed"]
    assert record["input_sha256"] == case.sha256["transformed"]
    assert record["repetition"] == 1 and record["condition_key"] == real_run.key
    assert record["model"]["name"] == "dummy" and "device_configured" in record["model"]
    assert record["environment"]["python"] and record["condition"]["thresholds"]["p67"] == 0.6813

    # 比較の出力: SU の数・境界・範囲・原因トークン・閾値、文の表
    folder = real_run.rep_dir(1) / "compare/s02_time"
    summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
    assert summary["thresholds"] == {"p67": 0.6813, "p80_saved": 1.3238}
    for label in ("p67", "p80_saved"):
        for version in lv.VERSIONS:
            detail = summary["su"][label][version]
            assert detail["count"] == len(detail["units"])
            assert detail["count"] == summary["metrics"][version][f"su_count_{label}"]
            assert len(detail["boundaries"]) + 1 == detail["count"]
            for unit in detail["units"][1:]:
                assert unit["trigger_tokens"]  # 境界を作ったトークンが残っている
    triggers = pd.read_csv(folder / "trigger_tokens.csv")
    assert {"entropy", "threshold", "owner_stmt", "pair_id"} <= set(triggers.columns)
    assert (triggers["entropy"] >= triggers["threshold"]).all()
    statements = pd.read_csv(folder / "statements.csv")
    assert (statements["match"] == "same_subtree").sum() == summary["alignment"]["n_pairs"]
    for version in lv.VERSIONS:  # 全トークンがちょうど 1 つの所有者に割り当てられる
        tokens = pd.read_csv(folder / f"tokens_{version}.csv")
        assert len(tokens) == summary["metrics"][version]["total_tokens"]
        assert tokens["owner"].notna().all()
    assert (real_run.dir / "repeatability.csv").exists()
    repeat = pd.read_csv(real_run.dir / "repeatability.csv")
    assert repeat["same_tokens"].all() and (repeat["max_abs_entropy_diff"] == 0).all()

    # 保存した出力が変わっていたら、上書きせずにエラーにする
    parquet = real_run.rep_dir(1) / "measure/s01_invoice/original.parquet"
    parquet.write_bytes(parquet.read_bytes() + b"x")
    fresh = lv.LocVariationRun(real_run.config_path, package_path=ZIP, output_root=real_run.output_root)
    with fresh.locked():
        with pytest.raises(ValueError, match="上書きしない"):
            fresh.measure(cases, [1], loader=measure_module.load_model, collector=counting)


@needs_zip
def test_model_measurement_requires_explicit_permission(tmp_path):
    config = tmp_path / "config.toml"
    config.write_text(CONFIG.replace('model_kind = "dummy"', 'model_kind = "hf_causal_lm"')
                      .replace('model = "dummy"', 'model = "not-downloaded/model"'), encoding="utf-8")
    run = lv.LocVariationRun(config, package_path=ZIP, output_root=tmp_path / "out_root")
    cases = lv.select_cases(run.package, "first3")
    with run.locked():
        run.behavior(cases)
        loaded = []
        with pytest.raises(RuntimeError, match="--run-model"):
            run.measure(cases, [1], loader=lambda cfg: loaded.append(cfg), collector=lambda *a, **k: None)
        assert not loaded  # モデルの読み込みに入る前に止まる


@needs_zip
def test_conditions_and_output_roots_are_separated(tmp_path):
    base = make_run(tmp_path, ZIP)
    config = tmp_path / "other.toml"
    config.write_text(CONFIG.replace("0.6813", "0.7"), encoding="utf-8")
    other = lv.LocVariationRun(config, package_path=ZIP, output_root=tmp_path / "out_root")
    assert base.key != other.key and base.dir != other.dir  # 条件が違えば別ディレクトリ
    for protected in (paths.DATA_DIR / "x", paths.OUT_DIR / "x", paths.RESULTS_DIR / "summaries",
                      paths.PROJECT_ROOT / "experiments" / "x"):
        with pytest.raises(ValueError):
            lv.LocVariationRun(base.config_path, package_path=ZIP, output_root=protected)
    occupied = tmp_path / "occupied"
    occupied.mkdir()
    (occupied / "keep.txt").write_text("existing")
    with pytest.raises(ValueError):
        lv.LocVariationRun(base.config_path, package_path=ZIP, output_root=occupied)
    assert (occupied / "keep.txt").read_text() == "existing"


def test_failed_behavior_blocks_measurement(tmp_path):
    archive = make_package(tmp_path, "def run(x):\n    return x\n", "def run(x): return x\n", [{"args": [1], "expected": 2}])
    run = make_run(tmp_path, archive)
    cases = run.package.cases
    with run.locked():
        with pytest.raises(RuntimeError, match="動作検証に失敗"):
            run.behavior(cases)
        with pytest.raises(RuntimeError, match="先に動作検証"):
            run.measure(cases, [1], loader=lambda cfg: None, collector=lambda *a, **k: None)


# ----------------------------------------------------------------------
# 計測結果 (Parquet) の指標列の検査: entropy と surprisal は別の規則
# ----------------------------------------------------------------------
INF = float("inf")
NAN = float("nan")


def metric_frame(entropy, surprisal, idx=None):
    n = len(entropy)
    return pd.DataFrame({PCol.IDX: list(range(n)) if idx is None else idx,
                         PCol.METRIC_ENTROPY: entropy, PCol.METRIC_SURPRISAL: surprisal})


def test_metrics_all_finite_pass():
    lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [0.1, 0.2, 0.3]))
    lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [0.1, 0.2, 0.3]), allow_leading_surprisal_missing=True)


@pytest.mark.parametrize("allow_leading", [False, True])
def test_entropy_all_missing_is_rejected(allow_leading):
    for missing in (None, NAN):
        frame = metric_frame([missing] * 3, [0.1, 0.2, 0.3])
        with pytest.raises(ValueError, match="entropy が全件欠損"):
            lv.check_token_metrics(frame, allow_leading)


@pytest.mark.parametrize("allow_leading", [False, True])
@pytest.mark.parametrize("position", [0, 1, 2])
def test_entropy_partial_missing_is_rejected_even_for_the_first_token(allow_leading, position):
    for missing in (None, NAN):
        values = [0.5, 1.0, 2.0]
        values[position] = missing
        with pytest.raises(ValueError, match="entropy が一部欠損 \\(1/3 件\\)"):
            lv.check_token_metrics(metric_frame(values, [0.1, 0.2, 0.3]), allow_leading)


@pytest.mark.parametrize("bad", [INF, -INF])
def test_entropy_non_finite_is_rejected(bad):
    with pytest.raises(ValueError, match="entropy に非有限値"):
        lv.check_token_metrics(metric_frame([0.5, bad, 2.0], [0.1, 0.2, 0.3]))
    # 欠損と非有限値は別のエラーである
    with pytest.raises(ValueError, match="entropy に非有限値"):
        lv.check_token_metrics(metric_frame([bad] * 3, [0.1, 0.2, 0.3]))


def test_surprisal_is_strict_by_default():
    with pytest.raises(ValueError, match="surprisal が一部欠損 \\(1/3 件\\)"):
        lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [None, 0.2, 0.3]))
    with pytest.raises(ValueError, match="surprisal が全件欠損"):
        lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [None] * 3))
    with pytest.raises(ValueError, match="surprisal に非有限値"):
        lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [0.1, INF, 0.3]))


def test_leading_surprisal_missing_is_a_separate_explicit_rule():
    frame = metric_frame([0.5, 1.0, 2.0], [None, 0.2, 0.3])
    lv.check_token_metrics(frame, allow_leading_surprisal_missing=True)  # 先頭だけの欠損は許す
    lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [NAN, 0.2, 0.3]), allow_leading_surprisal_missing=True)
    # 先頭以外の欠損・非有限値・全件欠損は、許す設定でも拒否する
    with pytest.raises(ValueError, match="surprisal が先頭以外が欠損 \\(1/3 件\\)"):
        lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [None, None, 0.3]), allow_leading_surprisal_missing=True)
    with pytest.raises(ValueError, match="surprisal が先頭以外が欠損"):
        lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [0.1, 0.2, None]), allow_leading_surprisal_missing=True)
    with pytest.raises(ValueError, match="surprisal が全件欠損"):
        lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [None] * 3), allow_leading_surprisal_missing=True)
    with pytest.raises(ValueError, match="surprisal に非有限値"):
        lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [None, INF, 0.3]), allow_leading_surprisal_missing=True)
    # 先頭の判定は行の並びではなく idx が最小の行で行う
    shuffled = metric_frame([0.5, 1.0, 2.0], [0.1, None, 0.3], idx=[2, 0, 1])
    lv.check_token_metrics(shuffled, allow_leading_surprisal_missing=True)
    with pytest.raises(ValueError, match="surprisal が先頭以外が欠損"):
        lv.check_token_metrics(metric_frame([0.5, 1.0, 2.0], [None, 0.2, 0.3], idx=[2, 0, 1]),
                               allow_leading_surprisal_missing=True)


def test_leading_surprisal_missing_does_not_relax_entropy():
    # BOS を持たないモデルでは先頭の surprisal と entropy が両方欠ける。entropy は例外なしなので拒否する。
    with pytest.raises(ValueError, match="entropy が一部欠損"):
        lv.check_token_metrics(metric_frame([None, 1.0, 2.0], [None, 0.2, 0.3]), allow_leading_surprisal_missing=True)


def parquet_frame(entropy, surprisal):
    frame = metric_frame(entropy, surprisal)
    frame[PCol.META_MODEL_NAME] = "dummy"
    frame[PCol.META_MODEL_REVISION] = None
    return frame


def test_validate_parquet_rejects_missing_and_non_finite_entropy(tmp_path):
    run = make_run(tmp_path, make_package(tmp_path, "def run(x):\n    return x\n", "def run(x): return x\n",
                                          [{"args": [1], "expected": 1}]))
    good = tmp_path / "good.parquet"
    parquet_frame([0.5, 1.0, 2.0], [0.1, 0.2, 0.3]).to_parquet(good)
    assert run.validate_parquet(good) == 3
    for name, entropy, message in (("all_missing", [None] * 3, "全件欠損"),
                                   ("partial", [0.5, None, 2.0], "一部欠損"),
                                   ("nan", [0.5, NAN, 2.0], "一部欠損"),
                                   ("inf", [0.5, INF, 2.0], "非有限値")):
        file = tmp_path / f"{name}.parquet"
        parquet_frame(entropy, [0.1, 0.2, 0.3]).to_parquet(file)
        with pytest.raises(ValueError, match=message):
            run.validate_parquet(file)


def test_validate_parquet_follows_the_configured_surprisal_rule(tmp_path):
    package = make_package(tmp_path, "def run(x):\n    return x\n", "def run(x): return x\n",
                           [{"args": [1], "expected": 1}])
    file = tmp_path / "leading.parquet"
    parquet_frame([0.5, 1.0, 2.0], [None, 0.2, 0.3]).to_parquet(file)
    strict = make_run(tmp_path, package)
    assert strict.allow_leading_surprisal_missing is False
    with pytest.raises(ValueError, match="surprisal が一部欠損"):
        strict.validate_parquet(file)
    config = tmp_path / "config_lenient.toml"
    config.write_text(CONFIG + "\n[validation]\nallow_leading_surprisal_missing = true\n", encoding="utf-8")
    lenient = lv.LocVariationRun(config, package_path=package, output_root=tmp_path / "out_lenient")
    assert lenient.allow_leading_surprisal_missing is True
    assert lenient.validate_parquet(file) == 3
    # 許す設定でも、entropy の先頭欠損は許さない
    both = tmp_path / "both.parquet"
    parquet_frame([None, 1.0, 2.0], [None, 0.2, 0.3]).to_parquet(both)
    with pytest.raises(ValueError, match="entropy が一部欠損"):
        lenient.validate_parquet(both)


def test_shipped_config_uses_the_strict_surprisal_rule():
    import tomllib

    config = tomllib.loads((paths.PROJECT_ROOT / "configs/equivalence/loc_variation_9pairs.toml")
                           .read_text(encoding="utf-8"))
    assert config["validation"]["allow_leading_surprisal_missing"] is False


def test_failed_validation_is_not_saved_as_success(tmp_path):
    run = make_run(tmp_path, make_package(tmp_path, "def run(x):\n    return x\n", "def run(x): return x\n",
                                          [{"args": [1], "expected": 1}]))
    cases = list(run.package.cases)

    def bad_collector(model, source_path, output_path, cfg, project):
        parquet_frame([None] * 3, [0.1, 0.2, 0.3]).to_parquet(output_path)  # entropy が全件欠損

    with run.locked():
        run.behavior(cases)
        with pytest.raises(RuntimeError, match="計測に失敗"):
            run.measure(cases, [1], loader=lambda cfg: object(), collector=bad_collector)
        assert all(s["status"] == "failed" for s in run.states("measure").values())
        assert "全件欠損" in next(iter(run.states("measure").values()))["reason"]


# ----------------------------------------------------------------------
# 動作検証の再開: tests_sha256 と実効的な entry が同じときだけ成功を再利用する
# ----------------------------------------------------------------------
BEHAVIOR_SOURCE = "def run(x):\n    return x * 2\n\n\ndef main(x):\n    return x * 3\n"
BEHAVIOR_TRANSFORMED = "def run(x): return x * 2\n\n\ndef main(x): return x * 3\n"


@pytest.fixture
def behavior_counter(monkeypatch):
    calls = []
    real = lv.run_tests

    def counting(source, entry, tests, timeout):
        calls.append(entry)
        return real(source, entry, tests, timeout)

    monkeypatch.setattr(lv, "run_tests", counting)
    return calls


def run_with_entry(tmp_path, package, entry="run"):
    config = tmp_path / f"config_{entry}.toml"
    config.write_text(CONFIG.replace('entry = "run"', f'entry = "{entry}"'), encoding="utf-8")
    return lv.LocVariationRun(config, package_path=package, output_root=tmp_path / "out_root")


def test_behavior_success_is_reused_for_the_same_tests_and_entry(tmp_path, behavior_counter):
    package = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [2], "expected": 4}])
    run = run_with_entry(tmp_path, package)
    with run.locked():
        run.behavior(run.package.cases)
        assert len(behavior_counter) == 2  # original と transformed
        run.behavior(run.package.cases)
        assert len(behavior_counter) == 2  # 同じ入力なので再利用する
    case = run.package.cases[0]
    state = json.loads((run.dir / "status/behavior.json").read_text(encoding="utf-8"))[case.case_id]
    assert state["tests_sha256"] == case.tests_sha256 and state["entry"] == "run"


def test_changed_args_and_expected_with_the_same_test_count_are_not_reused(tmp_path, behavior_counter):
    package = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [2], "expected": 4}])
    first = run_with_entry(tmp_path, package)
    with first.locked():
        first.behavior(first.package.cases)
    assert len(behavior_counter) == 2

    # 件数 (1) も manifest も同じまま、args と expected だけを変える。結果は両方とも成功する。
    changed = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [5], "expected": 10}])
    second = run_with_entry(tmp_path, changed)
    assert second.package.manifest_sha256 == first.package.manifest_sha256
    assert second.key == first.key  # 条件キーは同じ。それでも古い成功は使わない
    assert second.package.cases[0].tests_sha256 != first.package.cases[0].tests_sha256
    assert len(second.package.cases[0].tests) == len(first.package.cases[0].tests)
    with second.locked():
        second.behavior(second.package.cases)
        assert len(behavior_counter) == 4  # 検証し直した
        second.behavior(second.package.cases)
        assert len(behavior_counter) == 4  # 新しい入力の成功は次から再利用する
    saved = json.loads((second.dir / "behavior/c01.json").read_text(encoding="utf-8"))
    assert saved["tests_sha256"] == second.package.cases[0].tests_sha256
    assert saved["versions"]["original"]["results"][0]["args"] == [5]
    # 前の結果は上書きせずに残す
    old = list((second.dir / "behavior/superseded").glob("c01.*.json"))
    assert len(old) == 1
    assert json.loads(old[0].read_text(encoding="utf-8"))["versions"]["original"]["results"][0]["args"] == [2]


def test_stale_behavior_blocks_measurement_until_it_is_run_again(tmp_path, behavior_counter):
    package = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [2], "expected": 4}])
    first = run_with_entry(tmp_path, package)
    with first.locked():
        first.behavior(first.package.cases)
    changed = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [5], "expected": 10}])
    second = run_with_entry(tmp_path, changed)
    with second.locked():
        with pytest.raises(RuntimeError, match="先に動作検証"):
            second.require_behavior(second.package.cases)
        with pytest.raises(RuntimeError, match="先に動作検証"):
            second.measure(second.package.cases, [1], loader=lambda cfg: None, collector=lambda *a, **k: None)


def test_changed_entry_is_not_reused(tmp_path, behavior_counter):
    # run は x*2、main は x*3。同じ tests.json では entry によって成否が変わる。
    package = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [2], "expected": 4}])
    first = run_with_entry(tmp_path, package, "run")
    with first.locked():
        first.behavior(first.package.cases)
    assert behavior_counter == ["run", "run"]

    second = run_with_entry(tmp_path, package, "main")
    assert second.key == first.key and second.package.cases[0].entry == "main"
    assert second.package.manifest_sha256 == first.package.manifest_sha256
    assert second.package.cases[0].tests_sha256 == first.package.cases[0].tests_sha256
    with second.locked():
        with pytest.raises(RuntimeError, match="動作検証に失敗"):  # main(2) は 6 で、期待値 4 と合わない
            second.behavior(second.package.cases)
        assert behavior_counter == ["run", "run", "main", "main"]  # 古い成功は使わなかった
        assert second.states("behavior")["c01"]["status"] == "failed"
        with pytest.raises(RuntimeError, match="先に動作検証"):
            second.require_behavior(second.package.cases)
    assert list((second.dir / "behavior/superseded").glob("c01.*.json"))


def test_manifest_entry_is_the_effective_entry(tmp_path, behavior_counter):
    package = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [2], "expected": 4}])
    run = run_with_entry(tmp_path, package, "main")  # 設定は main だが、manifest の行が run を指す
    row_path = tmp_path / "src_pkg/pkg/manifest.json"
    rows = json.loads(row_path.read_text(encoding="utf-8"))
    rows[0]["entry"] = "run"
    row_path.write_text(json.dumps(rows), encoding="utf-8")
    with zipfile.ZipFile(tmp_path / "with_entry.zip", "w") as zf:
        for path in sorted((tmp_path / "src_pkg/pkg").rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(tmp_path / "src_pkg").as_posix())
    with_entry = run_with_entry(tmp_path, tmp_path / "with_entry.zip", "main")
    assert with_entry.package.cases[0].entry == "run"  # 実効的な entry は manifest の値
    assert run.package.cases[0].entry == "main"
    inputs = lv.LocVariationRun.behavior_inputs(with_entry.package.cases[0], with_entry.package.manifest_sha256)
    assert inputs["entry"] == "run"


def test_old_state_without_tests_sha256_and_entry_is_run_again(tmp_path, behavior_counter):
    package = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [2], "expected": 4}])
    first = run_with_entry(tmp_path, package)
    with first.locked():
        first.behavior(first.package.cases)
    status_file = first.dir / "status/behavior.json"
    states = json.loads(status_file.read_text(encoding="utf-8"))
    for key in ("tests_sha256", "entry"):
        states["c01"].pop(key)
    status_file.write_text(json.dumps(states), encoding="utf-8")
    second = run_with_entry(tmp_path, package)
    with second.locked():
        second.behavior(second.package.cases)
    assert len(behavior_counter) == 4


def test_status_reports_stale_behavior(tmp_path, behavior_counter):
    package = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [2], "expected": 4}])
    first = run_with_entry(tmp_path, package)
    with first.locked():
        first.behavior(first.package.cases)
        assert first.status(first.package.cases, [1])["behavior"] == {"expected": 1, "ok": 1}
    changed = make_package(tmp_path, BEHAVIOR_SOURCE, BEHAVIOR_TRANSFORMED, [{"args": [5], "expected": 10}])
    second = run_with_entry(tmp_path, changed)
    assert second.status(second.package.cases, [1])["behavior"] == {"expected": 1, "stale": 1}
