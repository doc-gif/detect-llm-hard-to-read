"""if/else 入れ替え変換 (Python)。

``if C: A else: B`` を ``if not (C): B else: A`` に書き換える。

対応言語: Python 3 (Python の ``ast`` で構文解析できるコードのみ)

適用条件 (満たさない候補は理由付きで ``not_applicable`` として記録する):
  - ``if`` 文に ``else`` 節がちょうど1つあり、``elif`` 節が無い
  - if 側・else 側とも本体が次の行以降のブロックになっている
    (``if c: x`` や ``else: y`` のような1行形式は対象外)
  - ファイル全体が Python 3 として構文解析でき、Tree-sitter でもエラーが無い

条件の否定方法 (比較演算子の置き換えはしない):
  - 既定 (``unwrap_not=True``): 条件が ``not X`` なら ``X`` にする。
    ``if`` も ``not`` も ``X`` の真偽値 (``bool(X)``) を1回だけ評価するので結果は同じ。
  - それ以外は ``not`` を付ける。条件が識別子・呼び出し・括弧式などの原子的な式なら
    ``not X``、それ以外は ``not (X)`` (``negation_style="always_paren"`` なら常に括弧)。
  - ``a < b`` を ``a >= b`` にするような書き換えは、NaN や独自の比較演算子を持つ
    オブジェクトで意味が変わるので行わない。

LOC を変えないための書き方:
  - 条件式の前後に ``not (`` と ``)`` を挿入する (または ``not`` を削る) だけで、改行は増減しない
  - if 側と else 側の本体は「行単位」でそのまま入れ替える (インデント・コメント・空行を含め
    各行の文字列は変えない)。本体の外にある行 (``else:`` の行、本体の前後の空行・コメント行)
    は元の位置に残す
  - 変換後に Python の ``ast`` で「期待される木 (条件を否定して body と orelse を交換した木)」
    と一致するか、行数が同じかを検査し、外れたら ``failed`` にする
"""
from __future__ import annotations

import ast
import copy
import warnings
from typing import Dict, List, Optional, Tuple

import tree_sitter_python
from tree_sitter import Language, Node, Parser

from .base import (
    STATUS_FAILED,
    STATUS_NOT_APPLICABLE,
    STATUS_OK,
    Candidate,
    LineMapping,
    Transformation,
    TransformOutcome,
)

_PARSER = Parser(Language(tree_sitter_python.language()))

#: ``not X`` と括弧なしで書いてよい (優先順位の問題が起きない) 条件式のノード種別
_ATOMIC_TYPES = frozenset({
    "identifier", "call", "attribute", "subscript", "parenthesized_expression",
    "list", "dictionary", "set", "tuple", "string", "concatenated_string",
    "integer", "float", "true", "false", "none",
    "list_comprehension", "dictionary_comprehension", "set_comprehension", "generator_expression",
})


def _block_rows(block: Node) -> Tuple[int, int]:
    """ブロックが占める行範囲 (0始まり、両端含む)。"""
    start_row = block.start_point[0]
    end_row, end_col = block.end_point
    if end_col == 0 and end_row > start_row:
        end_row -= 1  # 終端が次の行頭になっている場合
    return start_row, end_row


def _find_ast_if(tree: ast.AST, lineno: int, col_offset: int) -> Optional[ast.If]:
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and node.lineno == lineno and node.col_offset == col_offset:
            return node
    return None


class IfElseSwap(Transformation):
    """条件を否定して if 側と else 側の本体を交換する。"""

    name = "if_else_swap"
    languages = frozenset({"python"})

    def __init__(self, unwrap_not: bool = True, negation_style: str = "auto") -> None:
        if negation_style not in ("auto", "always_paren"):
            raise ValueError(f"negation_style は auto / always_paren のどちらか: {negation_style!r}")
        super().__init__(unwrap_not=unwrap_not, negation_style=negation_style)
        self.unwrap_not = unwrap_not
        self.negation_style = negation_style

    # ------------------------------------------------------------------
    # 候補の列挙
    # ------------------------------------------------------------------
    def _parse(self, source: str):
        source_bytes = source.encode("utf-8")
        tree = _PARSER.parse(source_bytes)
        return source_bytes, tree

    def _if_nodes(self, tree) -> List[Node]:
        nodes: List[Node] = []
        stack = [tree.root_node]
        while stack:
            node = stack.pop()
            if node.type == "if_statement":
                nodes.append(node)
            stack.extend(reversed(node.children))
        nodes.sort(key=lambda n: n.start_byte)
        return nodes

    def _check_node(self, node: Node) -> Tuple[Optional[str], Dict]:
        """適用できないなら理由を返す。適用できるなら (None, 位置情報)。"""
        alternatives = node.children_by_field_name("alternative")
        elifs = [a for a in alternatives if a.type == "elif_clause"]
        elses = [a for a in alternatives if a.type == "else_clause"]
        if elifs:
            return "elif 節を含む (単純な if/else ではない)", {}
        if not elses:
            return "else 節が無い", {}
        if len(elses) != 1:
            return "else 節が複数ある", {}
        if node.has_error:
            return "Tree-sitter の構文エラーを含む", {}

        condition = node.child_by_field_name("condition")
        consequence = node.child_by_field_name("consequence")
        else_clause = elses[0]
        else_body = else_clause.child_by_field_name("body")
        if condition is None or consequence is None or else_body is None:
            return "条件・本体のノードが見つからない", {}

        colon_row = None
        for child in node.children:
            if child.type == ":":
                colon_row = child.start_point[0]
                break
        if colon_row is None:
            return "if のコロンが見つからない", {}

        then_rows = _block_rows(consequence)
        else_rows = _block_rows(else_body)
        else_row = else_clause.start_point[0]
        else_colon_row = else_row
        for child in else_clause.children:
            if child.type == ":":
                else_colon_row = child.start_point[0]
                break

        if then_rows[0] <= colon_row:
            return "if 側の本体が if と同じ行にある (1行形式)", {}
        if else_rows[0] <= else_colon_row:
            return "else 側の本体が else と同じ行にある (1行形式)", {}
        if then_rows[1] >= else_row:
            return "if 側の本体と else が同じ行にある", {}

        return None, {
            "if_row": node.start_point[0],
            "if_col_byte": node.start_point[1],
            "colon_row": colon_row,
            "then_rows": then_rows,
            "else_row": else_row,
            "else_rows": else_rows,
            "end_row": node.end_point[0],
            "condition": condition,
        }

    def find_candidates(self, source: str) -> List[Candidate]:
        source_bytes, tree = self._parse(source)
        candidates: List[Candidate] = []
        for index, node in enumerate(self._if_nodes(tree)):
            reason, pos = self._check_node(node)
            start_line = node.start_point[0] + 1
            cand = Candidate(
                transform=self.name,
                index=index,
                variant_id=f"ifelse_L{start_line}",
                start_line=start_line,
                end_line=node.end_point[0] + 1,
            )
            if reason is not None:
                cand.status = STATUS_NOT_APPLICABLE
                cand.reason = reason
            else:
                cond = pos["condition"]
                cand.info = {
                    "condition": source_bytes[cond.start_byte:cond.end_byte].decode("utf-8"),
                    "condition_type": cond.type,
                    "then_lines": [pos["then_rows"][0] + 1, pos["then_rows"][1] + 1],
                    "else_line": pos["else_row"] + 1,
                    "else_lines": [pos["else_rows"][0] + 1, pos["else_rows"][1] + 1],
                }
            candidates.append(cand)
        return candidates

    # ------------------------------------------------------------------
    # 適用
    # ------------------------------------------------------------------
    def _negate(self, cond: Node, source_bytes: bytes) -> Tuple[bytes, int, int, str]:
        """条件の否定。``(置換後バイト列, 置換開始, 置換終了, 方法)`` を返す。"""
        text = source_bytes[cond.start_byte:cond.end_byte]
        if self.unwrap_not and cond.type == "not_operator":
            arg = cond.child_by_field_name("argument")
            if arg is not None:
                return source_bytes[arg.start_byte:arg.end_byte], cond.start_byte, cond.end_byte, "remove_not"
        if self.negation_style == "auto" and cond.type in _ATOMIC_TYPES:
            return b"not " + text, cond.start_byte, cond.end_byte, "add_not"
        return b"not (" + text + b")", cond.start_byte, cond.end_byte, "add_not_paren"

    def apply(self, source: str, candidate: Candidate) -> TransformOutcome:
        outcome = TransformOutcome(candidate=candidate, status=STATUS_FAILED)
        if candidate.status != STATUS_OK:
            outcome.status = candidate.status
            outcome.reason = candidate.reason
            return outcome

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                orig_tree = ast.parse(source)
        except SyntaxError as exc:
            outcome.reason = f"Python 3 として構文解析できない: {exc.msg} (line {exc.lineno})"
            return outcome

        source_bytes, tree = self._parse(source)
        nodes = self._if_nodes(tree)
        if candidate.index >= len(nodes):
            outcome.reason = "候補の if 文が見つからない"
            return outcome
        node = nodes[candidate.index]
        reason, pos = self._check_node(node)
        if reason is not None:
            outcome.status = STATUS_NOT_APPLICABLE
            outcome.reason = reason
            return outcome

        # --- 1. 条件の否定 (if の行の中だけを書き換える) -----------------
        new_cond, cstart, cend, method = self._negate(pos["condition"], source_bytes)
        if method != "remove_not" and cstart > 0 and (source_bytes[cstart - 1:cstart].isalnum() or source_bytes[cstart - 1:cstart] == b"_"):
            # ``if(x):`` のようにキーワード直後に空白が無い場合は ``if not (x):`` になるよう空白を足す
            new_cond = b" " + new_cond
        lines = source_bytes.split(b"\n")  # 行区切りは \n (read_text が改行を正規化する)
        then_s, then_e = pos["then_rows"]
        else_s, else_e = pos["else_rows"]
        prefix_len = sum(len(l) + 1 for l in lines[:then_s])  # then 本体より前のバイト数
        if cend > prefix_len:
            outcome.reason = "条件式が if 側の本体と重なっている"
            return outcome
        prefix = source_bytes[:prefix_len]
        new_prefix = prefix[:cstart] + new_cond + prefix[cend:]
        new_prefix_lines = new_prefix.split(b"\n")[:-1]  # 末尾は空要素 (prefix は改行で終わる)

        # --- 2. 本体を行単位で入れ替える ---------------------------------
        then_lines = lines[then_s:then_e + 1]
        between = lines[then_e + 1:else_s]   # else: の行、本体の外の空行・コメント行
        else_lines = lines[else_s:else_e + 1]
        rest = lines[else_e + 1:]
        new_lines = new_prefix_lines + else_lines + between + then_lines + rest
        if len(new_lines) != len(lines):
            # 例: ``if not \<改行> x:`` の not を外すと行継続ごと消えて行数が減る。行対応を作る前に止める
            outcome.reason = (f"条件の否定で行数が変わる ({len(lines)} → {len(new_lines)} 行)。"
                              "条件が複数行にまたがる not 式など")
            outcome.checks = {"line_count_before": len(lines), "line_count_after": len(new_lines),
                              "line_count_equal": False}
            return outcome
        new_bytes = b"\n".join(new_lines)
        try:
            new_source = new_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            outcome.reason = f"変換後のバイト列を UTF-8 として解釈できない: {exc}"
            return outcome

        # --- 3. 行対応 -----------------------------------------------------
        n_else, n_between = len(else_lines), len(between)
        header_rows = range(pos["if_row"], pos["colon_row"] + 1)
        line_map: List[LineMapping] = []
        for row in range(len(lines)):
            if row < then_s:
                new_row = row
                region = "if_header" if row in header_rows else "before"
                if row > pos["colon_row"]:
                    region = "between"  # if の行と本体の間の空行・コメント行
            elif row <= then_e:
                new_row = then_s + n_else + n_between + (row - then_s)
                region = "then_body"
            elif row < else_s:
                new_row = then_s + n_else + (row - then_e - 1)
                region = "between"
            elif row <= else_e:
                new_row = then_s + (row - else_s)
                region = "else_body"
            else:
                new_row = row
                region = "after"
            changed = lines[row] != new_lines[new_row]
            line_map.append(LineMapping(orig_line=row + 1, new_line=new_row + 1, region=region, text_changed=changed))

        outcome.transformed_source = new_source
        outcome.line_map = line_map
        outcome.edits = [
            {
                "kind": "negate_condition",
                "method": method,
                "line": pos["condition"].start_point[0] + 1,
                "before": source_bytes[cstart:cend].decode("utf-8"),
                "after": new_cond.decode("utf-8"),
            },
            {
                "kind": "swap_bodies",
                "then_lines_before": [then_s + 1, then_e + 1],
                "else_lines_before": [else_s + 1, else_e + 1],
                "then_lines_after": [then_s + n_else + n_between + 1, then_s + n_else + n_between + len(then_lines)],
                "else_lines_after": [then_s + 1, then_s + n_else],
            },
        ]

        # --- 4. 検査 -------------------------------------------------------
        checks = self._verify(source, new_source, orig_tree, pos, method)
        outcome.checks = checks
        if not checks["compiles"]:
            outcome.reason = f"変換後のコードが構文解析できない: {checks.get('compile_error')}"
            return outcome
        if not checks["ast_matches_expected"]:
            outcome.reason = "変換後の AST が期待される AST (条件否定 + 本体交換) と一致しない"
            return outcome
        if not checks["line_count_equal"]:
            outcome.reason = "変換前後で行数が変わった"
            return outcome
        outcome.status = STATUS_OK
        return outcome

    def _verify(self, source: str, new_source: str, orig_tree: ast.AST, pos: Dict, method: str) -> Dict:
        checks: Dict = {
            "line_count_before": source.count("\n") + 1,
            "line_count_after": new_source.count("\n") + 1,
        }
        checks["line_count_equal"] = checks["line_count_before"] == checks["line_count_after"]
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                compile(new_source, "<transformed>", "exec")
                new_tree = ast.parse(new_source)
            checks["compiles"] = True
        except SyntaxError as exc:
            checks["compiles"] = False
            checks["compile_error"] = f"{exc.msg} (line {exc.lineno})"
            checks["ast_matches_expected"] = False
            return checks

        # Tree-sitter の if 開始位置 (行・バイト列) は ast の lineno / col_offset (UTF-8 バイト) と一致する
        expected = copy.deepcopy(orig_tree)
        target = _find_ast_if(expected, pos["if_row"] + 1, pos["if_col_byte"])
        if target is None:
            checks["ast_matches_expected"] = False
            checks["ast_error"] = "元コードの ast に対応する If が見つからない"
            return checks
        if method == "remove_not":
            if not (isinstance(target.test, ast.UnaryOp) and isinstance(target.test.op, ast.Not)):
                checks["ast_matches_expected"] = False
                checks["ast_error"] = "not を外したが元の条件が not 式ではない"
                return checks
            target.test = target.test.operand
        else:
            target.test = ast.UnaryOp(op=ast.Not(), operand=target.test)
        target.body, target.orelse = target.orelse, target.body
        checks["ast_matches_expected"] = ast.dump(expected) == ast.dump(new_tree)
        return checks
