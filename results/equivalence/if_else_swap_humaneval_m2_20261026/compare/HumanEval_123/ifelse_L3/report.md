# HumanEval_123__ifelse_L3 変換前後の比較

- item: HumanEval_123__ifelse_L3
- transform: if_else_swap (L3: n%2==0 → not (n%2==0))
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80': 1.2515}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 16 | 16 | +0 |
| total_tokens | 124 | 126 | +2 |
| mean_entropy | 0.777 | 0.799 | +0.022 |
| ppl | 2.446 | 2.484 | +0.039 |
| su_count_p67 | 15 | 15 | +0 |
| su_count_p80 | 11 | 10 | -1 |
| lm_cc_p67 | 19.400 | 19.400 | +0.000 |
| lm_cc_p80 | 13.800 | 12.000 | -1.800 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80 | 変換前 | maxH | 新 | 境界p67 | 境界p80 | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `from typing import *` | 4.96 | 1 | \| | \| | `from typing import *` | 4.96 | before |
| 2 | \| | \| | `def get_odd_collatz(n):` | 7.03 | 2 | \| | \| | `def get_odd_collatz(n):` | 7.03 | before |
| 3 | \| | \| | `    if n%2==0:` | 3.98 | 3 | \| | \| | `    if not (n%2==0):` | 3.98 | if_header |
| 4 | \| | \| | `        odd_collatz = [] ` | 2.50 | 6 | \| | \| | `        odd_collatz = [] ` | 1.27 | then_body |
| 5 | \| | \| | `    else:` | 1.45 | 5 | \| |  | `    else:` | 0.86 | between |
| 6 | \| | \| | `        odd_collatz = [n]` | 1.31 | 4 | \| | \| | `        odd_collatz = [n]` | 2.18 | else_body |
| 7 | \| | \| | `    while n > 1:` | 2.02 | 7 | \| | \| | `    while n > 1:` | 2.06 | after |
| 8 | \| |  | `        if n % 2 == 0:` | 1.13 | 8 | \| |  | `        if n % 2 == 0:` | 1.23 | after |
| 9 | \| | \| | `            n = n/2` | 1.37 | 9 | \| | \| | `            n = n/2` | 1.45 | after |
| 10 | \| |  | `        else:` | 0.78 | 10 | \| |  | `        else:` | 0.76 | after |
| 11 | \| |  | `            n = n*3 + 1` | 1.07 | 11 | \| |  | `            n = n*3 + 1` | 1.05 | after |
| 12 |  |  |  | 0.43 | 12 |  |  |  | 0.37 | after |
| 13 | \| | \| | `        if n%2 == 1:` | 1.62 | 13 | \| | \| | `        if n%2 == 1:` | 1.73 | after |
| 14 |  |  | `            odd_collatz.append(int(n))` | 0.41 | 14 |  |  | `            odd_collatz.append(int(n))` | 0.37 | after |
| 15 | \| | \| |  | 1.49 | 15 | \| | \| |  | 1.51 | after |
| 16 | \| |  | `    return sorted(odd_collatz)` | 0.74 | 16 | \| |  | `    return sorted(odd_collatz)` | 0.81 | after |
| 17 |  |  |  | - | 17 |  |  |  | - | after |
