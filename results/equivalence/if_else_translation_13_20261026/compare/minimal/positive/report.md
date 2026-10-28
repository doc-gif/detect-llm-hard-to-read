# minimal/positive

- item: minimal/positive
- transform: if_else_swap (L2)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 5 | 5 | +0 |
| total_tokens | 29 | 31 | +2 |
| mean_entropy | 1.454 | 1.719 | +0.265 |
| ppl | 3.859 | 4.952 | +1.094 |
| su_count_p67 | 6 | 6 | +0 |
| su_count_p80_saved | 5 | 6 | +1 |
| lm_cc_p67 | 5.800 | 5.800 | +0.000 |
| lm_cc_p80_saved | 4.200 | 5.800 | +1.600 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `x = int(input())` | 7.20 | 1 | \| | \| | `x = int(input())` | 7.20 | before |
| 2 | \| | \| | `if x > 0:` | 3.18 | 2 | \| | \| | `if not (x > 0):` | 3.19 | if_header |
| 3 | \| | \| | `    print(1)` | 2.52 | 5 | \| | \| | `    print(1)` | 4.21 | then_body |
| 4 | \| |  | `else:` | 1.18 | 4 | \| | \| | `else:` | 1.45 | between |
| 5 | \| | \| | `    print(0)` | 1.48 | 3 | \| | \| | `    print(0)` | 2.22 | else_body |
| 6 |  |  |  | - | 6 |  |  |  | - | after |
