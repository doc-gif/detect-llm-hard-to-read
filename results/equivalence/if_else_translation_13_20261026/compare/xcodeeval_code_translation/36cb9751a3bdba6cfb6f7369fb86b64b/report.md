# xcodeeval_code_translation/36cb9751a3bdba6cfb6f7369fb86b64b

- item: xcodeeval_code_translation/36cb9751a3bdba6cfb6f7369fb86b64b
- transform: if_else_swap (L20)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 25 | 25 | +0 |
| total_tokens | 215 | 218 | +3 |
| mean_entropy | 1.045 | 1.085 | +0.040 |
| ppl | 3.062 | 3.159 | +0.097 |
| su_count_p67 | 25 | 25 | +0 |
| su_count_p80_saved | 17 | 18 | +1 |
| lm_cc_p67 | 19.600 | 19.600 | +0.000 |
| lm_cc_p80_saved | 12.600 | 14.000 | +1.400 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `curX, curY = (int(x) for x in input().split())` | 7.65 | 1 | \| | \| | `curX, curY = (int(x) for x in input().split())` | 7.65 | before |
| 2 | \| | \| |  | 2.71 | 2 | \| | \| |  | 2.71 | before |
| 3 | \| | \| | `x = abs(curX)` | 3.74 | 3 | \| | \| | `x = abs(curX)` | 3.74 | before |
| 4 | \| |  | `y = abs(curY)` | 0.86 | 4 | \| |  | `y = abs(curY)` | 0.86 | before |
| 5 | \| | \| |  | 1.76 | 5 | \| | \| |  | 1.76 | before |
| 6 | \| | \| | `y1 = int( x + y )` | 3.89 | 6 | \| | \| | `y1 = int( x + y )` | 3.89 | before |
| 7 | \| | \| | `x1 = y1` | 1.35 | 7 | \| | \| | `x1 = y1` | 1.35 | before |
| 8 | \| | \| | `area = x1 * x1` | 2.08 | 8 | \| | \| | `area = x1 * x1` | 2.08 | before |
| 9 | \| | \| | `newA = area` | 2.56 | 9 | \| | \| | `newA = area` | 2.56 | before |
| 10 | \| | \| |  | 2.67 | 10 | \| | \| |  | 2.67 | before |
| 11 | \| | \| | `while newA <= area:` | 3.12 | 11 | \| | \| | `while newA <= area:` | 3.12 | before |
| 12 | \| | \| | `    x1, y1 = x1 + 1, x1 + 1` | 2.11 | 12 | \| | \| | `    x1, y1 = x1 + 1, x1 + 1` | 2.11 | before |
| 13 | \| |  | `    area = newA` | 1.17 | 13 | \| |  | `    area = newA` | 1.17 | before |
| 14 | \| |  | `    newA = x1 * x1` | 1.11 | 14 | \| |  | `    newA = x1 * x1` | 1.11 | before |
| 15 | \| |  |  | 1.21 | 15 | \| |  |  | 1.21 | before |
| 16 | \| | \| |  | 2.49 | 16 | \| | \| |  | 2.49 | before |
| 17 | \| | \| | `x1 = int((x1-1) * (curX / abs(curX)))` | 2.79 | 17 | \| | \| | `x1 = int((x1-1) * (curX / abs(curX)))` | 2.79 | before |
| 18 |  |  | `y1 = int((y1-1) * (curY / abs(curY)))` | 0.51 | 18 |  |  | `y1 = int((y1-1) * (curY / abs(curY)))` | 0.51 | before |
| 19 | \| |  |  | 1.16 | 19 | \| |  |  | 1.16 | before |
| 20 | \| | \| | `if x1 < 0 :` | 2.81 | 20 | \| | \| | `if not (x1 < 0) :` | 2.81 | if_header |
| 21 | \| | \| | `    print(str(x1) + ' 0 0 ' + str(y1))` | 2.71 | 23 | \| |  | `    print(str(x1) + ' 0 0 ' + str(y1))` | 1.16 | then_body |
| 22 | \| |  | `else:` | 1.21 | 22 | \| | \| | `else:` | 1.35 | between |
| 23 | \| |  | `    print('0 ' + str(y1) + ' ' + str(x1) + ' 0')` | 0.79 | 21 | \| | \| | `    print('0 ' + str(y1) + ' ' + str(x1) + ' 0')` | 4.84 | else_body |
| 24 | \| |  |  | 0.94 | 24 | \| |  |  | 1.00 | after |
| 25 | \| | \| |  | 2.07 | 25 | \| | \| |  | 2.15 | after |
| 26 |  |  |  | - | 26 |  |  |  | - | after |
