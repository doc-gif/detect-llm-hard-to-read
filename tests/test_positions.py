from utils.positions import OffsetIndex


def test_char_to_line_column_ascii():
    idx = OffsetIndex.build("ab\ncd\n")
    assert idx.char_to_line_column(0) == (1, 0)
    assert idx.char_to_line_column(4) == (2, 1)


def test_ts_point_uses_byte_columns_on_non_ascii_lines():
    text = 'x = "あい"; y = 1\n'
    idx = OffsetIndex.build(text)
    y = text.index("y")
    # 文字単位の列と、Tree-sitter 用のバイト単位の列は非 ASCII 行で一致しない
    assert idx.char_to_line_column(y) == (1, y)
    assert idx.char_to_ts_point(y) == (0, len(text[:y].encode("utf-8")))
    assert idx.char_to_byte(y) == len(text[:y].encode("utf-8"))
