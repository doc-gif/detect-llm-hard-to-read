"""変換前後を並べて確認するためのレポート (HTML / Markdown)。

- 行は元コードの行順に並べ、右側に対応する変換後の行 (入れ替えで移動した行を含む) を置く
- 各トークンはエントロピーに応じて背景色を付け、閾値以上 (SU 境界の原因) は枠で囲む
- 行頭の ``|`` 印は SU 境界 (その行の前で SU が切れる) を表す
"""
from __future__ import annotations

import html
from typing import Any, Dict, List

import pandas as pd

_REGION_LABEL = {
    "before": "変換箇所より前", "if_header": "if の行 (条件を否定)", "then_body": "元の if 側の本体",
    "between": "else の行など", "else_body": "元の else 側の本体", "after": "変換箇所より後",
}


def _fmt(v: Any, digits: int = 3) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "-"
    if isinstance(v, float):
        return f"{v:.{digits}f}"
    return str(v)


def _fmt_delta(v: Any, digits: int = 3) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "-"
    if isinstance(v, float):
        return f"{v:+.{digits}f}"
    return f"{v:+d}" if isinstance(v, int) else str(v)


def _token_spans(tokens: pd.DataFrame, line: int, label: str) -> str:
    out = []
    for _, t in tokens[tokens["line"] == line].iterrows():
        text = t["text"].replace("\n", "")
        if not text:
            text = "↵"  # 改行トークン
            cls = "tok nl"
        else:
            cls = "tok"
        alpha = min(float(t["entropy"]) / 3.0, 1.0)
        trig = " trig" if t[f"trigger_{label}"] else ""
        title = f"idx={t['idx']} H={t['entropy']:.3f} SU={t[f'su_{label}']}"
        out.append(f'<span class="{cls}{trig}" style="--a:{alpha:.2f}" title="{html.escape(title)}">'
                   f"{html.escape(text).replace(' ', '&nbsp;')}</span>")
    return "".join(out)


def render_html(title: str, result: Dict[str, Any], meta: Dict[str, Any], labels: List[str]) -> str:
    label = labels[0]
    s = result["summary"]
    tb, ta, lines = result["tokens_before"], result["tokens_after"], result["lines"]

    keys = ["loc", "total_tokens", "mean_entropy", "ppl"] + [f"su_count_{l}" for l in labels] + [f"lm_cc_{l}" for l in labels]
    summary_rows = "".join(
        f"<tr><th>{k}</th><td>{_fmt(s[f'{k}_before'])}</td><td>{_fmt(s[f'{k}_after'])}</td>"
        f"<td>{_fmt_delta(s[f'{k}_delta'])}</td></tr>" for k in keys)

    body_rows = []
    for _, r in lines.iterrows():
        region = r["region"]
        marks_b = "".join(f'<td class="b">{"|" if r[f"boundary_{l}_before"] else ""}</td>' for l in labels)
        marks_a = "".join(f'<td class="b">{"|" if r[f"boundary_{l}_after"] else ""}</td>' for l in labels)
        body_rows.append(
            f'<tr class="r-{region}" title="{html.escape(_REGION_LABEL.get(region, region))}">'
            f'<td class="n">{r["orig_line"]}</td>{marks_b}<td class="code">{_token_spans(tb, r["orig_line"], label)}</td>'
            f'<td class="n">{r["new_line"]}</td>{marks_a}<td class="code">{_token_spans(ta, r["new_line"], label)}</td>'
            f'<td class="d">{_fmt_delta(r.get("sum_entropy_delta"))}</td></tr>')

    def unit_item(u: Dict[str, Any]) -> str:
        triggers = ", ".join(f"{t['token_str']}={t['entropy']:.2f}" for t in u["trigger_tokens"])
        span = "(空: 先頭行の前の境界)" if u["start_line"] is None else f"L{u['start_line']}–L{u['end_line']}"
        return (f"<li>SU{u['su_index']}: {span} ({u['n_tokens']} tokens)"
                f" {html.escape(triggers)}</li>")

    units_html = []
    for l in labels:
        for side in ("before", "after"):
            units = result["units"][l][side]
            items = "".join(unit_item(u) for u in units)
            units_html.append(f"<div><h3>{l} ({meta['thresholds'][l]}) {side}: {len(units)} SU</h3><ul>{items}</ul></div>")

    head_cols = "".join(f"<th>{l}</th>" for l in labels)
    meta_rows = "".join(f"<tr><th>{html.escape(str(k))}</th><td>{html.escape(str(v))}</td></tr>" for k, v in meta.items())
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>
body{{font-family:system-ui,sans-serif;margin:16px;color:#1d1d1f;background:#fff}}
table{{border-collapse:collapse}} td,th{{padding:2px 6px;border-bottom:1px solid #eee;vertical-align:top}}
.code{{font-family:ui-monospace,Menlo,Consolas,monospace;white-space:pre;font-size:13px}}
.tok{{background:rgba(230,120,20,var(--a));border-radius:2px}} .tok.nl{{color:#aaa}}
.tok.trig{{outline:1.5px solid #c00}} .n{{color:#888;text-align:right;font-family:monospace}}
.b{{color:#c00;font-weight:bold;text-align:center;width:1.2em}} .d{{font-family:monospace;color:#555}}
.r-if_header{{background:#eef4ff}} .r-then_body{{background:#f2fbf2}} .r-else_body{{background:#fff8e8}}
.r-between{{background:#f5f5f5}} .wrap{{overflow-x:auto}} .units{{display:flex;flex-wrap:wrap;gap:24px}}
</style></head><body>
<h1>{html.escape(title)}</h1>
<table>{meta_rows}</table>
<h2>ファイル単位の指標</h2>
<table><tr><th></th><th>変換前</th><th>変換後</th><th>差分</th></tr>{summary_rows}</table>
<h2>行ごとの対応 (元コードの行順)</h2>
<p>背景色の濃さ = トークンのエントロピー (3 nats で最大)。赤枠 = {label} の閾値以上。
「|」= その行の前に SU 境界 (列は {', '.join(labels)})。行の色: 青 = if の行、緑 = 元の if 側本体、黄 = 元の else 側本体。
右端は行のエントロピー合計の差分 (変換後 − 変換前)。</p>
<div class="wrap"><table><tr><th>元</th>{head_cols}<th>変換前</th><th>新</th>{head_cols}<th>変換後</th><th>ΔΣH</th></tr>
{''.join(body_rows)}</table></div>
<h2>SU の範囲</h2><div class="units">{''.join(units_html)}</div>
</body></html>
"""


def render_markdown(title: str, result: Dict[str, Any], meta: Dict[str, Any], labels: List[str]) -> str:
    s = result["summary"]
    out = [f"# {title}", ""]
    out += [f"- {k}: {v}" for k, v in meta.items()]
    out += ["", "| 指標 | 変換前 | 変換後 | 差分 |", "|---|---|---|---|"]
    keys = ["loc", "total_tokens", "mean_entropy", "ppl"] + [f"su_count_{l}" for l in labels] + [f"lm_cc_{l}" for l in labels]
    for k in keys:
        out.append(f"| {k} | {_fmt(s[f'{k}_before'])} | {_fmt(s[f'{k}_after'])} | {_fmt_delta(s[f'{k}_delta'])} |")
    bcols = " | ".join(f"境界{l}" for l in labels)
    out += ["", "行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。", "",
            f"| 元 | {bcols} | 変換前 | maxH | 新 | {bcols} | 変換後 | maxH | region |",
            "|" + "---|" * (7 + 2 * len(labels))]

    def cell(text: str) -> str:
        return "`" + text.replace("|", "\\|").replace("`", "'") + "`" if text.strip() else ""

    for _, r in result["lines"].iterrows():
        mb = " | ".join("\\|" if r[f"boundary_{l}_before"] else "" for l in labels)
        ma = " | ".join("\\|" if r[f"boundary_{l}_after"] else "" for l in labels)
        out.append(f"| {r['orig_line']} | {mb} | {cell(r['text_before'])} | {_fmt(r.get('max_entropy_before'), 2)} | "
                   f"{r['new_line']} | {ma} | {cell(r['text_after'])} | {_fmt(r.get('max_entropy_after'), 2)} | {r['region']} |")
    return "\n".join(out) + "\n"
