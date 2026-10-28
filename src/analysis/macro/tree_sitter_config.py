import os
import platform
from tree_sitter import Language, Parser
import tree_sitter_python

current_directory = os.getcwd()
ext = '.dll' if platform.system() == 'Windows' else '.so'

TREE_SITTER_PATH_PYTHON = os.path.join(current_directory, 'tree_sitter/build/python' + ext)


PYTHON_LANGUAGE = Language(tree_sitter_python.language())
py_parser = Parser()
py_parser.language = PYTHON_LANGUAGE

