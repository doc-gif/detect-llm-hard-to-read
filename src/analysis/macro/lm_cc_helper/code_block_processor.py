from .tree_sitter_config import py_parser
from tree_sitter import Node

def get_line_indent(line_code: str) -> int:
    return len(line_code) - len(line_code.lstrip())

def is_contain_boundary(start_line, end_line, boundaries):
    for b in boundaries:
        if start_line < b <= end_line:
            return True
    return False


def get_control_end_line(root_node: Node, target_line: int) -> int:
    def _traverse(node: Node):
        start_row, _ = node.start_point
        end_row, _ = node.end_point

        if not (start_row <= target_line <= end_row):
            return None

        for child in node.children:
            result = _traverse(child)
            if result is not None:
                return result
        code_block_types = {
            "if_statement", "for_statement", "while_statement",
            "function_definition", "class_definition",
            "try_statement", "with_statement", "match_statement",
            "elif_clause", "else_clause", "except_clause", "finally_clause"
        }
        if node.type in code_block_types:
            return node.end_point[0]
        return None

    return _traverse(root_node)

def is_contain_samelevel_boundary(start_line, end_line, boundaries, clean_code):
    clean_lines = clean_code.splitlines()
    start_line_code = clean_lines[start_line]
    start_indent = get_line_indent(start_line_code)
    for b in boundaries:
        if start_line < b <= end_line:
            b_line_code = clean_lines[b]
            b_indent = get_line_indent(b_line_code)
            if b_indent == start_indent:
                return True
    return False

def get_next_boundary(boundaries, target_line, end_line):
    boundary_count = len(boundaries)
    i = 0
    while i < boundary_count and boundaries[i] <= target_line:
            i += 1
    next_boundary = boundaries[i] if i < boundary_count else end_line + 1
    return next_boundary

def is_control_start(code_line):
    stripped_line = code_line.strip()
    is_control_start = any(
        stripped_line.startswith(keyword)
        for keyword in
        ['if', 'while', 'for', 'def', 'class', 'else', 'elif', 'try', 'with', 'match', 'except', 'finally']
    ) and ':' in stripped_line
    return is_control_start


def is_def_start(line_code):
    in_str = False
    bracket_stack = []
    closing_to_opening = {')': '(', ']': '[', '}': '{'}

    for c in line_code:
        if c in "'\"":
            in_str = not in_str
        elif not in_str:
            if c in closing_to_opening.values():
                bracket_stack.append(c)
            elif c in closing_to_opening:
                if not bracket_stack or bracket_stack.pop() != closing_to_opening[c]:
                    return True
    return len(bracket_stack) > 0

def get_matching_brace_line(root_node, left_brace_line):
    target_node_types = {
        "dictionary",
        "list",
        "call",
        "tuple",
        "set",
        "parenthesized_expression"
    }

    def traverse(node):
        if (node.type in target_node_types) and (node.start_point[0] == left_brace_line):
            if node.end_point[0] > left_brace_line:
                return node.end_point[0]

        for child in node.children:
            result = traverse(child)
            if result is not None:
                return result
        return None
    return traverse(root_node)

def get_block_end_line(block_start_line, clean_code, boundaries, root_node):
    clean_lines = clean_code.splitlines()
    cursor = block_start_line
    start_indent = get_line_indent(clean_lines[block_start_line])
    next_boundary = get_next_boundary(boundaries, target_line=block_start_line, end_line=len(clean_lines) - 1)
    block_end_line = next_boundary - 1
    while cursor < next_boundary:
        current_line_code = clean_lines[cursor]

        current_indent = get_line_indent(current_line_code)
        if current_indent < start_indent:
            block_end_line = cursor - 1
            break

        control_end = None

        if is_control_start(current_line_code):
            control_end = get_control_end_line(root_node, cursor)
        elif is_def_start(current_line_code):
            control_end = get_matching_brace_line(root_node, cursor)
        if control_end and control_end >= next_boundary:
            cursor = control_end
            next_boundary = get_next_boundary(boundaries, target_line=cursor, end_line=len(clean_lines) - 1)

        cursor += 1
    block_end_line = cursor - 1
    return block_end_line


class CodeBlockProcessor:
    def __init__(self):
        self.parser = py_parser

    def parse_code_blocks(self, code_with_boundaries, tokens, start_end_tokens):
        lines = code_with_boundaries.split('\n')
        code_lines = []
        boundaries = []

        for i, line in enumerate(lines):
            if line.strip() == "":
                continue
            if line.strip().startswith('='):
                boundaries.append(len(code_lines))
            else:
                code_lines.append(line)

        clean_code = '\n'.join(code_lines)
        tree = self.parser.parse(bytes(clean_code, 'utf8'))
        # print(code_with_boundaries)
        # 主处理流程
        root_block = {
            "block_code": clean_code,
            "start_line": 1,
            "end_line": len(code_lines),
            "children": self._process_level(
                clean_code=clean_code,
                boundaries=boundaries,
                root_node=tree.root_node,
                start_line=0,
                end_line=len(code_lines) - 1,
                tokens=tokens,
                start_end_tokens=start_end_tokens
            ),
            "start_token": start_end_tokens[0][0],
            "end_token": start_end_tokens[-1][1]
        }
        return root_block

    # start_line <= target_code <= end_line

    def _process_level(self, clean_code: str, boundaries, start_line, end_line, root_node, tokens, start_end_tokens):
        children = []
        if not is_contain_boundary(start_line, end_line, boundaries):
            return children
        clean_lines = clean_code.splitlines()
        if is_contain_samelevel_boundary(start_line, end_line, boundaries, clean_code):
            block_start_line = start_line
        else:
            next_boundary = get_next_boundary(boundaries, target_line=start_line, end_line=end_line)
            block_start_line = next_boundary

        block_end_line = get_block_end_line(block_start_line, clean_code, boundaries=boundaries, root_node=root_node)
        if block_start_line == start_line and block_end_line == end_line:
            next_boundary = get_next_boundary(boundaries, target_line=start_line, end_line=end_line)
            block_start_line = next_boundary
        while block_start_line <= end_line:
            block_end_line = get_block_end_line(block_start_line, clean_code, boundaries=boundaries,
                                                root_node=root_node)
            new_child = {
                "block_code": "\n".join(clean_lines[block_start_line: block_end_line + 1]),
                "start_line": block_start_line + 1,
                "end_line": block_end_line + 1,
                "start_token": start_end_tokens[block_start_line][0],
                "end_token": start_end_tokens[block_end_line][1],
                "children": []
            }
            children.append(new_child)
            next_boundary = get_next_boundary(boundaries, target_line=block_end_line, end_line=end_line)
            block_start_line = next_boundary

        for child in children:
            child_start = child["start_line"] - 1
            child_end = child["end_line"] - 1

            child_children = self._process_level(clean_code=clean_code,
                                                 boundaries=boundaries,
                                                 start_line=child_start,
                                                 end_line=child_end,
                                                 root_node=root_node,
                                                 tokens=tokens,
                                                 start_end_tokens=start_end_tokens)
            child['children'] = child_children
        return children