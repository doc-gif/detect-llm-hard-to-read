"""pytest 共通設定: src/ を import ルートにする (pyproject.toml の pythonpath と同じ)。"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
