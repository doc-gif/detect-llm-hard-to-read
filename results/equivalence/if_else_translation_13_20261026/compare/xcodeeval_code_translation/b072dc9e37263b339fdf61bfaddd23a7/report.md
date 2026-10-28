# xcodeeval_code_translation/b072dc9e37263b339fdf61bfaddd23a7

- item: xcodeeval_code_translation/b072dc9e37263b339fdf61bfaddd23a7
- transform: if_else_swap (L10)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 13 | 13 | +0 |
| total_tokens | 95 | 97 | +2 |
| mean_entropy | 1.019 | 1.045 | +0.026 |
| ppl | 3.188 | 3.284 | +0.096 |
| su_count_p67 | 14 | 14 | +0 |
| su_count_p80_saved | 11 | 11 | +0 |
| lm_cc_p67 | 15.400 | 15.400 | +0.000 |
| lm_cc_p80_saved | 11.400 | 11.400 | +0.000 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `k, a, b = list(map(lambda x: int(x), input().split()))` | 5.15 | 1 | \| | \| | `k, a, b = list(map(lambda x: int(x), input().split()))` | 5.15 | before |
| 2 | \| | \| | `r = 0` | 2.87 | 2 | \| | \| | `r = 0` | 2.87 | before |
| 3 | \| | \| | `aa = b // k` | 3.00 | 3 | \| | \| | `aa = b // k` | 3.00 | before |
| 4 | \| | \| | `bb = a // k` | 2.59 | 4 | \| | \| | `bb = a // k` | 2.59 | before |
| 5 | \| | \| | `a %= k` | 2.83 | 5 | \| | \| | `a %= k` | 2.83 | before |
| 6 | \| |  | `b %= k` | 0.80 | 6 | \| |  | `b %= k` | 0.80 | before |
| 7 | \| | \| | `r += aa + bb` | 2.59 | 7 | \| | \| | `r += aa + bb` | 2.59 | before |
| 8 | \| | \| | `aa *= k-1` | 2.81 | 8 | \| | \| | `aa *= k-1` | 2.81 | before |
| 9 | \| |  | `bb *= k-1` | 1.15 | 9 | \| |  | `bb *= k-1` | 1.15 | before |
| 10 | \| | \| | `if a <= aa and b <= bb:` | 2.45 | 10 | \| | \| | `if not (a <= aa and b <= bb):` | 2.36 | if_header |
| 11 | \| | \| | `    print(r)` | 1.43 | 13 | \| | \| | `    print(r)` | 1.99 | then_body |
| 12 | \| |  | `else:` | 0.97 | 12 | \| |  | `else:` | 0.77 | between |
| 13 | \| | \| | `    print(-1)` | 2.22 | 11 | \| | \| | `    print(-1)` | 2.22 | else_body |
