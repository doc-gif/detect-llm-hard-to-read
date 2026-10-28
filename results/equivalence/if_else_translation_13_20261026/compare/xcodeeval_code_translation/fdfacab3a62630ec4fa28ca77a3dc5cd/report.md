# xcodeeval_code_translation/fdfacab3a62630ec4fa28ca77a3dc5cd

- item: xcodeeval_code_translation/fdfacab3a62630ec4fa28ca77a3dc5cd
- transform: if_else_swap (L9)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 25 | 25 | +0 |
| total_tokens | 227 | 228 | +1 |
| mean_entropy | 0.710 | 0.795 | +0.085 |
| ppl | 1.903 | 2.043 | +0.140 |
| su_count_p67 | 21 | 24 | +3 |
| su_count_p80_saved | 15 | 20 | +5 |
| lm_cc_p67 | 27.400 | 33.000 | +5.600 |
| lm_cc_p80_saved | 16.800 | 24.800 | +8.000 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `import math` | 3.58 | 1 | \| | \| | `import math` | 3.58 | before |
| 2 | \| | \| | `s = input()` | 2.73 | 2 | \| | \| | `s = input()` | 2.73 | before |
| 3 | \| | \| | `n = int(s.split()[0])` | 4.36 | 3 | \| | \| | `n = int(s.split()[0])` | 4.36 | before |
| 4 | \| | \| | `k = int(s.split()[1])` | 3.43 | 4 | \| | \| | `k = int(s.split()[1])` | 3.43 | before |
| 5 | \| | \| | `st = input()` | 4.23 | 5 | \| | \| | `st = input()` | 4.23 | before |
| 6 | \| | \| | `i = 1` | 4.66 | 6 | \| | \| | `i = 1` | 4.66 | before |
| 7 | \| | \| | `arr = list(map(int, st.split()))` | 4.45 | 7 | \| | \| | `arr = list(map(int, st.split()))` | 4.45 | before |
| 8 | \| | \| | `j = (sum(arr) + k * i)/(len(arr) + i)` | 3.63 | 8 | \| | \| | `j = (sum(arr) + k * i)/(len(arr) + i)` | 3.63 | before |
| 9 | \| | \| | `if(j-math.trunc(j)>=0.5):` | 3.19 | 9 | \| | \| | `if not (j-math.trunc(j)>=0.5):` | 3.19 | if_header |
| 10 | \| | \| | `    j = math.ceil(j)` | 1.95 | 12 | \| |  | `    j = math.ceil(j)` | 1.00 | then_body |
| 11 |  |  | `else:` | 0.58 | 11 | \| | \| | `else:` | 2.62 | between |
| 12 | \| |  | `    j = math.trunc(j)` | 0.75 | 10 | \| | \| | `    j = math.trunc(j)` | 2.55 | else_body |
| 13 | \| | \| | `if(j == k):` | 3.47 | 13 | \| | \| | `if(j == k):` | 3.43 | after |
| 14 | \| | \| | `    print(0)` | 2.61 | 14 | \| | \| | `    print(0)` | 2.62 | after |
| 15 | \| |  | `else:` | 1.21 | 15 | \| |  | `else:` | 1.20 | after |
| 16 | \| | \| | `    while(True):` | 3.35 | 16 | \| | \| | `    while(True):` | 3.29 | after |
| 17 | \| | \| | `        j = (sum(arr) + k * i)/(len(arr) + i)` | 2.80 | 17 | \| | \| | `        j = (sum(arr) + k * i)/(len(arr) + i)` | 2.80 | after |
| 18 | \| |  | `        if(j-math.trunc(j)>=0.5):` | 0.96 | 18 | \| | \| | `        if(j-math.trunc(j)>=0.5):` | 1.95 | after |
| 19 |  |  | `            j = math.ceil(j)` | 0.23 | 19 | \| |  | `            j = math.ceil(j)` | 0.75 | after |
| 20 |  |  | `        else:` | 0.19 | 20 | \| |  | `        else:` | 1.15 | after |
| 21 |  |  | `            j = math.trunc(j)` | 0.15 | 21 |  |  | `            j = math.trunc(j)` | 0.23 | after |
| 22 | \| |  | `        if(j == k):` | 1.31 | 22 | \| | \| | `        if(j == k):` | 1.55 | after |
| 23 | \| |  | `            print(i)` | 1.32 | 23 | \| | \| | `            print(i)` | 1.33 | after |
| 24 |  |  | `            break` | 0.33 | 24 |  |  | `            break` | 0.31 | after |
| 25 | \| |  | `        i += 1` | 1.28 | 25 | \| | \| | `        i += 1` | 1.33 | after |
| 26 |  |  |  | - | 26 |  |  |  | - | after |
