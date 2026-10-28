# HumanEval_47__ifelse_L4 変換前後の比較

- item: HumanEval_47__ifelse_L4
- transform: if_else_swap (L4: len(l) % 2 == 1 → not (len(l) % 2 == 1))
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80': 1.2515}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 7 | 7 | +0 |
| total_tokens | 85 | 87 | +2 |
| mean_entropy | 0.580 | 0.607 | +0.026 |
| ppl | 1.765 | 1.983 | +0.217 |
| su_count_p67 | 8 | 6 | -2 |
| su_count_p80 | 5 | 6 | +1 |
| lm_cc_p67 | 9.200 | 5.800 | -3.400 |
| lm_cc_p80 | 4.200 | 5.800 | +1.600 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80 | 変換前 | maxH | 新 | 境界p67 | 境界p80 | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `from typing import *` | 4.96 | 1 | \| | \| | `from typing import *` | 4.96 | before |
| 2 | \| | \| | `def median(l: list):` | 6.43 | 2 | \| | \| | `def median(l: list):` | 6.43 | before |
| 3 | \| | \| | `    l = sorted(l)` | 2.69 | 3 | \| | \| | `    l = sorted(l)` | 2.69 | before |
| 4 | \| | \| | `    if len(l) % 2 == 1:` | 2.68 | 4 | \| | \| | `    if not (len(l) % 2 == 1):` | 2.68 | if_header |
| 5 | \| |  | `        return l[len(l) // 2]` | 0.85 | 7 |  |  | `        return l[len(l) // 2]` | 0.34 | then_body |
| 6 | \| |  | `    else:` | 0.81 | 6 |  |  | `    else:` | 0.66 | between |
| 7 | \| |  | `        return (l[len(l) // 2 - 1] + l[len(l) // 2]) / 2.0` | 1.20 | 5 | \| | \| | `        return (l[len(l) // 2 - 1] + l[len(l) // 2]) / 2.0` | 2.06 | else_body |
| 8 |  |  |  | - | 8 |  |  |  | - | after |
