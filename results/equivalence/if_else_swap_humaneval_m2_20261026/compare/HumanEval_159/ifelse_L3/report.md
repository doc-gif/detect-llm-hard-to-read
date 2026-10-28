# HumanEval_159__ifelse_L3 変換前後の比較

- item: HumanEval_159__ifelse_L3
- transform: if_else_swap (L3: (need <= remaining) →  not (need <= remaining))
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80': 1.2515}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 6 | 6 | +0 |
| total_tokens | 50 | 51 | +1 |
| mean_entropy | 1.538 | 1.619 | +0.081 |
| ppl | 6.443 | 7.866 | +1.424 |
| su_count_p67 | 7 | 7 | +0 |
| su_count_p80 | 6 | 7 | +1 |
| lm_cc_p67 | 7.800 | 7.800 | +0.000 |
| lm_cc_p80 | 6.000 | 7.800 | +1.800 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80 | 変換前 | maxH | 新 | 境界p67 | 境界p80 | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `from typing import *` | 4.96 | 1 | \| | \| | `from typing import *` | 4.96 | before |
| 2 | \| | \| | `def eat(number, need, remaining):` | 6.48 | 2 | \| | \| | `def eat(number, need, remaining):` | 6.48 | before |
| 3 | \| | \| | `    if(need <= remaining):` | 3.39 | 3 | \| | \| | `    if not (need <= remaining):` | 3.39 | if_header |
| 4 | \| | \| | `        return [ number + need , remaining-need ]` | 2.40 | 6 | \| | \| | `        return [ number + need , remaining-need ]` | 1.73 | then_body |
| 5 | \| |  | `    else:` | 1.11 | 5 | \| | \| | `    else:` | 2.18 | between |
| 6 | \| | \| | `        return [ number + remaining , 0]` | 1.46 | 4 | \| | \| | `        return [ number + remaining , 0]` | 2.19 | else_body |
| 7 |  |  |  | - | 7 |  |  |  | - | after |
