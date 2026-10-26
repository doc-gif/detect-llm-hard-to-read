"""等価変換の共通インターフェース。

変換は「候補の列挙」と「1候補だけを適用」の2段に分ける。1つのソースに候補が
複数あっても、それぞれを元コードに対して別々に適用し、元コードと1対1で比較できるようにする。

新しい変換を追加するときは :class:`Transformation` を継承して ``transforms/__init__.py``
の ``register_transformation`` で登録する。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

#: 候補・適用結果の状態
STATUS_OK = "ok"                          # 変換できた (構文・AST・行数の検査を通過)
STATUS_NOT_APPLICABLE = "not_applicable"  # 適用条件を満たさない (理由を記録)
STATUS_FAILED = "failed"                  # 適用を試みたが検査に失敗した (理由を記録)


@dataclass
class LineMapping:
    """変換前の1行が変換後のどの行になったか (行番号は1始まり)。

    ``region`` は変換箇所との位置関係:
      before / if_header / then_body / between / else_body / after
    (if/else 入れ替え以外の変換では独自の名前を使ってよい)
    """
    orig_line: int
    new_line: int
    region: str
    text_changed: bool


@dataclass
class Candidate:
    """変換候補 1 か所。"""
    transform: str
    index: int                 # ソース内の出現順 (0始まり)
    variant_id: str            # 例: "ifelse_L12" (ファイル名・ID に使う)
    start_line: int            # 候補ノードの開始行 (1始まり)
    end_line: int              # 候補ノードの終了行
    status: str = STATUS_OK
    reason: Optional[str] = None
    info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransformOutcome:
    """1候補を適用した結果。"""
    candidate: Candidate
    status: str
    reason: Optional[str] = None
    transformed_source: Optional[str] = None
    edits: List[Dict[str, Any]] = field(default_factory=list)
    line_map: List[LineMapping] = field(default_factory=list)
    checks: Dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> Dict[str, Any]:
        """JSON 保存用 (変換後ソース本文は別ファイルに保存するので含めない)。"""
        return {
            "candidate": asdict(self.candidate),
            "status": self.status,
            "reason": self.reason,
            "edits": self.edits,
            "line_map": [asdict(m) for m in self.line_map],
            "checks": self.checks,
        }


class Transformation(ABC):
    """等価変換の基底クラス。"""

    #: 登録名 (設定ファイルの ``transform.name``)
    name: str = "abstract"
    #: 対応言語 (``language`` パッケージの ``language_name``)
    languages: frozenset = frozenset()

    def __init__(self, **options: Any) -> None:
        self.options = options

    @abstractmethod
    def find_candidates(self, source: str) -> List[Candidate]:
        """適用候補を列挙する。適用できない候補も理由付きで返す。"""

    @abstractmethod
    def apply(self, source: str, candidate: Candidate) -> TransformOutcome:
        """候補 1 か所だけを変換する。元の ``source`` は変更しない。"""

    def describe(self) -> Dict[str, Any]:
        """記録用の設定値。"""
        return {"name": self.name, "languages": sorted(self.languages), "options": dict(self.options)}
