# xcodeeval_code_translation/e87d5dda1727b2bf5f0cdfc5042c02ab

- item: xcodeeval_code_translation/e87d5dda1727b2bf5f0cdfc5042c02ab
- transform: if_else_swap (L3)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 17 | 17 | +0 |
| total_tokens | 126 | 127 | +1 |
| mean_entropy | 0.736 | 0.796 | +0.060 |
| ppl | 2.263 | 2.486 | +0.224 |
| su_count_p67 | 17 | 16 | -1 |
| su_count_p80_saved | 8 | 10 | +2 |
| lm_cc_p67 | 26.800 | 23.000 | -3.800 |
| lm_cc_p80_saved | 8.400 | 11.800 | +3.400 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `x, y = map(int, input().split(" "))` | 7.20 | 1 | \| | \| | `x, y = map(int, input().split(" "))` | 7.20 | before |
| 2 | \| | \| | `k = 0` | 2.99 | 2 | \| | \| | `k = 0` | 2.99 | before |
| 3 | \| | \| | `if(y % x != 0):` | 3.31 | 3 | \| | \| | `if not (y % x != 0):` | 3.31 | if_header |
| 4 | \| | \| | `    print(-1)` | 1.98 | 17 | \| |  | `    print(-1)` | 0.92 | then_body |
| 5 | \| |  | `else:` | 1.01 | 16 | \| | \| | `else:` | 1.82 | between |
| 6 | \| | \| | `    y = y / x` | 2.51 | 4 | \| | \| | `    y = y / x` | 2.05 | else_body |
| 7 | \| | \| | `    while y != 1:` | 2.52 | 5 | \| | \| | `    while y != 1:` | 2.34 | else_body |
| 8 | \| | \| | `        if(y % 2 == 0):` | 1.87 | 6 | \| | \| | `        if(y % 2 == 0):` | 1.72 | else_body |
| 9 | \| |  | `            y /= 2` | 0.71 | 7 |  |  | `            y /= 2` | 0.67 | else_body |
| 10 | \| |  | `            k += 1` | 0.78 | 8 | \| |  | `            k += 1` | 0.73 | else_body |
| 11 | \| |  | `        elif(y % 3 == 0):` | 1.05 | 9 | \| |  | `        elif(y % 3 == 0):` | 1.01 | else_body |
| 12 |  |  | `            y /= 3` | 0.21 | 10 |  |  | `            y /= 3` | 0.22 | else_body |
| 13 | \| |  | `            k += 1` | 0.92 | 11 | \| |  | `            k += 1` | 0.88 | else_body |
| 14 | \| |  | `        else:` | 0.74 | 12 | \| |  | `        else:` | 0.71 | else_body |
| 15 | \| |  | `            print(-1)` | 1.30 | 13 | \| | \| | `            print(-1)` | 1.58 | else_body |
| 16 | \| |  | `            break` | 0.76 | 14 | \| |  | `            break` | 1.15 | else_body |
| 17 | \| |  | `    else: print(k)           ` | 1.18 | 15 | \| | \| | `    else: print(k)           ` | 1.46 | else_body |
| 18 |  |  |  | - | 18 |  |  |  | - | after |
