# HumanEval_123__ifelse_L8 変換前後の比較

- item: HumanEval_123__ifelse_L8
- transform: if_else_swap (L8: n % 2 == 0 → not (n % 2 == 0))
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80': 1.2515}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 16 | 16 | +0 |
| total_tokens | 124 | 126 | +2 |
| mean_entropy | 0.777 | 0.812 | +0.035 |
| ppl | 2.446 | 2.601 | +0.155 |
| su_count_p67 | 15 | 15 | +0 |
| su_count_p80 | 11 | 11 | +0 |
| lm_cc_p67 | 19.400 | 19.400 | +0.000 |
| lm_cc_p80 | 13.800 | 13.800 | +0.000 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80 | 変換前 | maxH | 新 | 境界p67 | 境界p80 | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `from typing import *` | 4.96 | 1 | \| | \| | `from typing import *` | 4.96 | before |
| 2 | \| | \| | `def get_odd_collatz(n):` | 7.03 | 2 | \| | \| | `def get_odd_collatz(n):` | 7.03 | before |
| 3 | \| | \| | `    if n%2==0:` | 3.98 | 3 | \| | \| | `    if n%2==0:` | 3.98 | before |
| 4 | \| | \| | `        odd_collatz = [] ` | 2.50 | 4 | \| | \| | `        odd_collatz = [] ` | 2.50 | before |
| 5 | \| | \| | `    else:` | 1.45 | 5 | \| | \| | `    else:` | 1.45 | before |
| 6 | \| | \| | `        odd_collatz = [n]` | 1.31 | 6 | \| | \| | `        odd_collatz = [n]` | 1.31 | before |
| 7 | \| | \| | `    while n > 1:` | 2.02 | 7 | \| | \| | `    while n > 1:` | 2.02 | before |
| 8 | \| |  | `        if n % 2 == 0:` | 1.13 | 8 | \| |  | `        if not (n % 2 == 0):` | 1.20 | if_header |
| 9 | \| | \| | `            n = n/2` | 1.37 | 11 | \| |  | `            n = n/2` | 1.25 | then_body |
| 10 | \| |  | `        else:` | 0.78 | 10 | \| |  | `        else:` | 0.92 | between |
| 11 | \| |  | `            n = n*3 + 1` | 1.07 | 9 | \| | \| | `            n = n*3 + 1` | 1.35 | else_body |
| 12 |  |  |  | 0.43 | 12 |  |  |  | 0.41 | after |
| 13 | \| | \| | `        if n%2 == 1:` | 1.62 | 13 | \| | \| | `        if n%2 == 1:` | 1.63 | after |
| 14 |  |  | `            odd_collatz.append(int(n))` | 0.41 | 14 |  |  | `            odd_collatz.append(int(n))` | 0.40 | after |
| 15 | \| | \| |  | 1.49 | 15 | \| | \| |  | 1.52 | after |
| 16 | \| |  | `    return sorted(odd_collatz)` | 0.74 | 16 | \| |  | `    return sorted(odd_collatz)` | 0.74 | after |
| 17 |  |  |  | - | 17 |  |  |  | - | after |
