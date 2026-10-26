"""変換候補の一覧 (dry-run): データセット × 変換ごとに、適用できる候補の数と適用できない理由を数える。

実験ディレクトリは作らず、ファイルも書かない (``--out`` を指定したときの CSV だけ)。
候補ごとに ``apply`` まで行うので、``failed`` (変換後の検査で落ちるもの) もここで分かる。
動作確認・計測は行わない。
"""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from equivalence import datasets as ds
from equivalence.transforms import STATUS_FAILED, STATUS_NOT_APPLICABLE, STATUS_OK, create_transformation
from utils.io import read_text

STATUSES = [STATUS_OK, STATUS_NOT_APPLICABLE, STATUS_FAILED]


def reason_group(reason: Optional[str]) -> Optional[str]:
    """理由から行番号などの個別の部分を落として集計用にする (``"…: 詳細"``, ``"… (詳細)"``)。"""
    if not isinstance(reason, str) or not reason:  # 欠損 (NaN) も含む
        return None
    return re.split(r"\s*[:(。]", reason, maxsplit=1)[0].strip() or reason


def scan_dataset(dataset: str, transform: str, options: Optional[Dict[str, Any]] = None,
                 ids: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """1つのデータセット × 変換の全候補。候補が無いファイルも ``status=None`` の1行で残す。"""
    spec = ds.get_dataset(dataset)
    transformation = create_transformation(transform, **(options or {}))
    rows: List[Dict[str, Any]] = []
    for uid in ids if ids is not None else ds.list_ids(spec):
        base = {"dataset": dataset, "transform": transform, "uid": uid}
        try:
            source = read_text(ds.source_path(spec, uid))
            candidates = transformation.find_candidates(source)
        except Exception as exc:  # noqa: BLE001
            rows.append({**base, "status": STATUS_FAILED, "reason": f"{type(exc).__name__}: {exc}"})
            continue
        if not candidates:
            rows.append({**base, "status": None, "reason": None})
        for cand in candidates:
            out = transformation.apply(source, cand)
            rows.append({**base, "variant_id": cand.variant_id, "start_line": cand.start_line,
                         "end_line": cand.end_line, "status": out.status, "reason": out.reason})
    table = pd.DataFrame(rows, columns=["dataset", "transform", "uid", "variant_id", "start_line", "end_line",
                                        "status", "reason"])
    table["reason_group"] = table["reason"].map(reason_group)
    return table


def summarize(table: pd.DataFrame) -> pd.DataFrame:
    """データセット × 変換ごとのファイル数・候補数。"""
    rows = []
    for (dataset, transform), g in table.groupby(["dataset", "transform"], sort=False):
        cands = g[g["status"].notna()]
        row = {"dataset": dataset, "transform": transform, "files": g["uid"].nunique(),
               "files_with_candidates": cands["uid"].nunique(),
               "files_with_ok": cands.loc[cands["status"] == STATUS_OK, "uid"].nunique(),
               "candidates": len(cands)}
        row.update({s: int((cands["status"] == s).sum()) for s in STATUSES})
        rows.append(row)
    return pd.DataFrame(rows)


def reason_counts(table: pd.DataFrame) -> pd.DataFrame:
    """適用できない・失敗した候補の理由ごとの件数。"""
    bad = table[table["status"].isin([STATUS_NOT_APPLICABLE, STATUS_FAILED])]
    if bad.empty:
        return pd.DataFrame(columns=["dataset", "transform", "status", "reason_group", "count", "example_reason"])
    return (bad.groupby(["dataset", "transform", "status", "reason_group"], sort=False)
            .agg(count=("uid", "size"), example_reason=("reason", "first"))
            .reset_index()
            .sort_values(["dataset", "transform", "status", "count"], ascending=[True, True, True, False]))
