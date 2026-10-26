"""変換前後のエントロピー・SU の比較。

ファイル単位の指標は Phase 2 (``analysis/pipeline.py``) と同じ関数で算出する:
  - 前処理: surprisal が null の行を除く (``pipeline.process_file`` と同じ)
  - LOC: ``analysis.macro.loc`` / PPL: ``analysis.macro.perplexity`` / トークン数: 行数
  - SU 数・LM-CC: ``analysis.macro.lm_cc`` (内部の ``get_code_with_boundaries``)
  - 平均トークンエントロピー: ``metric_entropy`` の平均

SU の位置・範囲は ``get_code_with_boundaries`` と同じ行分割 (改行トークンで区切った行) を使い、
「先頭以外のトークンでエントロピー ≥ 閾値のものを含む行の前に境界」を復元する。
復元した境界数 + 1 が既存関数の SU 数と一致することを毎回確認する。

変換前後の対応付けはトークン番号ではなく、変換が記録した「行の対応」(line_map) を使う。
対応する行どうしでトークン列を difflib で突き合わせ、同じ文字列のトークンだけを対にする。
"""
from __future__ import annotations

import difflib
from typing import Any, Dict, List, Optional

import pandas as pd

from analysis.macro import lm_cc, loc, perplexity
from analysis.macro.lm_cc_helper.calculate_code_with_boundaries import get_code_with_boundaries
from schema.records import ParquetSchema as PCol

ENT = PCol.METRIC_ENTROPY


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Phase 2 と同じ前処理 (surprisal が null の行を除く)。"""
    if PCol.METRIC_SURPRISAL in df.columns:
        df = df[df[PCol.METRIC_SURPRISAL].notnull()]
    return df.reset_index(drop=True)


def display_text(token_str: str) -> str:
    return token_str.replace("<0x0A>", "\n").replace("▁", " ")


# ----------------------------------------------------------------------
# SU の位置・範囲
# ----------------------------------------------------------------------
def semantic_units(df_clean: pd.DataFrame, threshold: float) -> Dict[str, Any]:
    """SU の境界と範囲を返す。

    Returns:
        ``{"count", "segments", "units", "token_su", "token_trigger"}``
        - segments: 行 (改行トークンで区切ったトークン列) ごとの境界情報
        - units: SU ごとの開始・終了行とトークン範囲、境界を作ったトークン
        - token_su / token_trigger: トークン位置 (df_clean の行番号) ごとの SU 番号・閾値以上か
    """
    tokens = df_clean[PCol.TOKEN_STR].tolist()
    entropies = df_clean[ENT].tolist()
    lines = df_clean[PCol.LINE].tolist()
    _, _, start_end_tokens, count = get_code_with_boundaries(tokens=tokens, entropies=entropies, threshold=threshold)

    token_trigger = [i > 0 and entropies[i] >= threshold for i in range(len(tokens))]
    segments = []
    for k, (s, e) in enumerate(start_end_tokens):
        seg_lines = [lines[i] for i in range(s, e + 1) if pd.notna(lines[i])]
        triggers = [i for i in range(s, e + 1) if token_trigger[i]]
        segments.append({
            "segment": k, "start_token": s, "end_token": e,
            "line": int(seg_lines[0]) if seg_lines else None,
            "boundary": bool(triggers), "triggers": triggers,
        })
    n_boundaries = sum(seg["boundary"] for seg in segments)
    if n_boundaries + 1 != count:
        raise RuntimeError(f"SU 境界の復元が既存関数と一致しない: {n_boundaries} + 1 != {count}")

    units: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = {"su_index": 0, "segments": [], "triggers": []}
    for seg in segments:
        if seg["boundary"]:
            units.append(current)
            current = {"su_index": len(units), "segments": [], "triggers": seg["triggers"]}
        current["segments"].append(seg)
    units.append(current)

    token_su = [0] * len(tokens)
    unit_rows = []
    for unit in units:
        segs = unit["segments"]
        for seg in segs:
            for i in range(seg["start_token"], seg["end_token"] + 1):
                token_su[i] = unit["su_index"]
        seg_lines = [seg["line"] for seg in segs if seg["line"] is not None]
        unit_rows.append({
            "su_index": unit["su_index"],
            "start_line": min(seg_lines) if seg_lines else None,
            "end_line": max(seg_lines) if seg_lines else None,
            "start_token": segs[0]["start_token"] if segs else None,
            "end_token": segs[-1]["end_token"] if segs else None,
            "n_tokens": sum(seg["end_token"] - seg["start_token"] + 1 for seg in segs),
            # 境界を作ったトークン (= この SU の先頭行にある閾値以上のトークン)
            "trigger_tokens": [
                {"pos": i, "idx": int(df_clean[PCol.IDX].iloc[i]), "token_str": tokens[i],
                 "entropy": float(entropies[i]), "line": int(lines[i]) if pd.notna(lines[i]) else None}
                for i in unit["triggers"]
            ],
        })
    return {"count": count, "segments": segments, "units": unit_rows,
            "token_su": token_su, "token_trigger": token_trigger}


def file_metrics(df_clean: pd.DataFrame, thresholds: Dict[str, float]) -> Dict[str, Any]:
    """ファイル単位の指標 (Phase 2 と同じ関数) と、閾値ごとの SU 詳細。"""
    metrics: Dict[str, Any] = {
        "loc": loc.calculate(df_clean),
        "total_tokens": len(df_clean),
        "mean_entropy": float(df_clean[ENT].mean()) if len(df_clean) else None,
        "ppl": perplexity.calculate(df_clean),
    }
    details = {}
    for label, threshold in thresholds.items():
        lmcc_value, su_from_lmcc = lm_cc.calculate(df_clean, threshold=threshold)
        su = semantic_units(df_clean, threshold)
        if su_from_lmcc is not None and su_from_lmcc != su["count"]:
            raise RuntimeError(f"SU 数が lm_cc.calculate と一致しない ({label}): {su_from_lmcc} != {su['count']}")
        metrics[f"su_count_{label}"] = su["count"]
        metrics[f"lm_cc_{label}"] = lmcc_value
        details[label] = su
    return {"metrics": metrics, "su": details}


# ----------------------------------------------------------------------
# トークン表・行の対応
# ----------------------------------------------------------------------
def token_table(df_clean: pd.DataFrame, su: Dict[str, Dict[str, Any]], line_region: Dict[int, str],
                line_partner: Dict[int, int]) -> pd.DataFrame:
    """トークンごとの文字列・位置・エントロピー・SU。``partner_line`` は相手側の対応行。"""
    out = pd.DataFrame({
        "pos": range(len(df_clean)),
        "idx": df_clean[PCol.IDX].astype(int),
        "token_str": df_clean[PCol.TOKEN_STR],
        "text": df_clean[PCol.TOKEN_STR].map(display_text),
        "line": df_clean[PCol.LINE].astype("Int64"),
        "column": df_clean[PCol.COLUMN].astype("Int64"),
        "entropy": df_clean[ENT].astype(float),
        "surprisal": df_clean[PCol.METRIC_SURPRISAL].astype(float),
    })
    out["region"] = out["line"].map(lambda ln: line_region.get(int(ln)) if pd.notna(ln) else None)
    out["partner_line"] = out["line"].map(lambda ln: line_partner.get(int(ln)) if pd.notna(ln) else None)
    for label, detail in su.items():
        out[f"trigger_{label}"] = detail["token_trigger"]
        out[f"su_{label}"] = detail["token_su"]
    return out


def _line_stats(tokens: pd.DataFrame, labels: List[str]) -> Dict[int, Dict[str, Any]]:
    stats: Dict[int, Dict[str, Any]] = {}
    for line, group in tokens.groupby("line"):
        row = {
            "n_tokens": len(group),
            "mean_entropy": float(group["entropy"].mean()),
            "max_entropy": float(group["entropy"].max()),
            "sum_entropy": float(group["entropy"].sum()),
        }
        for label in labels:
            row[f"n_triggers_{label}"] = int(group[f"trigger_{label}"].sum())
            row[f"boundary_{label}"] = bool(group[f"trigger_{label}"].any())
            row[f"su_{label}"] = int(group[f"su_{label}"].iloc[0])
        stats[int(line)] = row
    return stats


def line_table(line_map: List[Dict[str, Any]], tokens_before: pd.DataFrame, tokens_after: pd.DataFrame,
               source_before: str, source_after: str, labels: List[str]) -> pd.DataFrame:
    """元コードの行順に、対応する変換後の行と行単位の指標を並べる。"""
    lines_b = source_before.split("\n")
    lines_a = source_after.split("\n")
    stats_b = _line_stats(tokens_before, labels)
    stats_a = _line_stats(tokens_after, labels)
    rows = []
    for m in line_map:
        ob, na = m["orig_line"], m["new_line"]
        row = {
            "orig_line": ob, "new_line": na, "region": m["region"], "text_changed": m["text_changed"],
            "text_before": lines_b[ob - 1] if ob - 1 < len(lines_b) else "",
            "text_after": lines_a[na - 1] if na - 1 < len(lines_a) else "",
        }
        sb, sa = stats_b.get(ob, {}), stats_a.get(na, {})
        for key in ("n_tokens", "mean_entropy", "max_entropy", "sum_entropy"):
            row[f"{key}_before"] = sb.get(key)
            row[f"{key}_after"] = sa.get(key)
            if sb.get(key) is not None and sa.get(key) is not None:
                row[f"{key}_delta"] = sa[key] - sb[key]
        for label in labels:
            bb, ba = sb.get(f"boundary_{label}", False), sa.get(f"boundary_{label}", False)
            row[f"n_triggers_{label}_before"] = sb.get(f"n_triggers_{label}", 0)
            row[f"n_triggers_{label}_after"] = sa.get(f"n_triggers_{label}", 0)
            row[f"boundary_{label}_before"] = bb
            row[f"boundary_{label}_after"] = ba
            row[f"boundary_{label}_change"] = "same" if bb == ba else ("added" if ba else "removed")
            row[f"su_{label}_before"] = sb.get(f"su_{label}")
            row[f"su_{label}_after"] = sa.get(f"su_{label}")
        rows.append(row)
    return pd.DataFrame(rows)


def token_alignment(line_map: List[Dict[str, Any]], tokens_before: pd.DataFrame, tokens_after: pd.DataFrame,
                    labels: List[str]) -> pd.DataFrame:
    """対応する行どうしでトークン列を突き合わせる。

    同じトークン番号どうしは対応づけない。行の対応 (変換が記録したもの) の中で
    difflib によりトークン文字列が一致した部分だけを対にし、残りは片側だけの行として出力する。
    """
    by_line_b = {int(k): g for k, g in tokens_before.groupby("line")}
    by_line_a = {int(k): g for k, g in tokens_after.groupby("line")}
    rows = []

    def side(prefix: str, tok: Optional[pd.Series]) -> Dict[str, Any]:
        out = {f"{prefix}_pos": None, f"{prefix}_idx": None, f"{prefix}_token": None, f"{prefix}_entropy": None}
        for label in labels:
            out[f"{prefix}_trigger_{label}"] = None
        if tok is not None:
            out.update({f"{prefix}_pos": int(tok["pos"]), f"{prefix}_idx": int(tok["idx"]),
                        f"{prefix}_token": tok["token_str"], f"{prefix}_entropy": float(tok["entropy"])})
            for label in labels:
                out[f"{prefix}_trigger_{label}"] = bool(tok[f"trigger_{label}"])
        return out

    for m in line_map:
        gb = by_line_b.get(m["orig_line"])
        ga = by_line_a.get(m["new_line"])
        tb = [] if gb is None else [r for _, r in gb.iterrows()]
        ta = [] if ga is None else [r for _, r in ga.iterrows()]
        matcher = difflib.SequenceMatcher(a=[t["token_str"] for t in tb], b=[t["token_str"] for t in ta], autojunk=False)
        method = "identical_tokens" if [t["token_str"] for t in tb] == [t["token_str"] for t in ta] else "diff_in_line"
        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            pairs = []
            if op == "equal":
                pairs = [(tb[i1 + k], ta[j1 + k], "equal") for k in range(i2 - i1)]
            else:
                pairs = [(tb[i], None, "only_before") for i in range(i1, i2)]
                pairs += [(None, ta[j], "only_after") for j in range(j1, j2)]
            for b, a, match in pairs:
                row = {"orig_line": m["orig_line"], "new_line": m["new_line"], "region": m["region"],
                       "line_alignment": method, "match": match}
                row.update(side("before", b))
                row.update(side("after", a))
                row["entropy_delta"] = (row["after_entropy"] - row["before_entropy"]
                                        if match == "equal" else None)
                rows.append(row)
    return pd.DataFrame(rows)


def region_table(tokens_before: pd.DataFrame, tokens_after: pd.DataFrame, labels: List[str]) -> pd.DataFrame:
    """変換箇所との位置関係 (region) ごとの集計。after は変換箇所より後に続く部分。"""
    order = ["before", "if_header", "then_body", "between", "else_body", "after"]
    regions = [r for r in order if r in set(tokens_before["region"]) | set(tokens_after["region"])]
    regions += sorted((set(tokens_before["region"].dropna()) | set(tokens_after["region"].dropna())) - set(regions))
    rows = []
    for region in regions:
        gb = tokens_before[tokens_before["region"] == region]
        ga = tokens_after[tokens_after["region"] == region]
        row = {"region": region}
        for name, g in (("before", gb), ("after", ga)):
            row[f"n_tokens_{name}"] = len(g)
            row[f"mean_entropy_{name}"] = float(g["entropy"].mean()) if len(g) else None
            row[f"sum_entropy_{name}"] = float(g["entropy"].sum())
            for label in labels:
                row[f"n_triggers_{label}_{name}"] = int(g[f"trigger_{label}"].sum())
                row[f"n_boundary_lines_{label}_{name}"] = int(
                    g.groupby("line")[f"trigger_{label}"].any().sum()) if len(g) else 0
        row["mean_entropy_delta"] = (row["mean_entropy_after"] - row["mean_entropy_before"]
                                     if row["mean_entropy_before"] is not None and row["mean_entropy_after"] is not None
                                     else None)
        row["sum_entropy_delta"] = row["sum_entropy_after"] - row["sum_entropy_before"]
        for label in labels:
            row[f"n_boundary_lines_{label}_delta"] = (row[f"n_boundary_lines_{label}_after"]
                                                      - row[f"n_boundary_lines_{label}_before"])
        rows.append(row)
    return pd.DataFrame(rows)


def summary_rows(metrics_before: Dict[str, Any], metrics_after: Dict[str, Any], labels: List[str]) -> Dict[str, Any]:
    """ファイル単位の指標の 変換前・変換後・差分。"""
    row: Dict[str, Any] = {}
    keys = ["loc", "total_tokens", "mean_entropy", "ppl"]
    keys += [f"su_count_{label}" for label in labels] + [f"lm_cc_{label}" for label in labels]
    for key in keys:
        b, a = metrics_before.get(key), metrics_after.get(key)
        row[f"{key}_before"] = b
        row[f"{key}_after"] = a
        row[f"{key}_delta"] = (a - b) if (a is not None and b is not None) else None
    row["loc_equal"] = metrics_before.get("loc") == metrics_after.get("loc")
    for label in labels:
        d = row[f"su_count_{label}_delta"]
        row[f"su_change_{label}"] = None if d is None else ("decreased" if d < 0 else "increased" if d > 0 else "unchanged")
    return row


def compare_pair(df_before: pd.DataFrame, df_after: pd.DataFrame, source_before: str, source_after: str,
                 line_map: List[Dict[str, Any]], thresholds: Dict[str, float]) -> Dict[str, Any]:
    """1組 (元コード, 変換後コード) を比較する。"""
    labels = list(thresholds)
    cb, ca = clean(df_before), clean(df_after)
    fb, fa = file_metrics(cb, thresholds), file_metrics(ca, thresholds)
    region_b = {m["orig_line"]: m["region"] for m in line_map}
    region_a = {m["new_line"]: m["region"] for m in line_map}
    partner_b = {m["orig_line"]: m["new_line"] for m in line_map}
    partner_a = {m["new_line"]: m["orig_line"] for m in line_map}
    tok_b = token_table(cb, fb["su"], region_b, partner_b)
    tok_a = token_table(ca, fa["su"], region_a, partner_a)
    return {
        "summary": summary_rows(fb["metrics"], fa["metrics"], labels),
        "metrics_before": fb["metrics"],
        "metrics_after": fa["metrics"],
        "units": {label: {"before": fb["su"][label]["units"], "after": fa["su"][label]["units"]} for label in labels},
        "tokens_before": tok_b,
        "tokens_after": tok_a,
        "lines": line_table(line_map, tok_b, tok_a, source_before, source_after, labels),
        "token_alignment": token_alignment(line_map, tok_b, tok_a, labels),
        "regions": region_table(tok_b, tok_a, labels),
    }
