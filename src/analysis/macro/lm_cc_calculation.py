import os
import numpy as np
from .tree_sitter_config import py_parser
from tree_sitter import Node
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def get_line_indent(line_code: str) -> int:
    return len(line_code) - len(line_code.lstrip())


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


def is_contain_boundary(start_line, end_line, boundaries):
    for b in boundaries:
        if start_line < b <= end_line:
            return True
    return False


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


class TokenEntropyCalculator:
    def __init__(self, model_name="CodeLlama-7b-hf", cache_dir=None, temperature=1.0, device_map="auto",
                 float_type=torch.float32):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            dtype=float_type,
            cache_dir=cache_dir
        )
        self.model.eval()
        self.temperature = temperature
        self.float_type = float_type

        self.temperature = temperature
        self.float_type = float_type
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def calculate_entropy(self, probs):
        if self.float_type == np.float16 or self.float_type == torch.float16:
            min_val = 1e-5
        else:
            min_val = 1e-10
        log_probs = np.log(np.clip(probs, min_val, 1.0))
        return -np.sum(probs * log_probs)

    # def get_question_entropy(self, query, solution):
    #     full_text = f"{query} {solution}" if query else solution
    #     inputs = self.tokenizer(full_text, return_tensors="pt")
    #     input_ids = inputs["input_ids"].to(self.model.device)
    #     attention_mask = inputs["attention_mask"].to(self.model.device)
    #     with torch.no_grad():
    #         outputs = self.model(input_ids, attention_mask=attention_mask)
    #         logits = outputs.logits.cpu().numpy()
    #     scaled_logits = logits / self.temperature
    #     exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=-1, keepdims=True))
    #     probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
    #     query_tokens = self.tokenizer.tokenize(query)
    #     # solution_tokens = self.tokenizer.tokenize(solution)
    #     full_tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
    #     # start_idx = len(query_tokens) + 1
    #     start_idx = 1
    #     s_tokens = full_tokens[start_idx:]
    #     entropies = []
    #     for i in range(len(s_tokens)):
    #         pos = start_idx + i
    #         prev_probs = probs[0, pos - 1]
    #         entropy = self.calculate_entropy(prev_probs)
    #         entropies.append(entropy)
    #     return s_tokens, entropies

    def get_question_entropy(self, code):
        inputs = self.tokenizer(code, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.model.device)
        attention_mask = inputs["attention_mask"].to(self.model.device)
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits.cpu().numpy()
        scaled_logits = logits / self.temperature
        exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=-1, keepdims=True))
        probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

        code_tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        start_idx = 1
        s_tokens = code_tokens[1:]
        entropies = []
        for i in range(len(s_tokens)):
            pos = start_idx + i
            prev_probs = probs[0, pos - 1]
            entropy = self.calculate_entropy(prev_probs)
            entropies.append(entropy)
        return s_tokens, entropies


def find_first_real_newline(text: str) -> int:
    i = 0
    n = len(text)
    while i < n:
        if text[i] == '\\':
            i += 2
        elif text[i] == '\n':
            return i
        else:
            i += 1
    return -1


def get_code_with_boundaries(tokens, entropies, threshold=0.67):
    clean_code_lines = []
    start_end_tokens = []
    current_line = ""
    line_start_token = 0
    text = ""
    should_divide = False
    for idx, (token, entropy) in enumerate(zip(tokens, entropies)):
        # code llama
        token = token.replace("<0x0A>", "\n").replace("\u2581", " ")
        # print((token, entropy))
        last_entropy = 0 if idx == 0 else entropies[idx - 1]

        if idx > 0 and entropy >= threshold:
            should_divide = True

        current_line += token
        if "\n" in token or idx == len(tokens) - 1:
            clean_code_lines.append(current_line)
            current_line = ""
            start_end_tokens.append((line_start_token, idx))
            line_start_token = idx + 1
            if should_divide:
                last_newline_pos = text.rfind('\n')
                text = text[:last_newline_pos + 1] + "\n" + "=" * 30 + "\n" + text[last_newline_pos + 1:]
                should_divide = False
        text += token
    if line_start_token < len(tokens):
        start_end_tokens.append((line_start_token, len(tokens) - 1))

    return text, clean_code_lines, start_end_tokens


def get_block_cnt(node):
    if not node:
        return 0
    total = 1
    for child in node.get('children', []):
        total += get_block_cnt(child)
    return total


def get_total_branch(node):
    return get_block_cnt(node) - 1


def get_depth_sum(node, depth=1):
    if not node:
        return 0
    total = depth
    if 'children' in node:
        for child in node['children']:
            total += get_depth_sum(child, depth + 1)
    return total


def get_lmcc(tree_node):
    ALPHA = 0.8
    total_branch = get_total_branch(tree_node)
    depth_sum = get_depth_sum(tree_node, depth=1)
    return depth_sum * (1 - ALPHA) + total_branch * ALPHA


def get_code_lmcc(code, calculator=None, processor=None):
    if not calculator:
        calculator = TokenEntropyCalculator(
            model_name="codellama/CodeLlama-7b-hf",
            cache_dir="",  # default cache dir
        )
    if not processor:
        processor = CodeBlockProcessor()
    tokens, entropies = calculator.get_question_entropy(code)
    code_with_boundaries, _, start_end_tokens = get_code_with_boundaries(tokens, entropies, threshold=0.67)
    block_tree_dict = processor.parse_code_blocks(code_with_boundaries, tokens=tokens,
                                                  start_end_tokens=start_end_tokens)
    return get_lmcc(block_tree_dict)



