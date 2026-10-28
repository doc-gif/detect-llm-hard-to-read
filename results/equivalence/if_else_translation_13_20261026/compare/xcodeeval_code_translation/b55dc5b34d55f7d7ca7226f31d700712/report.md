# xcodeeval_code_translation/b55dc5b34d55f7d7ca7226f31d700712

- item: xcodeeval_code_translation/b55dc5b34d55f7d7ca7226f31d700712
- transform: if_else_swap (L13)
- behavior: match
- model: codellama/CodeLlama-7b-hf
- thresholds: {'p67': 0.6813, 'p80_saved': 1.3238}

| 指標 | 変換前 | 変換後 | 差分 |
|---|---|---|---|
| loc | 22 | 22 | +0 |
| total_tokens | 253 | 255 | +2 |
| mean_entropy | 0.937 | 0.965 | +0.028 |
| ppl | 2.685 | 2.750 | +0.065 |
| su_count_p67 | 18 | 19 | +1 |
| su_count_p80_saved | 16 | 16 | +0 |
| lm_cc_p67 | 21.400 | 22.800 | +1.400 |
| lm_cc_p80_saved | 18.800 | 18.800 | +0.000 |

行は元コードの順。`|` = その行の前に SU 境界、maxH = 行内の最大エントロピー。

| 元 | 境界p67 | 境界p80_saved | 変換前 | maxH | 新 | 境界p67 | 境界p80_saved | 変換後 | maxH | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | \| | \| | `def main():` | 4.03 | 1 | \| | \| | `def main():` | 4.03 | before |
| 2 | \| | \| | `    from math import sqrt` | 6.19 | 2 | \| | \| | `    from math import sqrt` | 6.19 | before |
| 3 | \| | \| | `    m, n, k = map(int, input().split())` | 3.77 | 3 | \| | \| | `    m, n, k = map(int, input().split())` | 3.77 | before |
| 4 | \| | \| | `    if n < m:` | 4.68 | 4 | \| | \| | `    if n < m:` | 4.68 | before |
| 5 | \| | \| | `        n, m = m, n` | 2.03 | 5 | \| | \| | `        n, m = m, n` | 2.03 | before |
| 6 | \| | \| | `    lo, hi = 1, k + 1` | 4.29 | 6 | \| | \| | `    lo, hi = 1, k + 1` | 4.29 | before |
| 7 | \| | \| | `    while lo + 1 < hi:` | 1.47 | 7 | \| | \| | `    while lo + 1 < hi:` | 1.47 | before |
| 8 | \| | \| | `        mid = (lo + hi) // 2` | 1.76 | 8 | \| | \| | `        mid = (lo + hi) // 2` | 1.76 | before |
| 9 | \| | \| | `        t = mid - 1` | 3.05 | 9 | \| | \| | `        t = mid - 1` | 3.05 | before |
| 10 | \| | \| | `        v = min(int(sqrt(t)), m)` | 3.61 | 10 | \| | \| | `        v = min(int(sqrt(t)), m)` | 3.61 | before |
| 11 | \| | \| | `        tn, tm = (t - 1) // m, t // n` | 3.57 | 11 | \| | \| | `        tn, tm = (t - 1) // m, t // n` | 3.57 | before |
| 12 | \| | \| | `        vv = [t // i for i in range(tm + 1, v + 1)]` | 2.66 | 12 | \| | \| | `        vv = [t // i for i in range(tm + 1, v + 1)]` | 2.66 | before |
| 13 | \| | \| | `        if t // n * (n + m) + sum(vv) * 2 + max(min((tn - tm), len(vv)) * m, 0) - v * v - sum(` | 3.17 | 13 | \| | \| | `        if not (t // n * (n + m) + sum(vv) * 2 + max(min((tn - tm), len(vv)) * m, 0) - v * v - sum(` | 3.18 | if_header |
| 14 | \| | \| | `                vv[:max(min(tn - tm, len(vv)), 0)]) < k:` | 2.61 | 14 | \| | \| | `                vv[:max(min(tn - tm, len(vv)), 0)]) < k):` | 2.54 | if_header |
| 15 |  |  | `            lo = mid` | 0.67 | 17 |  |  | `            lo = mid` | 0.13 | then_body |
| 16 |  |  | `        else:` | 0.24 | 16 |  |  | `        else:` | 0.21 | between |
| 17 |  |  | `            hi = mid` | 0.11 | 15 | \| |  | `            hi = mid` | 0.73 | else_body |
| 18 | \| | \| | `    print(lo)` | 1.83 | 18 | \| | \| | `    print(lo)` | 1.85 | after |
| 19 |  |  |  | 0.45 | 19 |  |  |  | 0.46 | after |
| 20 |  |  |  | 0.54 | 20 |  |  |  | 0.52 | after |
| 21 | \| |  | `if __name__ == '__main__':` | 0.96 | 21 | \| |  | `if __name__ == '__main__':` | 0.96 | after |
| 22 | \| |  | `    main()` | 1.26 | 22 | \| |  | `    main()` | 1.29 | after |
| 23 |  |  |  | - | 23 |  |  |  | - | after |
