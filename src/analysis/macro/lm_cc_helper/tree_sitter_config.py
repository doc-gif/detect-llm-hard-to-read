"""LM-CC のブロック解析で使う Tree-sitter (Python) パーサ。"""
import tree_sitter_python
from tree_sitter import Language, Parser

PYTHON_LANGUAGE = Language(tree_sitter_python.language())
py_parser = Parser(PYTHON_LANGUAGE)
