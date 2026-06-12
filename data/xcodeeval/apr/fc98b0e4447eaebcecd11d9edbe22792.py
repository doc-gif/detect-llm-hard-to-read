# -*- coding:utf-8 -*-

"""

created by shuangquan.huang at 1/17/20

"""

import collections
import time
import os
import sys
import bisect
import heapq
from typing import List


def solve(N, A, B, K):
    MOD = 1000000007
    
    dp = [0 for _ in range(N+1)]
    dp[A] = 1
    for k in range(1, K+1):
        delta = []
        for x in range(1, N+1):
            d = abs(x-B)
            if d <= 1:
                continue
            l, r = max(x-d+1, 1), min(x+d, N+1)
            if l < x:
                delta.append((l, dp[x]))
                delta.append((x, -dp[x]))
            if x < r:
                delta.append((x+1, dp[x]))
                delta.append((r, -dp[x]))
        
        delta.sort()
        
        ndp = [0 for _ in range(N+1)]
        v = 0
        for x, d in delta:
            v += d
            v %= MOD
            if x <= N:
                ndp[x] = v
        
        dp = ndp
    
    return sum(dp) % MOD


N, A, B, K = map(int, input().split())
print(solve(N, A, B, K))