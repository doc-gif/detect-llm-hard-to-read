"""等価変換実験を、ダミーモデルで transform → behavior → measure → compare → accuracy まで通すテスト。

lm-cc (テストデータ・プロンプト) が無い環境ではスキップする。API は呼ばない (偽の回答関数を使う)。
"""
import json

import pandas as pd
import pytest

import paths
from equivalence import accuracy
from equivalence.experiment import DEFAULT_CONFIG, Experiment, _merge

pytestmark = pytest.mark.skipif(not (paths.LM_CC_ROOT / "dataset" / "humaneval").exists(),
                                reason="lm-cc の dataset が無い")


def _config(tmp_path, **experiment):
    cfg = _merge(DEFAULT_CONFIG, {
        "experiment": {"name": "t", "dataset": "humaneval", "ids": ["HumanEval_123", "HumanEval_10"],
                       "output_root": str(tmp_path), **experiment},
        "measure": {"model": "dummy", "model_kind": "dummy", "device": "", "dtype": ""},
    })
    return cfg


def test_pipeline_end_to_end_and_resume(tmp_path):
    exp = Experiment(_config(tmp_path))
    assert exp.run_transform()["candidates_ok"] == 2          # HumanEval_123 の L3 / L8 (HumanEval_10 は候補なし)
    assert exp.run_behavior() == {"match": 2}
    assert exp.run_measure()["measured"] == 3                 # 元コード + 変換後2つ
    assert exp.run_compare()["compared"] == 2

    run = exp.run_dir
    tr = pd.read_csv(run / "transforms.csv")
    assert set(tr["status"]) == {"ok", "not_applicable"} and tr["reason"].notna().sum() == (tr["status"] != "ok").sum()
    assert (run / "codes" / "HumanEval_123" / "original.py").read_text() == \
        (paths.DATA_DIR / "humaneval" / "HumanEval_123.py").read_text()
    summary = pd.read_csv(run / "compare" / "summary.csv")
    assert list(summary["item_id"]) == ["HumanEval_123__ifelse_L3", "HumanEval_123__ifelse_L8"]
    assert summary["loc_equal"].all()
    for col in ("su_count_p67_before", "su_count_p67_after", "su_count_p67_delta", "mean_entropy_delta",
                "total_tokens_delta", "su_change_p80"):
        assert col in summary.columns
    d = run / "compare" / "HumanEval_123" / "ifelse_L3"
    for name in ("tokens_before.csv", "tokens_after.csv", "lines.csv", "token_alignment.csv", "regions.csv",
                 "summary.json", "report.html", "report.md"):
        assert (d / name).exists(), name
    manifest = json.loads((run / "manifest.json").read_text())
    assert "commit" in manifest["code"] and "python" in manifest["environment"]

    # 再実行しても成功済みは処理しない
    exp2 = Experiment(_config(tmp_path))
    assert exp2.run_measure()["measured"] == 0
    assert exp2.run_compare()["compared"] == 0
    assert len((run / "runs.jsonl").read_text().splitlines()) == 6

    # 計測条件を変えて同じディレクトリを使うとエラー
    cfg = _config(tmp_path)
    cfg["thresholds"] = {"p67": 0.5}
    with pytest.raises(ValueError):
        Experiment(cfg)

    # 回答精度: 入力の準備 → 偽の回答 → 採点 (失敗した試行だけ再実行)
    table = exp.run_accuracy_prepare()
    assert table["usable"].all() and len(table) == 3
    prompts = [json.loads(l) for l in (run / "accuracy" / "prompts.jsonl").read_text().splitlines()]
    for p in prompts:
        code = (run / "codes" / p["uid"] / f"{p['variant_id']}.py").read_text().strip("\n")
        assert p["prompt"].count(code) == 1                    # 計測したコードがプロンプトに入っている

    calls = []

    def flaky(prompt, cfg):
        calls.append(prompt)
        if len(calls) == 2:
            raise RuntimeError("API error")
        return "<<<Analysis>>>\n...\n<<<Output>>>\n[1, 5]\n[END-OF-RESPONSE]"

    cfg = dict(exp.config["accuracy"], trials=2)
    counts = accuracy.run_ier(exp.accuracy_dir(), cfg, caller=flaky)
    assert counts == {"done": 5, "skipped": 0, "failed": 1}
    assert accuracy.run_ier(exp.accuracy_dir(), cfg, only_failed=True, caller=flaky) == \
        {"done": 1, "skipped": 5, "failed": 0}
    out = accuracy.score_ier(exp.accuracy_dir(), cfg)
    acc = out["accuracy"].set_index("item_id")
    assert acc["complete"].all() and (acc["n_scored"] == 2).all()
    assert (acc["pass_at_1"] == 0.0).all()                     # 正解は [1, 5, 7, 11, 13, 17]
    assert set(out["comparison"]["item_id"]) == {"HumanEval_123__ifelse_L3", "HumanEval_123__ifelse_L8"}
