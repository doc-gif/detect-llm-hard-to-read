# HumanEval_126__ifelse_L10 変換前後の比較

- item: HumanEval_126__ifelse_L10
- transform: if_else_swap (L10: all(lst[i - 1] <= lst[i] for i in range(1, len(lst))) → not all(lst[i - 1] <= lst[i] for i in range(1, len(lst))))
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80': 1.2515}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 13 | 13 | +0 |
| total_tokens | 116 | 117 | +1 |
| mean_entropy | 0.770 | 0.771 | +0.001 |
| ppl | 2.235 | 2.256 | +0.021 |
| su_count_p67 | 11 | 10 | -1 |
| su_count_p80 | 8 | 8 | +0 |
| lm_cc_p67 | 10.200 | 8.600 | -1.600 |
| lm_cc_p80 | 7.000 | 7.000 | +0.000 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80 | 変換前 | maxH | 新 | 境界p67 | 境界p80 | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `from typing import *` | 4.96 | 1 | \| | \| | `from typing import *` | 4.96 | before |
| 2 | \| |  |  | 0.70 | 2 | \| |  |  | 0.70 | before |
| 3 | \| | \| |  | 1.79 | 3 | \| | \| |  | 1.79 | before |
| 4 | \| | \| | `def is_sorted(lst):` | 6.34 | 4 | \| | \| | `def is_sorted(lst):` | 6.34 | before |
| 5 | \| | \| | `    count_digit = dict([(i, 0) for i in lst])` | 4.68 | 5 | \| | \| | `    count_digit = dict([(i, 0) for i in lst])` | 4.68 | before |
| 6 | \| | \| | `    for i in lst:` | 2.24 | 6 | \| | \| | `    for i in lst:` | 2.24 | before |
| 7 | \| |  | `        count_digit[i] += 1` | 0.94 | 7 | \| |  | `        count_digit[i] += 1` | 0.94 | before |
| 8 | \| | \| | `    if any(count_digit[i] > 2 for i in lst):` | 3.15 | 8 | \| | \| | `    if any(count_digit[i] > 2 for i in lst):` | 3.15 | before |
| 9 |  |  | `        return False` | 0.30 | 9 |  |  | `        return False` | 0.30 | before |
| 10 | \| | \| | `    if all(lst[i - 1] <= lst[i] for i in range(1, len(lst))):` | 2.77 | 10 | \| | \| | `    if not all(lst[i - 1] <= lst[i] for i in range(1, len(lst))):` | 2.77 | if_header |
| 11 |  |  | `        return True` | 0.18 | 13 |  |  | `        return True` | 0.19 | then_body |
| 12 | \| |  | `    else:` | 1.16 | 12 |  |  | `    else:` | 0.59 | between |
| 13 |  |  | `        return False` | 0.24 | 11 |  |  | `        return False` | 0.09 | else_body |
| 14 |  |  |  | - | 14 |  |  |  | - | after |
