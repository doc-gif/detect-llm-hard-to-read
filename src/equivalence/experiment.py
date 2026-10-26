"""等価変換実験の各段階 (transform → behavior → measure → compare、accuracy-*)。

各段階は対象ごとに状態を ``status/<stage>.json`` に記録し、成功済みの対象は再実行しない。
失敗した対象だけを再実行するには同じコマンドをもう一度実行する (``--only-failed`` で
未実行の対象を除き、失敗分だけに絞れる)。

出力 (``<output_root>/<experiment.name>/``):
    codes/<uid>/original.py, <variant>.py   元コードと変換後コード
    transforms/<uid>.json, transforms.csv   全候補 (適用できない・失敗も理由付き)
    behavior/<uid>/*.json, behavior.csv     動作確認の観測結果と判定
    measure/<uid>/<original|variant>.parquet  Phase 1 と同じ形式のトークン表
    compare/<uid>/<variant>/...            トークン・行・SU・region の比較とレポート
    compare/summary.csv, compare/regions.csv  全体の一覧
    accuracy/...                            回答精度評価の入力と結果
"""
from __future__ import annotations

import copy
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pandas as pd

import paths
from equivalence import accuracy, behavior, compare, datasets as ds, report
from equivalence.runstate import RunState, now
from equivalence.transforms import STATUS_OK, create_transformation
from utils.io import read_text

logger = logging.getLogger("equivalence")

ORIGINAL = "original"

DEFAULT_CONFIG: Dict[str, Any] = {
    # name の {transform} / {dataset} は変換名・データセット名に置き換える
    "experiment": {"name": "{transform}_{dataset}", "dataset": None, "ids": "all", "targets": [], "output_root": "results/equivalence"},
    "transform": {"name": "if_else_swap", "options": {}},
    "behavior": {"timeout_sec": 10.0, "workers": 4},
    "measure": {
        "model": "codellama/CodeLlama-7b-hf", "model_kind": "hf_causal_lm", "revision": "",
        "device": "mps", "dtype": "float16", "context_strategy": "function_scope",
        # この判定の変換後コードだけを計測する
        "allowed_behavior": ["match"],
        # 同じ条件で同じコードを計測した結果を再利用する (cache_dir は output_root からの相対パス)
        "cache": True, "cache_dir": "_cache/measure",
    },
    # 既存の分析と同じ固定閾値 [nats]。変換結果を見て変えない
    "thresholds": {"p67": 0.6813, "p80": 1.2515},
    "accuracy": dict(accuracy.DEFAULT_ANSWER),
}


def _merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(base)
    for k, v in override.items():
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) and k != "thresholds" else v
    return out


def load_config(path: Optional[Path] = None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """TOML 設定 (省略時は ``DEFAULT_CONFIG``) に上書きを重ね、``experiment.name`` を展開する。"""
    return build_configs(path, overrides=overrides)[0]


def build_configs(path: Optional[Path], datasets: Optional[List[str]] = None, transforms: Optional[List[str]] = None,
                  name: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """データセット × 変換の組ごとに設定を作る (CLI の ``--dataset`` / ``--transform``)。

    - ``datasets`` / ``transforms`` が None なら設定ファイルの値。``["all"]`` は登録済みの全部
    - データセットを差し替えたときは ids を "all"、targets を空に戻す (ID は別データセットのものなので)。
      ``overrides`` に ids / targets があればそちらを使う
    - 変換を差し替えたときは transform.options を空に戻す (別の変換のオプションなので)
    - 名前は ``name`` > 設定ファイルの name。差し替えたのに名前に {dataset} / {transform} が無ければ
      既定の "{transform}_{dataset}" を使う (別条件の結果が同じディレクトリに入らないように)
    """
    import tomllib
    from equivalence.transforms import available_transformations

    file_cfg: Dict[str, Any] = {}
    if path is not None:
        with open(path, "rb") as f:
            file_cfg = tomllib.load(f)
    base = _merge(DEFAULT_CONFIG, file_cfg)
    if datasets == ["all"]:
        datasets = list(ds.DATASETS)
    if transforms == ["all"]:
        transforms = available_transformations()
    changed = ((["{dataset}"] if any(d != base["experiment"]["dataset"] for d in datasets or []) else [])
               + (["{transform}"] if any(t != base["transform"]["name"] for t in transforms or []) else []))
    name_template = name or base["experiment"]["name"]
    if not name and any(p not in name_template for p in changed):
        name_template = DEFAULT_CONFIG["experiment"]["name"]

    configs = []
    for dataset in datasets or [base["experiment"]["dataset"]]:
        for transform in transforms or [base["transform"]["name"]]:
            o: Dict[str, Any] = {"experiment": {"name": name_template}}
            if datasets and dataset != base["experiment"]["dataset"]:
                o["experiment"].update({"dataset": dataset, "ids": "all", "targets": []})
            if transforms and transform != base["transform"]["name"]:
                o["transform"] = {"name": transform, "options": {}}
            config = _merge(base, o)
            if overrides:
                config = _merge(config, overrides)
            exp = config["experiment"]
            if not exp.get("name") or not exp.get("dataset"):
                raise ValueError("experiment.name と experiment.dataset は必須 (dataset は --dataset でも指定できる)")
            ds.get_dataset(exp["dataset"])
            exp["name"] = exp["name"].format(transform=config["transform"]["name"], dataset=exp["dataset"])
            configs.append(config)
    names = [c["experiment"]["name"] for c in configs]
    if len(set(names)) != len(names):
        raise ValueError(f"実験名が重複する: {names} (名前に {{dataset}} / {{transform}} を入れる)")
    return configs


def target_ids(config: Dict[str, Any]) -> List[str]:
    """設定の対象 ID (ids → targets の uid を追加 → limit で先頭 N 件)。"""
    exp = config["experiment"]
    ids = ds.list_ids(ds.get_dataset(exp["dataset"])) if exp.get("ids") in (None, "all") else list(exp["ids"])
    ids += [t.split(":")[0] for t in exp.get("targets") or [] if t.split(":")[0] not in ids]
    if exp.get("limit"):
        ids = ids[: int(exp["limit"])]
    return ids


class Experiment:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        exp = config["experiment"]
        self.spec = ds.get_dataset(exp["dataset"])
        self.output_root = Path(exp["output_root"])
        if not self.output_root.is_absolute():
            self.output_root = paths.PROJECT_ROOT / self.output_root
        self.run_dir = self.output_root / exp["name"]
        self.state = RunState(self.run_dir, config)
        self.transformation = create_transformation(config["transform"]["name"], **config["transform"]["options"])
        self.thresholds: Dict[str, float] = {k: float(v) for k, v in config["thresholds"].items()}

    def _resolve(self, path_str: str) -> Path:
        """``output_root`` からの相対パスを解決する (絶対パスはそのまま)。"""
        path = Path(path_str)
        return path if path.is_absolute() else self.output_root / path

    # ------------------------------------------------------------------
    # 対象
    # ------------------------------------------------------------------
    def target_ids(self) -> List[str]:
        return target_ids(self.config)

    def _selected_variants(self) -> Dict[str, Optional[set]]:
        """uid -> 対象の variant_id 集合 (None は全候補)。"""
        selected: Dict[str, Optional[set]] = {}
        for t in self.config["experiment"].get("targets") or []:
            uid, _, variant = t.partition(":")
            if variant:
                if selected.get(uid, set()) is not None:
                    selected.setdefault(uid, set()).add(variant)
            else:
                selected[uid] = None
        return selected

    def code_path(self, uid: str, variant_id: str) -> Path:
        return self.run_dir / "codes" / uid / f"{variant_id}.py"

    def transform_record(self, uid: str) -> Optional[Dict[str, Any]]:
        path = self.run_dir / "transforms" / f"{uid}.json"
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

    def variants(self, uid: str) -> List[Dict[str, Any]]:
        """変換に成功し、対象に選ばれている候補。"""
        rec = self.transform_record(uid)
        if rec is None:
            return []
        selected = self._selected_variants()
        wanted = selected.get(uid) if uid in selected else None
        return [c for c in rec["candidates"]
                if c["status"] == STATUS_OK and (wanted is None or c["variant_id"] in wanted)]

    @staticmethod
    def item_id(uid: str, variant_id: str) -> str:
        return uid if variant_id == ORIGINAL else f"{uid}__{variant_id}"

    def _ids_for(self, stage: str, ids: Iterable[str], only_failed: bool) -> Iterable[str]:
        for key in ids:
            st = self.state.status(stage).get(key, {}).get("status")
            if st == "ok":
                continue
            if only_failed and st is None:
                continue
            yield key

    def _log(self, stage: str, started: str, counts: Dict[str, int]) -> None:
        self.state.log_run({"stage": stage, "started_at": started, "finished_at": now(), "counts": counts,
                            "experiment": self.config["experiment"]["name"]})
        logger.info("[%s] %s", stage, counts)

    # ------------------------------------------------------------------
    # 1. transform
    # ------------------------------------------------------------------
    def run_transform(self, only_failed: bool = False) -> Dict[str, int]:
        started, counts = now(), {"files": 0, "candidates_ok": 0, "not_applicable": 0, "failed": 0, "errors": 0}
        for uid in self._ids_for("transform", self.target_ids(), only_failed):
            try:
                src_path = ds.source_path(self.spec, uid)
                source = read_text(src_path)
                orig_path = self.code_path(uid, ORIGINAL)
                orig_path.parent.mkdir(parents=True, exist_ok=True)
                orig_path.write_bytes(source.encode("utf-8"))
                task_code = ds.task_code(self.spec, uid)
                outcomes = []
                for cand in self.transformation.find_candidates(source):
                    out = self.transformation.apply(source, cand)
                    rec = out.to_record()
                    rec["status"] = out.status
                    rec["variant_id"] = cand.variant_id
                    if out.status == STATUS_OK:
                        self.code_path(uid, cand.variant_id).write_bytes(out.transformed_source.encode("utf-8"))
                        counts["candidates_ok"] += 1
                    else:
                        counts["not_applicable" if out.status == "not_applicable" else "failed"] += 1
                    outcomes.append(rec)
                record = {
                    "uid": uid, "dataset": self.spec.name, "source_path": str(src_path.relative_to(paths.PROJECT_ROOT)),
                    "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
                    "transform": self.transformation.describe(),
                    # lm-cc がプロンプトに入れるコードと計測用ソースが同じか (改行の前後差は無視)
                    "task_code_matches_source": None if task_code is None
                    else task_code.replace("\r\n", "\n").strip("\n") == source.strip("\n"),
                    "lm_cc_cases_with_same_code": ds.cases_with_same_code(self.spec, uid, source),
                    "candidates": outcomes,
                }
                path = self.run_dir / "transforms" / f"{uid}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
                n_ok = sum(c["status"] == STATUS_OK for c in outcomes)
                self.state.set("transform", uid, "ok", n_candidates=len(outcomes), n_ok=n_ok)
                counts["files"] += 1
            except Exception as exc:  # noqa: BLE001
                logger.exception("transform failed: %s", uid)
                self.state.set("transform", uid, "failed", reason=f"{type(exc).__name__}: {exc}")
                counts["errors"] += 1
        self._write_transform_table()
        self._log("transform", started, counts)
        return counts

    def _write_transform_table(self) -> None:
        rows = []
        for uid in self.target_ids():
            rec = self.transform_record(uid)
            if rec is None:
                continue
            for c in rec["candidates"]:
                cand, edits = c["candidate"], {e["kind"]: e for e in c["edits"]}
                neg = edits.get("negate_condition", {})
                rows.append({
                    "uid": uid, "variant_id": c["variant_id"], "item_id": self.item_id(uid, c["variant_id"]),
                    "status": c["status"], "reason": c["reason"],
                    "start_line": cand["start_line"], "end_line": cand["end_line"],
                    "condition_before": neg.get("before"), "condition_after": neg.get("after"),
                    "negation_method": neg.get("method"),
                    "line_count_equal": c["checks"].get("line_count_equal"),
                    "ast_matches_expected": c["checks"].get("ast_matches_expected"),
                    "task_code_matches_source": rec.get("task_code_matches_source"),
                    "lm_cc_cases_with_same_code": ";".join(rec.get("lm_cc_cases_with_same_code") or []),
                })
        pd.DataFrame(rows).to_csv(self.run_dir / "transforms.csv", index=False)

    # ------------------------------------------------------------------
    # 2. behavior
    # ------------------------------------------------------------------
    def behavior_path(self, uid: str, variant_id: str) -> Path:
        return self.run_dir / "behavior" / uid / f"{variant_id}.json"

    def behavior_result(self, uid: str, variant_id: str) -> Optional[Dict[str, Any]]:
        path = self.behavior_path(uid, variant_id)
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

    def run_behavior(self, only_failed: bool = False) -> Dict[str, int]:
        started, counts = now(), {}
        timeout = float(self.config["behavior"]["timeout_sec"])
        workers = int(self.config["behavior"].get("workers", 1))
        for uid in self.target_ids():
            keys = {self.item_id(uid, v["variant_id"]): v for v in self.variants(uid)}
            todo = list(self._ids_for("behavior", keys, only_failed))
            if not todo:
                continue
            try:
                built = behavior.build_cases(self.spec, uid)
                cases = built["cases"]
                orig_path = self.behavior_path(uid, ORIGINAL)
                if orig_path.exists():
                    orig_obs = json.loads(orig_path.read_text(encoding="utf-8"))["observations"]
                else:
                    orig_obs = behavior.observe_all(read_text(self.code_path(uid, ORIGINAL)), cases, timeout, workers)
                    orig_path.parent.mkdir(parents=True, exist_ok=True)
                    orig_path.write_text(json.dumps({"uid": uid, "case_ids": [c["case_id"] for c in cases],
                                                     "observations": orig_obs}, ensure_ascii=False, indent=1),
                                         encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                logger.exception("behavior failed: %s", uid)
                for key in todo:
                    self.state.set("behavior", key, "failed", reason=f"{type(exc).__name__}: {exc}")
                counts["errors"] = counts.get("errors", 0) + len(todo)
                continue
            for key in todo:
                variant = keys[key]
                try:
                    obs = behavior.observe_all(read_text(self.code_path(uid, variant["variant_id"])), cases, timeout, workers,
                                               skip=[bool(o.get("timeout")) for o in orig_obs])
                    result = behavior.compare(cases, orig_obs, obs, built["notes"])
                    result.update(uid=uid, variant_id=variant["variant_id"], checked_at=now(), timeout_sec=timeout)
                    self.behavior_path(uid, variant["variant_id"]).write_text(
                        json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
                    self.state.set("behavior", key, "ok", result=result["status"], reason=result["reason"])
                    counts[result["status"]] = counts.get(result["status"], 0) + 1
                except Exception as exc:  # noqa: BLE001
                    logger.exception("behavior failed: %s", key)
                    self.state.set("behavior", key, "failed", reason=f"{type(exc).__name__}: {exc}")
                    counts["errors"] = counts.get("errors", 0) + 1
        self._write_behavior_table()
        self._log("behavior", started, counts)
        return counts

    def _write_behavior_table(self) -> None:
        rows = []
        for uid in self.target_ids():
            for v in self.variants(uid):
                res = self.behavior_result(uid, v["variant_id"])
                row = {"uid": uid, "variant_id": v["variant_id"], "item_id": self.item_id(uid, v["variant_id"]),
                       "line_count_equal": v["checks"].get("line_count_equal")}
                if res is None:
                    row.update(status=behavior.STATUS_NOT_RUN)
                else:
                    exp_flags = [c["original"].get("matches_expected") for c in res["cases"]
                                 if c["original"].get("matches_expected") is not None]
                    row.update(status=res["status"], reason=res["reason"], n_cases=res["n_cases"],
                               n_equal=res["n_equal"], n_timeout=res["n_timeout"],
                               original_matches_expected=f"{sum(exp_flags)}/{len(exp_flags)}" if exp_flags else None)
                rows.append(row)
        pd.DataFrame(rows).to_csv(self.run_dir / "behavior.csv", index=False)

    # ------------------------------------------------------------------
    # 3. measure
    # ------------------------------------------------------------------
    def measure_path(self, uid: str, variant_id: str) -> Path:
        return self.run_dir / "measure" / uid / f"{variant_id}.parquet"

    def measure_items(self) -> List[Tuple[str, str, Optional[str]]]:
        """``(uid, variant_id, 計測しない理由)`` の一覧。"""
        allowed = set(self.config["measure"].get("allowed_behavior") or [])
        items = []
        for uid in self.target_ids():
            variants = self.variants(uid)
            if not variants:
                continue
            items.append((uid, ORIGINAL, None))
            for v in variants:
                res = self.behavior_result(uid, v["variant_id"])
                status = behavior.STATUS_NOT_RUN if res is None else res["status"]
                reason = None if (not allowed or status in allowed) else f"動作確認の判定が {status}"
                items.append((uid, v["variant_id"], reason))
        return items

    def run_measure(self, only_failed: bool = False, model=None) -> Dict[str, int]:
        from equivalence import measure

        started, counts = now(), {"measured": 0, "cached": 0, "skipped": 0, "errors": 0}
        mcfg = self.config["measure"]
        todo = []
        for uid, variant_id, reason in self.measure_items():
            key = self.item_id(uid, variant_id)
            if self.state.is_ok("measure", key):
                continue
            if reason is not None:
                self.state.set("measure", key, "skipped", reason=reason)
                counts["skipped"] += 1
                continue
            if only_failed and self.state.status("measure").get(key, {}).get("status") != "failed":
                continue
            todo.append((uid, variant_id, key))
        cache = measure.MeasureCache(self._resolve(mcfg.get("cache_dir") or "_cache/measure")) \
            if mcfg.get("cache", True) else None
        for uid, variant_id, key in todo:
            t0 = time.time()
            src, out = self.code_path(uid, variant_id), self.measure_path(uid, variant_id)
            out.parent.mkdir(parents=True, exist_ok=True)
            ckey, parts = measure.cache_key(src.read_bytes(), mcfg)
            n = cache.get(ckey, out, src, project=key) if cache is not None else None
            hit = n is not None
            if not hit:
                if model is None:  # 全部キャッシュにあればモデルを読み込まない (読み込みの失敗は全体を止める)
                    model = measure.load_model(mcfg)
                try:
                    n = measure.measure_file(model, src, out, mcfg, project=key)
                except Exception as exc:  # noqa: BLE001
                    logger.exception("measure failed: %s", key)
                    self.state.set("measure", key, "failed", reason=f"{type(exc).__name__}: {exc}")
                    counts["errors"] += 1
                    continue
                if cache is not None:
                    cache.put(ckey, parts, out, n)
            self.state.set("measure", key, "ok", tokens=n, seconds=round(time.time() - t0, 2),
                           model=mcfg["model"], model_kind=mcfg["model_kind"], device=mcfg.get("device"),
                           dtype=mcfg.get("dtype"), cache_hit=hit, cache_key=ckey)
            counts["cached" if hit else "measured"] += 1
        self._log("measure", started, counts)
        return counts

    # ------------------------------------------------------------------
    # 4. compare
    # ------------------------------------------------------------------
    def compare_dir(self, uid: str, variant_id: str) -> Path:
        return self.run_dir / "compare" / uid / variant_id

    def run_compare(self, only_failed: bool = False) -> Dict[str, int]:
        started, counts = now(), {"compared": 0, "waiting": 0, "errors": 0}
        labels = list(self.thresholds)
        for uid in self.target_ids():
            for v in self.variants(uid):
                key = self.item_id(uid, v["variant_id"])
                st = self.state.status("compare").get(key, {}).get("status")
                if st == "ok" or (only_failed and st != "failed"):
                    continue
                if not (self.state.is_ok("measure", self.item_id(uid, ORIGINAL)) and self.state.is_ok("measure", key)):
                    counts["waiting"] += 1  # 計測が済んでいない
                    continue
                try:
                    out_dir = self.compare_dir(uid, v["variant_id"])
                    out_dir.mkdir(parents=True, exist_ok=True)
                    result = compare.compare_pair(
                        pd.read_parquet(self.measure_path(uid, ORIGINAL)),
                        pd.read_parquet(self.measure_path(uid, v["variant_id"])),
                        read_text(self.code_path(uid, ORIGINAL)), read_text(self.code_path(uid, v["variant_id"])),
                        v["line_map"], self.thresholds)
                    self._write_compare(uid, v, result, out_dir, labels)
                    self.state.set("compare", key, "ok")
                    counts["compared"] += 1
                except Exception as exc:  # noqa: BLE001
                    logger.exception("compare failed: %s", key)
                    self.state.set("compare", key, "failed", reason=f"{type(exc).__name__}: {exc}")
                    counts["errors"] += 1
        self._write_compare_tables()
        self._log("compare", started, counts)
        return counts

    def _write_compare(self, uid: str, v: Dict[str, Any], result: Dict[str, Any], out_dir: Path,
                       labels: List[str]) -> None:
        for name in ("tokens_before", "tokens_after", "lines", "token_alignment", "regions"):
            result[name].to_csv(out_dir / f"{name}.csv", index=False)
        beh = self.behavior_result(uid, v["variant_id"])
        neg = {e["kind"]: e for e in v["edits"]}.get("negate_condition", {})
        summary = {"uid": uid, "variant_id": v["variant_id"], "item_id": self.item_id(uid, v["variant_id"]),
                   "dataset": self.spec.name, "transform": self.transformation.name,
                   "if_line": v["candidate"]["start_line"], "condition_before": neg.get("before"),
                   "condition_after": neg.get("after"),
                   "behavior_status": beh["status"] if beh else behavior.STATUS_NOT_RUN,
                   "line_count_equal": v["checks"].get("line_count_equal"), **result["summary"]}
        (out_dir / "summary.json").write_text(json.dumps(
            {"summary": summary, "metrics_before": result["metrics_before"], "metrics_after": result["metrics_after"],
             "units": result["units"], "thresholds": self.thresholds}, ensure_ascii=False, indent=1, default=str),
            encoding="utf-8")
        meta = {"item": summary["item_id"], "transform": f"{self.transformation.name} (L{summary['if_line']}: "
                f"{neg.get('before')} → {neg.get('after')})", "behavior": summary["behavior_status"],
                "model": self.config["measure"]["model"], "thresholds": self.thresholds}
        title = f"{summary['item_id']} 変換前後の比較"
        (out_dir / "report.html").write_text(report.render_html(title, result, meta, labels), encoding="utf-8")
        (out_dir / "report.md").write_text(report.render_markdown(title, result, meta, labels), encoding="utf-8")

    def _write_compare_tables(self) -> None:
        summaries, regions = [], []
        for uid in self.target_ids():
            for v in self.variants(uid):
                d = self.compare_dir(uid, v["variant_id"])
                if not (d / "summary.json").exists():
                    continue
                summaries.append(json.loads((d / "summary.json").read_text(encoding="utf-8"))["summary"])
                reg = pd.read_csv(d / "regions.csv")
                reg.insert(0, "item_id", self.item_id(uid, v["variant_id"]))
                regions.append(reg)
        if summaries:
            pd.DataFrame(summaries).to_csv(self.run_dir / "compare" / "summary.csv", index=False)
            pd.concat(regions).to_csv(self.run_dir / "compare" / "regions.csv", index=False)

    # ------------------------------------------------------------------
    # 5. accuracy
    # ------------------------------------------------------------------
    def accuracy_dir(self) -> Path:
        return self.run_dir / "accuracy"

    def accuracy_items(self) -> List[Dict[str, Any]]:
        items = []
        for uid in self.target_ids():
            variants = self.variants(uid)
            if not variants:
                continue
            original = read_text(self.code_path(uid, ORIGINAL))
            orig_beh = self.behavior_result(uid, ORIGINAL)
            items.append({"item_id": uid, "uid": uid, "variant_id": ORIGINAL, "code": original, "behavior": None,
                          "original_behavior": orig_beh})
            for v in variants:
                items.append({"item_id": self.item_id(uid, v["variant_id"]), "uid": uid, "variant_id": v["variant_id"],
                              "code": read_text(self.code_path(uid, v["variant_id"])), "original_code": original,
                              "behavior": self.behavior_result(uid, v["variant_id"]), "original_behavior": orig_beh})
        return items

    def run_accuracy_prepare(self) -> pd.DataFrame:
        started = now()
        table = accuracy.prepare(self.spec, self.accuracy_items(), self.config["accuracy"], self.accuracy_dir())
        self._log("accuracy-prepare", started, {"rows": len(table), "usable": int(table["usable"].sum()) if len(table) else 0})
        return table

    def run_accuracy(self, only_failed: bool = False, limit: Optional[int] = None) -> Dict[str, int]:
        if self.spec.task != ds.TASK_IER:
            raise ValueError("xcodeeval は lm-cc の generate_*.py / evaluate_*.py で実行する (docs 参照)")
        started = now()
        counts = accuracy.run_ier(self.accuracy_dir(), self.config["accuracy"], only_failed=only_failed, limit=limit)
        self._log("accuracy-run", started, counts)
        return counts

    def run_accuracy_score(self, details: Optional[Path] = None) -> Dict[str, pd.DataFrame]:
        started = now()
        if self.spec.task == ds.TASK_IER:
            out = accuracy.score_ier(self.accuracy_dir(), self.config["accuracy"])
        else:
            if details is None:
                raise ValueError("xcodeeval では --details に lm-cc の *_details.jsonl を指定する")
            out = accuracy.import_xcodeeval(self.accuracy_dir(), details)
        self._log("accuracy-score", started, {k: len(v) for k, v in out.items()})
        return out

    # ------------------------------------------------------------------
    def status_counts(self) -> Dict[str, Dict[str, int]]:
        out = {}
        for stage in ("transform", "behavior", "measure", "compare"):
            c: Dict[str, int] = {}
            for v in self.state.status(stage).values():
                c[v["status"]] = c.get(v["status"], 0) + 1
            out[stage] = c
        return out
