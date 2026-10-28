# xcodeeval_code_translation/3b399bc13f31d7ac665a906c006042f4

- item: xcodeeval_code_translation/3b399bc13f31d7ac665a906c006042f4
- transform: if_else_swap (L2)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 10 | 10 | +0 |
| total_tokens | 120 | 122 | +2 |
| mean_entropy | 0.830 | 0.849 | +0.018 |
| ppl | 2.403 | 2.685 | +0.281 |
| su_count_p67 | 10 | 10 | +0 |
| su_count_p80_saved | 8 | 8 | +0 |
| lm_cc_p67 | 11.000 | 10.400 | -0.600 |
| lm_cc_p80_saved | 7.200 | 7.400 | +0.200 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `n, m, k = map(int, input().split())` | 4.15 | 1 | \| | \| | `n, m, k = map(int, input().split())` | 4.15 | before |
| 2 | \| | \| | `if k <= n - 1:` | 2.80 | 2 | \| | \| | `if not (k <= n - 1):` | 2.80 | if_header |
| 3 | \| | \| | `    print(1 + k, 1)` | 2.25 | 9 | \| | \| | `    print(1 + k, 1)` | 1.66 | then_body |
| 4 | \| |  | `else:` | 1.18 | 8 | \| |  | `else:` | 0.98 | between |
| 5 | \| | \| | `    k = k - n` | 3.64 | 3 | \| |  | `    k = k - n` | 1.28 | else_body |
| 6 | \| | \| | `    if (n - k // (m - 1)) % 2 == 0:` | 3.12 | 4 | \| | \| | `    if (n - k // (m - 1)) % 2 == 0:` | 3.01 | else_body |
| 7 | \| | \| | `        print((n - k // (m - 1)), 2 + k % (m - 1))` | 2.03 | 5 | \| | \| | `        print((n - k // (m - 1)), 2 + k % (m - 1))` | 1.80 | else_body |
| 8 |  |  | `    else:` | 0.42 | 6 |  |  | `    else:` | 0.46 | else_body |
| 9 | \| |  | `        print((n - k // (m - 1)), m - k % (m - 1))` | 1.25 | 7 | \| | \| | `        print((n - k // (m - 1)), m - k % (m - 1))` | 1.53 | else_body |
| 10 | \| | \| |  | 1.92 | 10 | \| | \| |  | 1.93 | after |
