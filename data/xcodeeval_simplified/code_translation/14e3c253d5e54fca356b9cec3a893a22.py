N = int(input())
n = list(map(int, input().split()))
if N == 1:
    ans = [0, n[0]]
elif N == 2:
    ans = [min(n), max(n)]
else:
    n.reverse()
    first = max(n[0], n[1])
    second = n[0] + n[1]
    for i in range(2, N):
        first = max(n[i] + second - first, first)
        second += n[i]
    ans = [second - first, first]
print(" ".join(map(str, ans)))