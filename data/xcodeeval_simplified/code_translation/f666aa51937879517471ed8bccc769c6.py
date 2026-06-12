L1, R1, L2, R2, K = map(int, input().split())
overlap_start = max(L1, L2)
overlap_end = min(R1, R2)
if overlap_start <= overlap_end:
    ans = overlap_end - overlap_start + 1
    if overlap_start <= K <= overlap_end:
        ans -= 1
else:
    ans = 0
print(ans)