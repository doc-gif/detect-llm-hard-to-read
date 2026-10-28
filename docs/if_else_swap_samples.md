# 用意したif-elseコード

xCodeEvalの10件と最小例3件について、元コードと入れ替えコードを別ファイルで保存した。
構文・AST・行数は確認済みである。13組の動作テストは完了した。モデル計測は未実行である。

選定方法と操作は [実験手順](if_else_swap_translation.md)を参照する。
完全な問題IDとハッシュは [samples.csv](../experiments/if_else_swap_translation_20261026/samples.csv)にある。

| 対象 | 選定用LOC | ifの行 | 元コード | 入れ替えコード | 差分 |
|---|---:|---:|---|---|---|
| 短い群1 | 13 | 10 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/b072dc9e37263b339fdf61bfaddd23a7/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/b072dc9e37263b339fdf61bfaddd23a7/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/b072dc9e37263b339fdf61bfaddd23a7/diff.patch) |
| 短い群2 | 17 | 3 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/e87d5dda1727b2bf5f0cdfc5042c02ab/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/e87d5dda1727b2bf5f0cdfc5042c02ab/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/e87d5dda1727b2bf5f0cdfc5042c02ab/diff.patch) |
| 短い群3 | 10 | 2 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/3b399bc13f31d7ac665a906c006042f4/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/3b399bc13f31d7ac665a906c006042f4/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/3b399bc13f31d7ac665a906c006042f4/diff.patch) |
| 中程度1 | 22 | 13 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/b55dc5b34d55f7d7ca7226f31d700712/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/b55dc5b34d55f7d7ca7226f31d700712/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/b55dc5b34d55f7d7ca7226f31d700712/diff.patch) |
| 中程度2 | 25 | 20 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/36cb9751a3bdba6cfb6f7369fb86b64b/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/36cb9751a3bdba6cfb6f7369fb86b64b/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/36cb9751a3bdba6cfb6f7369fb86b64b/diff.patch) |
| 中程度3 | 22 | 19 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/dae6d6e41bc2c3062a445566c056ffbf/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/dae6d6e41bc2c3062a445566c056ffbf/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/dae6d6e41bc2c3062a445566c056ffbf/diff.patch) |
| 中程度4 | 25 | 9 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/fdfacab3a62630ec4fa28ca77a3dc5cd/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/fdfacab3a62630ec4fa28ca77a3dc5cd/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/fdfacab3a62630ec4fa28ca77a3dc5cd/diff.patch) |
| 長い群1 | 59 | 7 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/0469a415b73c86652f520eaf69bd7311/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/0469a415b73c86652f520eaf69bd7311/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/0469a415b73c86652f520eaf69bd7311/diff.patch) |
| 長い群2 | 37 | 16 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/0709e40ee49b6439d328de121380ddcb/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/0709e40ee49b6439d328de121380ddcb/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/0709e40ee49b6439d328de121380ddcb/diff.patch) |
| 長い群3 | 47 | 4 | [元](../experiments/if_else_swap_translation_20261026/xcodeeval/4b2e18a331e01e1ae120ac59b747c8ba/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/xcodeeval/4b2e18a331e01e1ae120ac59b747c8ba/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/xcodeeval/4b2e18a331e01e1ae120ac59b747c8ba/diff.patch) |
| positive | 5 | 2 | [元](../experiments/if_else_swap_translation_20261026/minimal/positive/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/minimal/positive/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/minimal/positive/diff.patch) |
| even | 5 | 2 | [元](../experiments/if_else_swap_translation_20261026/minimal/even/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/minimal/even/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/minimal/even/diff.patch) |
| both_positive | 5 | 2 | [元](../experiments/if_else_swap_translation_20261026/minimal/both_positive/original.py) | [入れ替え](../experiments/if_else_swap_translation_20261026/minimal/both_positive/swapped.py) | [差分](../experiments/if_else_swap_translation_20261026/minimal/both_positive/diff.patch) |

各ディレクトリの `tests.json` にテスト入力と期待する出力を保存した。
最小例は単体テストで両方の分岐の出力を確認した。xCodeEvalも元コードと入れ替えコードの出力一致を確認した。2件に保存正解との文字列比較で不一致があり、詳細は実験手順に記録した。
