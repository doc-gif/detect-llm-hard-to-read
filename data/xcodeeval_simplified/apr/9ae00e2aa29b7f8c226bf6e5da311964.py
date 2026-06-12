from sys import stdin, stdout
from collections import defaultdict
from math import sqrt, log10, gcd

mod = 10**9 + 7


def ncr(n, r, p=mod):
    num = den = 1
    for i in range(r):
        num = (num * (n - i)) % p
        den = (den * (i + 1)) % p
    return (num * pow(den, p - 2, p)) % p


def normalncr(n, r):
    r = min(r, n - r)
    count = 1
    for i in range(n - r, n + 1):
        count *= i
    for i in range(1, r + 1):
        count //= i
    return count


inf = float("inf")
adj = defaultdict(set)
visited = defaultdict(int)


def addedge(a, b):
    adj[a].add(b)
    adj[b].add(a)


def bfs(v):
    from queue import Queue

    q = Queue()
    q.put(v)
    visited[v] = 1
    while q.qsize() > 0:
        s = q.get_nowait()
        print(s)
        for i in adj[s]:
            if visited[i] == 0:
                q.put(i)
                visited[i] = 1


def dfs(v, visited):
    if visited[v] == 1:
        return
    visited[v] = 1
    print(v)
    for i in adj[v]:
        dfs(i, visited)


def reverse_bisect_right(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError("lo must be non-negative")
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x > a[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo


def reverse_bisect_left(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError("lo must be non-negative")
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x >= a[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo


def get_list():
    return list(map(int, input().split()))


def get_str_list_in_int():
    return [int(i) for i in list(input())]


def get_str_list():
    return list(input())


def get_map():
    return map(int, input().split())


def input_int():
    return int(input())


def matrix(a, b):
    return [[0 for _ in range(b)] for _ in range(a)]


def swap(a, b):
    return b, a


def find_gcd(l):
    a = l[0]
    for i in range(len(l)):
        a = gcd(a, l[i])
    return a


def is_prime(n):
    sqrta = int(sqrt(n))
    for i in range(2, sqrta + 1):
        if n % i == 0:
            return 0
    return 1


def prime_factors(n):
    while n % 2 == 0:
        return [2] + prime_factors(n // 2)
    sqrta = int(sqrt(n))
    for i in range(3, sqrta + 1, 2):
        if n % i == 0:
            return [i] + prime_factors(n // i)
    return [n]


def p(a):
    if isinstance(a, str):
        print(a + "\n")
    else:
        print(str(a) + "\n")


def ps(a):
    if isinstance(a, str):
        print(a)
    else:
        print(str(a))


def kth_no_not_div_by_n(n, k):
    return k + (k - 1) // (n - 1)


def forward_array(l):
    n = len(l)
    stack = []
    forward = [0] * n
    for i in range(n - 1, -1, -1):
        while stack and l[stack[-1]] < l[i]:
            stack.pop()
        forward[i] = stack[-1] if stack else n
        stack.append(i)
    return forward


def backward_array(l):
    n = len(l)
    stack = []
    backward = [0] * n
    for i in range(n):
        while stack and l[stack[-1]] < l[i]:
            stack.pop()
        backward[i] = stack[-1] if stack else -1
        stack.append(i)
    return backward


def char(a):
    return chr(a + 97)


def get_length(a):
    return 1 + int(log10(a))


nc = "NO"
yc = "YES"
ns = "No"
ys = "Yes"


def issq(n):
    sqrta = int(n**0.5)
    return sqrta**2 == n


for _ in range(int(input())):
    n, k = get_map()
    print(pow(n, k, mod))
print(1)
