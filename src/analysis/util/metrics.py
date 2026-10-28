import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL
import re
import tempfile
import os
from complexipy import code_complexity
from src.analysis.util.utils import get_total_branch, get_depth_sum, format_python_code


def get_file_cc(file_path):
    radon_cmd = ["radon", "cc", file_path, "-s"]
    try:
        result = subprocess.check_output(
            radon_cmd,
            stdin=DEVNULL,
            stderr=DEVNULL
            )
        result = result.decode("utf-8")
        messages = result.strip().split("\n")
        
        complexity = 0
        for m in messages:
            if m.strip().endswith(")"):
                c = m.split("(")[-1].split(")")[0]
                complexity += float(c)
        if complexity == 0:
            complexity = 1
        
    
    except Exception as e:
        complexity = 1
        # print("Error to calculate complexity: ", e)
        # print(code)

    if complexity == 1:
        code = open(file_path, 'r').read()
        codelines = code.splitlines()
        codelines = [line.rstrip() for line in codelines if line.strip()!=""]
        codelines = ["\t"+line for line in codelines]
        newcode = "def f():\n" + "\n".join(codelines)
        with open(file_path, 'w') as f:
            f.write(newcode)
        radon_cmd = ["radon", "cc", file_path, "-s"]
        try:
            result = subprocess.check_output(
                radon_cmd,
                stdin=DEVNULL,
                stderr=DEVNULL
                )
            result = result.decode("utf-8")
            messages = result.strip().split("\n")
            
            complexity = 0
            for m in messages:
                if m.strip().endswith(")"):
                    c = m.split("(")[-1].split(")")[0]
                    complexity += float(c)
            if complexity == 0:
                complexity = 1
        except Exception as e:
            complexity = 1
            # print("Error to calculate complexity: ", e)
            # print(code)
    return complexity

def get_code_cc(code):
    _, temp_name = tempfile.mkstemp(prefix="cc_temp_", suffix=".py")
    with open(temp_name, 'w') as f:
        f.write(code)
    complexity = get_file_cc(temp_name)
    os.remove(temp_name)
    return complexity

def get_code_loc(code):
    content_lines = code.splitlines()
    loc = len([line for line in content_lines if line.strip()])
    return loc

def get_code_cog(code):
    try:
        result = code_complexity(code)
        cog = result.complexity
    except:
        cog = 1
    return cog

def get_code_mi(code):
    # code = format_python_code(code)
    _, temp_name = tempfile.mkstemp(prefix="cc_temp_", suffix=".py")
    with open(temp_name, 'w') as f:
        f.write(code)
    try:
        out = subprocess.check_output(['radon', 'mi', temp_name, '-s'], stderr=subprocess.STDOUT, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        out = e.output if hasattr(e, 'output') else ''
    except FileNotFoundError:
        return None
    m = re.search(r'\(([\d\.]+)\)', out)
    if m:
        try:
            res =  float(m.group(1))
        except ValueError:
            res = None
    else:
        res = None
    os.remove(temp_name)
    return res

def get_code_hc_difficulty(code):
    code = format_python_code(code)
    _, temp_name = tempfile.mkstemp(prefix="cc_temp_", suffix=".py")
    with open(temp_name, 'w') as f:
        f.write(code)
    try:
        with open(temp_name, 'w', encoding='utf-8') as f:
            f.write(code)

        try:
            out = subprocess.check_output(['radon', 'hal', temp_name], stderr=subprocess.STDOUT, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            out = e.output if hasattr(e, 'output') else ''
        except FileNotFoundError:
            return None
        m = re.search(r'^\s*difficulty:\s*([0-9]+(?:\.[0-9]+)?)', out, re.MULTILINE | re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                return None
        return None
    finally:
        try:
            os.remove(temp_name)
        except Exception:
            pass

def get_lmcc(tree_node):
    ALPHA = 0.8
    total_branch = get_total_branch(tree_node)
    depth_sum = get_depth_sum(tree_node, depth=1)
    return depth_sum*(1-ALPHA) + total_branch*ALPHA










