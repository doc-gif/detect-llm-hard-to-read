"""回答精度 (pass@1) の評価を、元コードと変換後コードで同じ条件にそろえて行うための処理。

回答モデルは lm-cc と同じく OpenAI 互換 API (既定 deepseek-v3) で、エントロピーを計測する
モデル (CodeLlama-7b) とは別。プロンプト・採点は lm-cc の実装に合わせる:

- HumanEval (IER): プロンプトは lm-cc ``scripts/tasks/ier/create_prompt_ier.py`` の
  ``create_prompt`` を lm-cc から直接読み込んで作る (コピーしない)。コードは ``strip("\\n")``
  してから渡す (lm-cc ``ier.py`` と同じ)。API 呼び出しの設定は ``prompt.chatgpt_generator``
  (system ロール、temperature 0、max_tokens 1024)、採点は ``parse_result`` と同じ。
  正解は ``output.txt``。変換後コードでは、動作確認でそのケースの返り値が元コードと一致した
  ときだけ同じ正解を使う (一致を確認できていないものは採点しない)。
- xcodeeval (APR / CT): lm-cc の ``generate_apr.py`` / ``generate_ct.py`` / ``evaluate_*.py`` を
  そのまま使う。ここでは問題レコードのコード欄を変換後コードに置き換えた jsonl を書き出し
  (``prepare``)、lm-cc の評価結果 (``*_details.jsonl``) を読み戻して同じ形式の表にする (``import``)。
  正解は問題ごとの hidden tests なので変換後もそのまま使える (コードの動作確認が一致した場合)。
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

import paths
from equivalence import datasets as ds
from equivalence.behavior import STATUS_MATCH
from equivalence.scoring import extract_ier_prediction, ier_is_correct, pass_at_1

# lm-cc ``prompt.chatgpt_generator`` の既定値
DEFAULT_ANSWER = {"answer_model": "deepseek-v3", "trials": 5, "temperature": 0.0, "max_tokens": 1024,
                  "require_behavior_match": True, "ier_cases": "base"}


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load_lm_cc_create_prompt():
    """lm-cc の ``create_prompt`` を読み込む (lm-cc 側の変更がそのまま反映されるようにコピーしない)。"""
    path = paths.LM_CC_ROOT / "scripts" / "tasks" / "ier" / "create_prompt_ier.py"
    if not path.exists():
        raise FileNotFoundError(f"lm-cc の create_prompt_ier.py が見つからない: {path} (LM_CC_ROOT を確認)")
    module_spec = importlib.util.spec_from_file_location("lm_cc_create_prompt_ier", path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.create_prompt


# ----------------------------------------------------------------------
# prepare
# ----------------------------------------------------------------------
def prepare(spec: ds.DatasetSpec, items: List[Dict[str, Any]], cfg: Dict[str, Any], out_dir: Path) -> pd.DataFrame:
    """評価の入力を作る。

    Args:
        items: ``{"item_id", "uid", "variant_id", "code", "behavior": 動作確認結果 or None,
            "original_behavior": 元コードの観測結果}`` (variant_id == "original" が元コード)
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    if spec.task == ds.TASK_IER:
        create_prompt = load_lm_cc_create_prompt()
        prompts = []
        for item in items:
            dirs = ds.humaneval_case_dirs(spec, item["uid"])
            if cfg.get("ier_cases", "base") == "base":
                dirs = dirs[:1]  # 先行研究の pass@1 は接尾辞なしのケース
            behavior_cases = {c["case_id"]: c for c in (item.get("behavior") or {}).get("cases", [])}
            ob = item.get("original_behavior") or {}
            original_obs = dict(zip(ob.get("case_ids", []), ob.get("observations", [])))
            if not dirs:
                rows.append({**_item_cols(item), "case_id": None, "usable": False, "skip_reason": "lm-cc の問題データが無い"})
                continue
            for d in dirs:
                case_id = f"input:{d.name}"
                code = item["code"].strip("\n")
                code_input = d.joinpath("input.txt").read_text(encoding="utf-8").strip("\n")
                expected = d.joinpath("output.txt").read_text(encoding="utf-8")
                # lm-cc は dataset 名に "humaneval" を渡す (simplified でも同じテンプレート)
                prompt = create_prompt(cfg.get("answer_model", "deepseek-v3"), code, code_input, "humaneval", "Python")
                usable, reason = True, None
                orig_ob = original_obs.get(case_id)
                if prompt.count(code) != 1:
                    usable, reason = False, "プロンプト内に計測対象のコードがちょうど1回含まれていない"
                elif orig_ob is None:
                    usable, reason = False, "元コードの動作確認が未実行 (output.txt を正解に使えるか未確認)"
                elif not orig_ob.get("matches_expected"):
                    # data/ の計測用ソースは lm-cc の接尾辞なしケースの main.py と書き方が違うことがある
                    usable, reason = False, "元コード (計測用ソース) の返り値が output.txt と一致しない"
                elif item["variant_id"] != "original":
                    bc = behavior_cases.get(case_id)
                    if item.get("original_code") and item["original_code"].strip("\n") in prompt:
                        usable, reason = False, "プロンプトに元コードが残っている"
                    elif bc is None:
                        usable, reason = False, "このケースの動作確認結果が無い (正解を流用できるか未確認)"
                    elif not bc["equal"]:
                        usable, reason = False, "このケースで変換前後の返り値が一致しない (正解を流用できない)"
                row = {**_item_cols(item), "case_id": case_id, "usable": usable, "skip_reason": reason,
                       "code_sha": _sha(code), "prompt_sha": _sha(prompt)}
                rows.append(row)
                prompts.append({**row, "prompt": prompt, "expected": expected})
        _write_jsonl(out_dir / "prompts.jsonl", prompts)
    else:
        records = []
        for item in items:
            record = ds.xcodeeval_record(spec, item["uid"])
            usable, reason = True, None
            if record is None:
                usable, reason = False, "lm-cc の問題レコードが無い"
            elif (item["variant_id"] != "original" and cfg.get("require_behavior_match", True)
                  and (item.get("behavior") or {}).get("status") != STATUS_MATCH):
                usable, reason = False, "動作確認で一致を確認できていない"
            row = {**_item_cols(item), "case_id": "hidden_tests", "usable": usable, "skip_reason": reason,
                   "code_sha": _sha(item["code"])}
            rows.append(row)
            if usable:
                new = dict(record)
                new[spec.code_field] = item["code"]
                new[spec.uid_field] = item["item_id"]  # lm-cc の出力は uid で区別されるので item_id にする
                new["equivalence_original_uid"] = item["uid"]
                new["equivalence_variant_id"] = item["variant_id"]
                records.append(new)
        _write_jsonl(out_dir / "lmcc_input.jsonl", records)
    table = pd.DataFrame(rows)
    table.to_csv(out_dir / "items.csv", index=False)
    return table


def _item_cols(item: Dict[str, Any]) -> Dict[str, Any]:
    return {"item_id": item["item_id"], "uid": item["uid"], "variant_id": item["variant_id"],
            "behavior_status": (item.get("behavior") or {}).get("status")}


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# ----------------------------------------------------------------------
# run (IER のみ。xcodeeval は lm-cc のスクリプトで実行する)
# ----------------------------------------------------------------------
def _call_api(prompt: str, cfg: Dict[str, Any]) -> str:
    """lm-cc ``prompt.chatgpt_generator`` と同じ呼び出し (system ロール 1 メッセージ)。"""
    from openai import OpenAI  # 回答精度を評価するときだけ必要

    model = cfg.get("answer_model", "deepseek-v3")
    if "deepseek-v3" in model:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                        base_url=os.getenv("OPENAI_BASE_URL", "https://qianfan.baidubce.com/v2"))
        model = os.getenv("OPENAI_MODEL_NAME", "deepseek-v3")
    else:
        client = OpenAI()
    completion = client.chat.completions.create(
        model=model, max_tokens=cfg.get("max_tokens", 1024), temperature=cfg.get("temperature", 0.0),
        messages=[{"role": "system", "content": prompt}], frequency_penalty=0, presence_penalty=0,
    )
    return completion.choices[0].message.content


def response_path(out_dir: Path, item_id: str, case_id: str, trial: int) -> Path:
    safe_case = case_id.replace(":", "_")
    return out_dir / "responses" / f"{item_id}__{safe_case}__t{trial}.json"


def run_ier(out_dir: Path, cfg: Dict[str, Any], only_failed: bool = False, limit: Optional[int] = None,
            caller=None) -> Dict[str, int]:
    """回答を取得して1試行1ファイルで保存する。成功済みの試行は再実行しない。"""
    caller = caller or _call_api
    counts = {"done": 0, "skipped": 0, "failed": 0}
    prompts = [p for p in _read_jsonl(out_dir / "prompts.jsonl") if p["usable"]]
    n_calls = 0
    for p in prompts:
        for trial in range(1, int(cfg.get("trials", 5)) + 1):
            path = response_path(out_dir, p["item_id"], p["case_id"], trial)
            if path.exists():
                prev = json.loads(path.read_text(encoding="utf-8"))
                if prev.get("error") is None and prev.get("prompt_sha") == p["prompt_sha"]:
                    counts["skipped"] += 1
                    continue
            elif only_failed:
                continue
            if limit is not None and n_calls >= limit:
                return counts
            n_calls += 1
            record = {"item_id": p["item_id"], "uid": p["uid"], "variant_id": p["variant_id"], "case_id": p["case_id"],
                      "trial": trial, "prompt_sha": p["prompt_sha"],
                      "answer_model": cfg.get("answer_model"), "api_model": os.getenv("OPENAI_MODEL_NAME"),
                      "temperature": cfg.get("temperature"), "max_tokens": cfg.get("max_tokens"),
                      "requested_at": datetime.now(timezone.utc).isoformat()}
            try:
                record["response"] = caller(p["prompt"], cfg)
                record["error"] = None
                counts["done"] += 1
            except Exception as exc:  # noqa: BLE001 - 失敗も記録して後で再実行する
                record["response"] = None
                record["error"] = f"{type(exc).__name__}: {exc}"
                counts["failed"] += 1
                time.sleep(float(cfg.get("retry_wait_sec", 0)))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    return counts


def score_ier(out_dir: Path, cfg: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """保存済みの回答を lm-cc と同じ方法で採点する。"""
    answers = []
    trials = int(cfg.get("trials", 5))
    for p in _read_jsonl(out_dir / "prompts.jsonl"):
        if not p["usable"]:
            continue
        for trial in range(1, trials + 1):
            path = response_path(out_dir, p["item_id"], p["case_id"], trial)
            row = {"item_id": p["item_id"], "uid": p["uid"], "variant_id": p["variant_id"], "case_id": p["case_id"],
                   "trial": trial, "expected": p["expected"]}
            if not path.exists():
                row.update(status="not_run")
            else:
                rec = json.loads(path.read_text(encoding="utf-8"))
                if rec.get("error") is not None or rec.get("prompt_sha") != p["prompt_sha"]:
                    row.update(status="error", error=rec.get("error") or "prompt が変わっている")
                else:
                    pred = extract_ier_prediction(rec["response"])
                    row.update(status="scored", prediction=pred, correct=ier_is_correct(pred, p["expected"]))
            answers.append(row)
    return _aggregate(pd.DataFrame(answers), out_dir)


def import_xcodeeval(out_dir: Path, details_path: Path) -> Dict[str, pd.DataFrame]:
    """lm-cc ``evaluate_apr.py`` / ``evaluate_ct.py`` の details jsonl を読み戻す。"""
    items = pd.read_csv(out_dir / "items.csv")
    by_id = {r["item_id"]: r for _, r in items.iterrows()}
    answers = []
    for d in _read_jsonl(details_path):
        item = by_id.get(d["task_id"])
        if item is None:
            continue
        for trial, res in enumerate(d.get("test_results", []), 1):
            answers.append({"item_id": item["item_id"], "uid": item["uid"], "variant_id": item["variant_id"],
                            "case_id": "hidden_tests", "trial": trial, "status": "scored",
                            "correct": bool(res["is_passed"]), "pass_rate": res.get("pass_rate")})
    return _aggregate(pd.DataFrame(answers), out_dir)


def _aggregate(answers: pd.DataFrame, out_dir: Path) -> Dict[str, pd.DataFrame]:
    answers.to_csv(out_dir / "answers.csv", index=False)
    if answers.empty:
        return {"answers": answers}
    scored = answers[answers["status"] == "scored"]
    acc = answers.groupby(["item_id", "uid", "variant_id", "case_id"], as_index=False).agg(
        n_trials_planned=("trial", "count"),
        n_scored=("status", lambda s: int((s == "scored").sum())),
    )
    corr = scored.groupby(["item_id", "case_id"])["correct"].sum().astype(int).to_dict()
    acc["n_correct"] = [int(corr.get((i, c), 0)) for i, c in zip(acc["item_id"], acc["case_id"])]
    acc["complete"] = acc["n_scored"] == acc["n_trials_planned"]
    acc["pass_at_1"] = [pass_at_1(c, n) if ok else None for c, n, ok in
                        zip(acc["n_correct"], acc["n_scored"], acc["complete"])]
    acc.to_csv(out_dir / "accuracy.csv", index=False)

    orig = acc[acc["variant_id"] == "original"].set_index(["uid", "case_id"])["pass_at_1"]
    comp = acc[acc["variant_id"] != "original"].copy()
    comp["pass_at_1_original"] = [orig.get((u, c)) for u, c in zip(comp["uid"], comp["case_id"])]
    comp["pass_at_1_delta"] = [None if (a is None or b is None or pd.isna(a) or pd.isna(b)) else a - b
                               for a, b in zip(comp["pass_at_1"], comp["pass_at_1_original"])]
    comp.to_csv(out_dir / "comparison.csv", index=False)
    return {"answers": answers, "accuracy": acc, "comparison": comp}
