"""候補の一覧 (scan)、データセット × 変換の設定展開、計測結果のキャッシュのテスト。"""
import json

import pandas as pd
import pytest

from equivalence import datasets as ds
from equivalence import measure, scan
from equivalence.experiment import DEFAULT_CONFIG, Experiment, build_configs, load_config

SAMPLE = "configs/equivalence/if_else_swap_humaneval_sample_dummy.toml"


def test_scan_counts_candidates_and_reasons():
    table = scan.scan_dataset("humaneval", "if_else_swap", ids=["HumanEval_123", "HumanEval_10", "HumanEval_0"])
    assert set(table["uid"]) == {"HumanEval_123", "HumanEval_10", "HumanEval_0"}  # 候補が無いファイルも残る
    s = scan.summarize(table).iloc[0]
    assert (s["files"], s["ok"]) == (3, 2)
    assert s["candidates"] == s["ok"] + s["not_applicable"] + s["failed"]
    reasons = scan.reason_counts(table)
    assert reasons["count"].sum() == s["not_applicable"] + s["failed"]
    assert scan.reason_group("Python 3 として構文解析できない: invalid syntax (line 3)") == "Python 3 として構文解析できない"
    assert scan.reason_group(float("nan")) is None


def test_build_configs_expands_dataset_and_transform(tmp_path):
    # 設定ファイルどおり
    (cfg,) = build_configs(SAMPLE)
    assert cfg["experiment"]["name"] == "if_else_swap_humaneval_sample_dummy"
    assert cfg["experiment"]["ids"] != "all"

    # データセットを差し替えると ids は全件、名前は既定の "{transform}_{dataset}"
    configs = build_configs(SAMPLE, datasets=["all"])
    assert [c["experiment"]["dataset"] for c in configs] == list(ds.DATASETS)
    assert configs[0]["experiment"]["ids"] != "all"                 # humaneval は設定ファイルのまま
    other = configs[1]["experiment"]
    assert other["ids"] == "all" and other["targets"] == []
    assert other["name"] == "if_else_swap_humaneval_simplified-top60"
    assert configs[1]["measure"]["model"] == "dummy"                # 他の設定は引き継ぐ

    # --ids は上書きとして残る。名前の指定は {dataset} を置き換える
    (cfg,) = build_configs(SAMPLE, datasets=["xcodeeval_apr"], name="x_{dataset}",
                           overrides={"experiment": {"ids": ["a"]}})
    assert cfg["experiment"]["name"] == "x_xcodeeval_apr" and cfg["experiment"]["ids"] == ["a"]

    # 設定ファイルなし (既定値) は dataset が必須
    with pytest.raises(ValueError):
        build_configs(None)
    (cfg,) = build_configs(None, datasets=["humaneval"])
    assert cfg["experiment"]["name"] == "if_else_swap_humaneval"
    assert load_config(None, {"experiment": {"dataset": "humaneval"}})["experiment"]["name"] == "if_else_swap_humaneval"

    # 名前が重複する組み合わせはエラー
    with pytest.raises(ValueError):
        build_configs(SAMPLE, datasets=["humaneval", "xcodeeval_apr"], name="same")


def _config(tmp_path, name):
    (cfg,) = build_configs(None, datasets=["humaneval"], name=name, overrides={
        "experiment": {"ids": ["HumanEval_123"], "output_root": str(tmp_path)},
        # 動作確認を省くため、判定に関係なく計測する
        "measure": {"model": "dummy", "model_kind": "dummy", "device": "", "dtype": "", "allowed_behavior": []},
    })
    return cfg


def test_measure_cache_reuses_same_code(tmp_path, monkeypatch):
    exp1 = Experiment(_config(tmp_path, "first"))
    exp1.run_transform()
    assert exp1.run_measure() == {"measured": 3, "cached": 0, "skipped": 0, "errors": 0}
    assert len(list((tmp_path / "_cache" / "measure").rglob("*.parquet"))) == 3

    # 別の実験でも、同じ条件・同じコードならモデルを読み込まずにキャッシュを使う
    def no_model(cfg):
        raise AssertionError("モデルを読み込んだ")

    monkeypatch.setattr(measure, "load_model", no_model)
    exp2 = Experiment(_config(tmp_path, "second"))
    exp2.run_transform()
    assert exp2.run_measure() == {"measured": 0, "cached": 3, "skipped": 0, "errors": 0}
    st = json.loads((exp2.run_dir / "status" / "measure.json").read_text())
    assert all(v["cache_hit"] for v in st.values())

    for p1 in (exp1.run_dir / "measure").rglob("*.parquet"):
        p2 = exp2.run_dir / p1.relative_to(exp1.run_dir)
        d1, d2 = pd.read_parquet(p1), pd.read_parquet(p2)
        assert d2["meta_file"].iloc[0] == str(exp2.code_path(p1.parent.name, p1.stem))   # この実験の値
        assert d1["meta_project"].iloc[0] == d2["meta_project"].iloc[0]
        pd.testing.assert_frame_equal(d1.drop(columns=["meta_file"]), d2.drop(columns=["meta_file"]))

    # 計測条件 (ここでは dtype) が違えばキャッシュは使わない
    cfg = _config(tmp_path, "third")
    cfg["measure"]["dtype"] = "float32"
    exp3 = Experiment(cfg)
    exp3.run_transform()
    with pytest.raises(AssertionError, match="モデルを読み込んだ"):
        exp3.run_measure()

    # cache = false なら使わない (同じディレクトリで切り替えてもよい)
    cfg = _config(tmp_path, "second")
    cfg["measure"]["cache"] = False
    exp4 = Experiment(cfg)
    exp4.state.set("measure", "HumanEval_123", "failed", reason="test")
    with pytest.raises(AssertionError, match="モデルを読み込んだ"):
        exp4.run_measure()


def test_cache_key_depends_on_content_and_conditions():
    m = dict(DEFAULT_CONFIG["measure"])
    k1, parts = measure.cache_key(b"x = 1\n", m)
    assert parts["source_sha256"] and "collector_version" in parts
    assert measure.cache_key(b"x = 1\n", dict(m, cache=False, allowed_behavior=[]))[0] == k1  # 計測に関係しない設定
    assert measure.cache_key(b"x = 2\n", m)[0] != k1
    assert measure.cache_key(b"x = 1\n", dict(m, model="other"))[0] != k1
