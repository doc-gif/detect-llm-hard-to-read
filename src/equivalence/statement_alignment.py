"""処理文の対応付けと、トークンの所属文の決定 (位置情報を使わない AST の一致)。

``compare.token_alignment`` は行の対応と difflib でトークンを突き合わせる。多対一の行対応では、
変換後の同じトークンが複数の変換前トークンの相手として重複して使われる。
LOC が変わる変換 (文の結合、本体の同じ行への配置) では行の対応が成り立たないため、
ここでは行の対応を使わない。

対応付けの規則
--------------
1. ``ast.parse`` で得た ``ast.stmt`` を、出現順 (前順) に並べる。
2. 各文について「位置属性を除き、入れ子の文の並びを ``[S*]`` に置き換えた ``ast.dump``」を作る
   (``head_key``。子の文の個数は含めない)。``if`` なら条件式、``def`` なら名前・引数・戻り値の注釈になる。
   ``lineno`` などの位置情報は含めない。入れ子の深さも対応の条件に加える。
3. 変換前後の ``(head_key, depth)`` の列を difflib の最長一致で突き合わせる。
   結果は 1 対 1 で、同じ文を 2 回使わない。一致しない文は片側だけの行として残す。
4. 部分木まで含めた ``ast.dump`` が等しければ ``same_subtree``、見出しだけ等しければ
   ``same_head`` とする。

トークンの所属
--------------
各トークンはちょうど 1 つの所有者へ割り当てる。所有者は「トークン内の最初の非空白文字を
含む最も内側の文」で、どの文にも入らなければ ``OUTSIDE`` (-1) とする。
``;``、``else``、``:``、改行、インデントのような文ではない文字は、それを囲む文の所有になる。
(``collect_metrics`` が AST 情報を引く位置と同じ規則である。)

トークンが文の境界をまたぐ場合
------------------------------
トークンの文字範囲は、次のトークンの開始位置までとする (最後のトークンはソース末尾まで)。
範囲内の非空白文字が 2 つ以上の所有者にまたがるトークンは ``crosses_boundary=True`` とし、
関係する所有者を ``spanned_owners`` に残す。割り当ては先頭の非空白文字の所有者だけで、
トークンを分割も複製もしない。空白だけのトークンは先頭の文字の所有者に割り当てる。
したがって、変換前後のトークン数の合計は各側の総トークン数と一致する。
"""
from __future__ import annotations

import ast
import difflib
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pandas as pd

from schema.records import ParquetSchema as PCol

ENT = PCol.METRIC_ENTROPY
OUTSIDE = -1


def normalize_newlines(text: str) -> str:
    """``utils.io.read_text`` (universal newlines) と同じ改行の正規化。"""
    return text.replace("\r\n", "\n").replace("\r", "\n")


@dataclass
class Statement:
    sid: int
    parent: int
    depth: int
    node_type: str
    head_key: str
    full_key: str
    start_line: int
    end_line: int
    start: int  # 文字位置 [start, end)
    end: int
    head_end: int  # 最初の入れ子の文の直前 (入れ子がなければ end)


def shallow_dump(node: Any, root: bool = True) -> str:
    """位置属性を除き、入れ子の文 (の並び) を ``S`` / ``[S*]`` に置き換えた ``ast.dump`` 相当の文字列。"""
    if isinstance(node, ast.AST):
        if not root and isinstance(node, ast.stmt):
            return "S"
        parts = [f"{name}={shallow_dump(value, False)}" for name, value in ast.iter_fields(node)]
        return f"{type(node).__name__}({', '.join(parts)})"
    if isinstance(node, list):
        if any(isinstance(v, ast.stmt) for v in node):
            return "[S*]"  # 子の文の個数は見出しに含めない (子は別に対応づける)
        return "[" + ", ".join(shallow_dump(v, False) for v in node) + "]"
    return repr(node)


def _line_starts(source: str) -> List[int]:
    starts = [0]
    for i, ch in enumerate(source):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def parse_statements(source: str) -> List[Statement]:
    """``source`` の全ての文を前順で返す。構文エラーは ``SyntaxError`` のまま投げる。"""
    source = normalize_newlines(source)
    tree = ast.parse(source)
    starts = _line_starts(source)
    lines = source.split("\n")

    def offset(lineno: int, byte_col: int) -> int:
        text = lines[lineno - 1].encode("utf-8")[:byte_col].decode("utf-8", errors="ignore")
        return starts[lineno - 1] + len(text)

    statements: List[Statement] = []

    def visit(node: ast.AST, parent: int, depth: int) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.stmt):
                end_line = child.end_lineno or child.lineno
                end_col = child.end_col_offset if child.end_col_offset is not None else 0
                stmt = Statement(
                    sid=len(statements), parent=parent, depth=depth, node_type=type(child).__name__,
                    head_key=shallow_dump(child), full_key=ast.dump(child, include_attributes=False),
                    start_line=child.lineno, end_line=end_line,
                    start=offset(child.lineno, child.col_offset), end=offset(end_line, end_col), head_end=0)
                stmt.head_end = stmt.end
                statements.append(stmt)
                visit(child, stmt.sid, depth + 1)
            else:
                visit(child, parent, depth)

    visit(tree, OUTSIDE, 0)
    first_child: Dict[int, int] = {}
    for stmt in statements:
        if stmt.parent != OUTSIDE:
            first_child[stmt.parent] = min(first_child.get(stmt.parent, stmt.start), stmt.start)
    for stmt in statements:
        if stmt.sid in first_child:
            stmt.head_end = first_child[stmt.sid]
    return statements


def ast_equal(source_before: str, source_after: str) -> bool:
    """位置情報を除いたモジュール全体の AST が等しいか。"""
    a = ast.dump(ast.parse(normalize_newlines(source_before)), include_attributes=False)
    b = ast.dump(ast.parse(normalize_newlines(source_after)), include_attributes=False)
    return a == b


def align_statements(before: List[Statement], after: List[Statement]) -> Dict[str, Any]:
    """変換前後の文を 1 対 1 で対応づける。"""
    keys_b = [(s.head_key, s.depth) for s in before]
    keys_a = [(s.head_key, s.depth) for s in after]
    matcher = difflib.SequenceMatcher(None, keys_b, keys_a, autojunk=False)
    pairs: List[Dict[str, Any]] = []
    for block in matcher.get_matching_blocks():
        for k in range(block.size):
            i, j = block.a + k, block.b + k
            pairs.append({
                "pair_id": len(pairs), "before_sid": i, "after_sid": j,
                "match": "same_subtree" if before[i].full_key == after[j].full_key else "same_head",
            })
    used_b = {p["before_sid"] for p in pairs}
    used_a = {p["after_sid"] for p in pairs}
    return {
        "pairs": pairs,
        "unmatched_before": [s.sid for s in before if s.sid not in used_b],
        "unmatched_after": [s.sid for s in after if s.sid not in used_a],
    }


def assign_tokens(df_clean: pd.DataFrame, source: str, statements: List[Statement]) -> pd.DataFrame:
    """各トークンを 1 つの文へ割り当てる。列: pos, char_start, char_end, owner, owner_type,
    crosses_boundary, spanned_owners, is_whitespace, has_position。"""
    source = normalize_newlines(source)
    starts = _line_starts(source)
    owner_at = [OUTSIDE] * len(source)
    for stmt in statements:  # 前順なので内側の文が後から上書きする
        for i in range(stmt.start, stmt.end):
            owner_at[i] = stmt.sid
    types = {s.sid: s.node_type for s in statements}

    lines = df_clean[PCol.LINE].tolist()
    columns = df_clean[PCol.COLUMN].tolist()
    begin: List[Optional[int]] = []
    for line, column in zip(lines, columns):
        if pd.isna(line) or pd.isna(column):
            begin.append(None)
            continue
        begin.append(starts[int(line) - 1] + int(column))
    positioned = [b for b in begin if b is not None]
    if any(b2 < b1 for b1, b2 in zip(positioned, positioned[1:])):
        raise ValueError("トークンの開始位置が単調に増えていない")

    rows = []
    for pos, start in enumerate(begin):
        if start is None:
            rows.append({"pos": pos, "char_start": None, "char_end": None, "owner": OUTSIDE,
                         "owner_type": "<outside>", "crosses_boundary": False, "spanned_owners": "",
                         "is_whitespace": False, "has_position": False})
            continue
        nxt = next((b for b in begin[pos + 1:] if b is not None), len(source))
        end = max(nxt, start)
        text = source[start:end]
        non_ws = [i for i in range(start, end) if not source[i].isspace()]
        if non_ws:
            owner = owner_at[non_ws[0]]
            spanned = sorted({owner_at[i] for i in non_ws})
        else:
            owner = owner_at[start] if start < len(source) else OUTSIDE
            spanned = [owner]
        rows.append({
            "pos": pos, "char_start": start, "char_end": end, "owner": owner,
            "owner_type": types.get(owner, "<outside>"), "crosses_boundary": len(spanned) > 1,
            "spanned_owners": ",".join(str(x) for x in spanned),
            "is_whitespace": not non_ws and bool(text), "has_position": True,
        })
    return pd.DataFrame(rows)


def _side(prefix: str, stmt: Optional[Statement], source: str, tokens: pd.DataFrame, labels: List[str]) -> Dict[str, Any]:
    keys = ["sid", "node_type", "depth", "start_line", "end_line", "n_lines", "head_text", "n_tokens",
            "n_whitespace_tokens", "n_crossing_tokens", "sum_entropy", "mean_entropy", "max_entropy"]
    row: Dict[str, Any] = {f"{prefix}_{k}": None for k in keys}
    for label in labels:
        row[f"{prefix}_n_triggers_{label}"] = None
        row[f"{prefix}_first_su_{label}"] = None
    if stmt is None:
        return row
    own = tokens[tokens["owner"] == stmt.sid]
    head = source[stmt.start:stmt.head_end].strip().replace("\n", "⏎")
    row.update({
        f"{prefix}_sid": stmt.sid, f"{prefix}_node_type": stmt.node_type, f"{prefix}_depth": stmt.depth,
        f"{prefix}_start_line": stmt.start_line, f"{prefix}_end_line": stmt.end_line,
        f"{prefix}_n_lines": stmt.end_line - stmt.start_line + 1, f"{prefix}_head_text": head,
        f"{prefix}_n_tokens": len(own),
        f"{prefix}_n_whitespace_tokens": int(own["is_whitespace"].sum()),
        f"{prefix}_n_crossing_tokens": int(own["crosses_boundary"].sum()),
        f"{prefix}_sum_entropy": float(own["entropy"].sum()) if len(own) else None,
        f"{prefix}_mean_entropy": float(own["entropy"].mean()) if len(own) else None,
        f"{prefix}_max_entropy": float(own["entropy"].max()) if len(own) else None,
    })
    visible = own[~own["is_whitespace"]]
    for label in labels:
        row[f"{prefix}_n_triggers_{label}"] = int(own[f"trigger_{label}"].sum())
        row[f"{prefix}_first_su_{label}"] = int(visible[f"su_{label}"].iloc[0]) if len(visible) else None
    return row


def statement_table(before: List[Statement], after: List[Statement], source_before: str, source_after: str,
                    tokens_before: pd.DataFrame, tokens_after: pd.DataFrame, alignment: Dict[str, Any],
                    labels: List[str]) -> pd.DataFrame:
    """対応づけた文ごとに、変換前後の行数・トークン数・エントロピー・SU 境界の原因トークン数を並べる。

    ``tokens_*`` は ``owner`` / ``entropy`` / ``is_whitespace`` / ``crosses_boundary`` と、
    ラベルごとの ``trigger_<label>`` / ``su_<label>`` 列を持つ。
    """
    source_before, source_after = normalize_newlines(source_before), normalize_newlines(source_after)
    rows: List[Dict[str, Any]] = []
    for pair in alignment["pairs"]:
        rows.append({"pair_id": pair["pair_id"], "match": pair["match"],
                     **_side("before", before[pair["before_sid"]], source_before, tokens_before, labels),
                     **_side("after", after[pair["after_sid"]], source_after, tokens_after, labels)})
    for sid in alignment["unmatched_before"]:
        rows.append({"pair_id": None, "match": "only_before",
                     **_side("before", before[sid], source_before, tokens_before, labels),
                     **_side("after", None, source_after, tokens_after, labels)})
    for sid in alignment["unmatched_after"]:
        rows.append({"pair_id": None, "match": "only_after",
                     **_side("before", None, source_before, tokens_before, labels),
                     **_side("after", after[sid], source_after, tokens_after, labels)})
    outside_b = tokens_before[tokens_before["owner"] == OUTSIDE]
    outside_a = tokens_after[tokens_after["owner"] == OUTSIDE]
    rows.append({"pair_id": None, "match": "outside_statements",
                 "before_node_type": "<outside>", "after_node_type": "<outside>",
                 "before_n_tokens": len(outside_b), "after_n_tokens": len(outside_a),
                 "before_sum_entropy": float(outside_b["entropy"].sum()) if len(outside_b) else None,
                 "after_sum_entropy": float(outside_a["entropy"].sum()) if len(outside_a) else None})
    table = pd.DataFrame(rows)
    for key in ("n_lines", "n_tokens", "sum_entropy"):
        b, a = f"before_{key}", f"after_{key}"
        if b in table and a in table:
            table[f"{key}_delta"] = pd.to_numeric(table[a]) - pd.to_numeric(table[b])
    return table
