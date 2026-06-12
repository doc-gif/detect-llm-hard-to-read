import sys
sys.setrecursionlimit(10**7)
RI = lambda: list(map(int, input().split()))
RS = lambda: input().rstrip().split()
s = input().rstrip()
s = s[0] + s[1:-1].replace("dot", ".") + s[-1]
s = s[0] + s[1:-1].replace("at", "@", 1) + s[-1]
print(s)