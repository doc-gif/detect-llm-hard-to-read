import sys
sys.setrecursionlimit(1000000)
INF = 10**10
YES = "YES"
NO = "NO"
ng = set()
def dfs(s, target):
    if s == target:
        return True
    n = int(s)
    if n in ng:
        return False
    if len(s) > 100:
        return False
    ng.add(n)
    for s1 in [str(int(s[::-1])), (s + "1")[::-1]]:
        if s1 in ng:
            continue
        if dfs(s1, target):
            return True
    return False
def solve(X, Y):
    if X == Y:
        return YES
    SX = bin(X)[2:]
    SY = bin(Y)[2:]
    if dfs(SX, SY):
        return YES
    return NO
def main():
    X, Y = map(int, sys.stdin.readline().split())
    print(solve(X, Y))
if __name__ == "__main__":
    main()