w1, h1, w2, h2 = map(int, input().split())
ans = (w1 + 2) + h1 + (h2 + 1) + (w2 + 1) + h2 + h1 + w1 - w2
print(ans)
