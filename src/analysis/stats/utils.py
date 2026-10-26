from collections import defaultdict
import tempfile, os, subprocess, uuid
from textwrap import dedent
import re

def get_depth_sum(node, depth=1):
    if not node:
        return 0
    total = depth 
    if 'children' in node:
        for child in node['children']:
            total += get_depth_sum(child, depth + 1)
    return total


def get_block_cnt(node):
    if not node: 
        return 0
    total = 1  
    for child in node.get('children', []):
        total += get_block_cnt(child)  
    return total

def get_total_branch(node):
    return get_block_cnt(node) - 1

def get_max_depth(node, depth=1):
    if not node:
        return 0
    children = node.get("children")
    if not children:
        return depth
    max_d = depth
    for child in children:
        d = get_max_depth(child, depth + 1)
        if d > max_d:
            max_d = d
    return max_d


def get_avg_depth(node, depth=1):
    if not node:
        return 0.0
    total_depth = get_depth_sum(node, depth)
    total_nodes = get_block_cnt(node)
    if total_nodes == 0:
        return 0.0
    return float(total_depth) / total_nodes


def get_max_width(node):
    if not node:
        return 0
    level_counts = defaultdict(int)
    
    def traverse(node, level):
        weight = node.get("weight", 1)
        level_counts[level] += weight
        for child in node.get("children", []):
            traverse(child, level + 1)
    traverse(node, 1)  
    return max(level_counts.values())  


def get_avg_children(node):
    if not node:
        return 0.0
    internal_count = 0
    total_children = 0
    def traverse(n):
        nonlocal internal_count, total_children
        children = n.get("children", []) if isinstance(n, dict) else []
        if children:
            internal_count += 1
            total_children += len(children)
            for c in children:
                traverse(c)
    traverse(node)
    return float(total_children) / internal_count if internal_count > 0 else 0.0

def format_python_code(code):
    # 去装饰器
    if "@" in code:
        code = '\n'.join(line for line in code.split('\n') if not (line.strip().startswith("@")))
    # 去统一缩进
    code = dedent(code)
    random_filename = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.py")
    try:
        with open(random_filename, 'w') as f:
            f.write(code)
        # 运行 black 格式化
        try:
            subprocess.run(
                ["black", "--quiet", "--fast", random_filename], 
                check=True, 
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            try:
                subprocess.run(
                    ["black", "--quiet", random_filename], 
                    check=True, 
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:    
                print(f"Format failed: {e.stderr}")
                # print(code)
                return None
        # 读取格式化后的代码
        with open(random_filename, 'r') as f:
            formatted_code = f.read()
        return formatted_code
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        os.remove(random_filename)



def remove_comments_and_docstrings(code):
    string_placeholders = []
    string_pattern = r'''(
        \"\"\" (?:\\. | "(?!\"\"") | [^\\"])*? \"\"\" |  
        \''' (?:\\. | '(?!'') | [^\\'])*? \'''     |  
        " (?: \\. | [^"\\] )* "                    |  
        ' (?: \\. | [^'\\] )* '                       
    )'''
    def replace_string(match):
        string_placeholders.append(match.group(1))
        return f'__STRING_{len(string_placeholders)-1}__'
    
    code = re.sub(string_pattern, replace_string, code, flags=re.DOTALL | re.VERBOSE)
    code = re.sub(r'#.*', '', code)
    for idx, content in enumerate(string_placeholders):
        code = code.replace(f'__STRING_{idx}__', content)

    code = re.sub(r'^(?:\s*)(["\']{3}.*?["\']{3})(?:\s*)$', '', code, flags=re.DOTALL | re.MULTILINE)
    patterns = [
        r'(def\s+\w+\(.*?\):\s*?\n)(\s*["\']{3}.*?["\']{3}\n)',
        r'(class\s+\w+.*?:\s*?\n)(\s*["\']{3}.*?["\']{3}\n)',
        r'(async\s+def\s+\w+\(.*?\):\s*?\n)(\s*["\']{3}.*?["\']{3}\n)'
    ]
    for pattern in patterns:
        code = re.sub(pattern, r'\1', code, flags=re.DOTALL)
    lines = [line for line in code.splitlines() if line.strip()]
    return '\n'.join(lines)



