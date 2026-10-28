# xcodeeval_code_translation/dae6d6e41bc2c3062a445566c056ffbf

- item: xcodeeval_code_translation/dae6d6e41bc2c3062a445566c056ffbf
- transform: if_else_swap (L19)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 22 | 22 | +0 |
| total_tokens | 260 | 261 | +1 |
| mean_entropy | 0.627 | 0.632 | +0.005 |
| ppl | 1.881 | 1.925 | +0.044 |
| su_count_p67 | 22 | 23 | +1 |
| su_count_p80_saved | 17 | 17 | +0 |
| lm_cc_p67 | 26.400 | 28.000 | +1.600 |
| lm_cc_p80_saved | 20.000 | 20.000 | +0.000 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `pairs = []` | 4.19 | 1 | \| | \| | `pairs = []` | 4.19 | before |
| 2 | \| | \| | `for i in range (8):` | 2.92 | 2 | \| | \| | `for i in range (8):` | 2.92 | before |
| 3 | \| | \| | `  tmp = list (map (int, input().split()))` | 3.45 | 3 | \| | \| | `  tmp = list (map (int, input().split()))` | 3.45 | before |
| 4 | \| | \| | `  pairs.append (tmp)` | 1.90 | 4 | \| | \| | `  pairs.append (tmp)` | 1.90 | before |
| 5 | \| | \| | `pairs.sort ()` | 1.76 | 5 | \| | \| | `pairs.sort ()` | 1.76 | before |
| 6 | \| | \| |  | 3.73 | 6 | \| | \| |  | 3.73 | before |
| 7 | \| | \| | `def judge ():` | 5.66 | 7 | \| | \| | `def judge ():` | 5.66 | before |
| 8 | \| | \| | `  return (pairs[0][0] < pairs[3][0] < pairs[5][0] and` | 4.42 | 8 | \| | \| | `  return (pairs[0][0] < pairs[3][0] < pairs[5][0] and` | 4.42 | before |
| 9 | \| | \| | `          pairs[0][1] < pairs[1][1] < pairs[2][1] and` | 1.52 | 9 | \| | \| | `          pairs[0][1] < pairs[1][1] < pairs[2][1] and` | 1.52 | before |
| 10 | \| | \| | `          pairs[0][0] == pairs[1][0] == pairs[2][0] and` | 1.72 | 10 | \| | \| | `          pairs[0][0] == pairs[1][0] == pairs[2][0] and` | 1.72 | before |
| 11 | \| | \| | `          pairs[3][0] == pairs[4][0] and` | 1.45 | 11 | \| | \| | `          pairs[3][0] == pairs[4][0] and` | 1.45 | before |
| 12 | \| |  | `          pairs[5][0] == pairs[6][0] == pairs[7][0] and` | 1.15 | 12 | \| |  | `          pairs[5][0] == pairs[6][0] == pairs[7][0] and` | 1.15 | before |
| 13 | \| | \| | `          pairs[0][1] == pairs[5][1] and` | 1.64 | 13 | \| | \| | `          pairs[0][1] == pairs[5][1] and` | 1.64 | before |
| 14 | \| |  | `          pairs[1][1] == pairs[6][1] and` | 1.20 | 14 | \| |  | `          pairs[1][1] == pairs[6][1] and` | 1.20 | before |
| 15 | \| |  | `          pairs[2][1] == pairs[7][1] and` | 0.73 | 15 | \| |  | `          pairs[2][1] == pairs[7][1] and` | 0.73 | before |
| 16 | \| | \| | `          pairs[0][1] == pairs[3][1] and` | 1.75 | 16 | \| | \| | `          pairs[0][1] == pairs[3][1] and` | 1.75 | before |
| 17 | \| |  | `          pairs[2][1] == pairs[4][1])` | 1.24 | 17 | \| |  | `          pairs[2][1] == pairs[4][1])` | 1.24 | before |
| 18 | \| |  |  | 0.87 | 18 | \| |  |  | 0.87 | before |
| 19 | \| | \| | `if judge ():` | 3.01 | 19 | \| | \| | `if not judge ():` | 3.01 | if_header |
| 20 | \| | \| | `  print ('respectable')` | 3.16 | 22 | \| | \| | `  print ('respectable')` | 2.92 | then_body |
| 21 |  |  | `else:` | 0.50 | 21 | \| |  | `else:` | 1.05 | between |
| 22 | \| | \| | `  print ('ugly')` | 3.27 | 20 | \| | \| | `  print ('ugly')` | 2.90 | else_body |
| 23 |  |  |  | - | 23 |  |  |  | - | after |
