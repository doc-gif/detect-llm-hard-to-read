"""Read saved question scores without collapsing distinct question IDs."""
import json
import logging
import math
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

logger = logging.getLogger(__name__)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_scores(dataset_name: str, config: dict) -> dict:
    """Preserve full IDs; a missing score is missing, never an incorrect answer."""
    path = Path(config["path"])
    if not path.exists():
        raise FileNotFoundError(f"Score file missing ({dataset_name}): {path}")
    with path.open(encoding="utf-8") as stream:
        data = json.load(stream, object_pairs_hook=_unique_object)
    scores = {}
    if config["format"] not in {"simple", "nested"}:
        raise ValueError(f"Unknown score format: {config['format']}")
    for uid, record in data.items():
        value = record if config["format"] == "simple" else record.get("pass@1")
        if value is None:
            logger.warning("Missing score excluded: dataset=%s uid=%s", dataset_name, uid)
            continue
        if config["format"] == "nested" and record.get("task_id", uid) != uid:
            raise ValueError(f"Score key/task_id mismatch: {uid}")
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"Non-numeric score: {uid}={value!r}")
        if not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f"Score outside [0, 1]: {uid}={value!r}")
        scores[uid] = float(value)
    return scores


def validate_summary_ids(df):
    """One row represents one metric record, identified by dataset and full uid."""
    keys = ["dataset", "uid"]
    if df[keys].isna().any().any() or df.duplicated(keys).any():
        raise ValueError("Summary requires non-missing, unique (dataset, uid) keys")


def new_output_dir(parent, requested=None):
    """Create a fresh run directory; historical results must not be overwritten."""
    path = Path(requested) if requested else Path(parent) / (
        datetime.now(timezone.utc).strftime("run-%Y%m%dT%H%M%SZ-") + uuid4().hex[:8]
    )
    path.mkdir(parents=True, exist_ok=False)
    return path


def audit_humaneval_code(df, metric_dir=None, scored_dir=None):
    """Compare measured source with the exact question's saved main.py.

    AST equality ignores whitespace/comments, but preserves imports and program structure.
    This is an identity check, not a proof of semantic equivalence.
    """
    import ast
    import hashlib
    root = Path(__file__).resolve().parents[2]
    metric_dir = Path(metric_dir) if metric_dir else root / "data" / "humaneval"
    scored_dir = Path(scored_dir) if scored_dir else root.parent / "lm-cc" / "dataset" / "humaneval"
    records = []
    for uid in df["uid"]:
        row = {"dataset": "humaneval", "uid": uid, "code_status": "unverified"}
        try:
            measured = (metric_dir / f"{uid}.py").read_text(encoding="utf-8")
            scored = (scored_dir / uid / "main.py").read_text(encoding="utf-8")
            row["measured_sha256"] = hashlib.sha256(measured.encode()).hexdigest()
            row["scored_sha256"] = hashlib.sha256(scored.encode()).hexdigest()
            measured_ast = ast.dump(ast.parse(measured), include_attributes=False)
            scored_ast = ast.dump(ast.parse(scored), include_attributes=False)
            row["code_status"] = "exact" if measured == scored else (
                "ast_equal" if measured_ast == scored_ast else "ast_mismatch")
        except (OSError, SyntaxError) as exc:
            row["code_status"] = type(exc).__name__
        records.append(row)
    return records


def filter_matching_code(df, dataset_name):
    """Exclude HumanEval joins whose full-ID code identity cannot be verified."""
    if dataset_name != "humaneval":
        return df
    checks = audit_humaneval_code(df)
    accepted = {row["uid"] for row in checks if row["code_status"] in {"exact", "ast_equal"}}
    for row in checks:
        if row["uid"] not in accepted:
            logger.warning("Code join excluded: dataset=%s uid=%s reason=%s",
                           dataset_name, row["uid"], row["code_status"])
    return df.loc[df["uid"].isin(accepted)].copy()
