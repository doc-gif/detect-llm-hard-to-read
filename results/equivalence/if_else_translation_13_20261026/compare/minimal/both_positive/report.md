# minimal/both_positive

- item: minimal/both_positive
- transform: if_else_swap (L2)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 5 | 5 | +0 |
| total_tokens | 40 | 42 | +2 |
| mean_entropy | 1.009 | 1.167 | +0.158 |
| ppl | 2.675 | 2.944 | +0.268 |
| su_count_p67 | 6 | 6 | +0 |
| su_count_p80_saved | 5 | 5 | +0 |
| lm_cc_p67 | 5.800 | 5.800 | +0.000 |
| lm_cc_p80_saved | 4.200 | 4.200 | +0.000 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `a, b = map(int, input().split())` | 5.21 | 1 | \| | \| | `a, b = map(int, input().split())` | 5.21 | before |
| 2 | \| | \| | `if a > 0 and b > 0:` | 2.57 | 2 | \| | \| | `if not (a > 0 and b > 0):` | 2.93 | if_header |
| 3 | \| | \| | `    print(1)` | 3.11 | 5 | \| | \| | `    print(1)` | 4.07 | then_body |
| 4 | \| |  | `else:` | 0.81 | 4 | \| |  | `else:` | 1.21 | between |
| 5 | \| | \| | `    print(0)` | 2.03 | 3 | \| | \| | `    print(0)` | 1.44 | else_body |
| 6 |  |  |  | - | 6 |  |  |  | - | after |
