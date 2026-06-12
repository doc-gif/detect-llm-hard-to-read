'''input
7
2 3 4 1 6 7 5
'''

def rints():
    return list(map(int, input().split()))

def ri():
    return int(input())

def gcd(a, b):
    if a < b:
        a, b = b, a
    if b == 0:
        return a
    return gcd(b, a % b)

def lcm(xs):
    if not xs:
        return 1
    if len(xs) == 1:
        return x[0]
    if len(xs) == 2:
        return (xs[0] * xs[1]) // gcd(xs[0], xs[1])
    return lcm(xs[:-2] + [lcm([xs[-2], xs[-1]])])

def dfs_cycle_length(arr, u, visited, origin):
    visited.add(u)
    nxt = arr[u-1]
    if nxt in visited:
        return None if nxt != origin else 1
    tmp = dfs_cycle_length(arr, nxt, visited, origin)
    return None if tmp is None else tmp + 1

def solve(arr):
    cycles = []
    visited = set([])
    for u in range(1, len(arr) + 1):
        if u not in visited:
            length = dfs_cycle_length(arr, u, visited, u)
            if length is None:
                return -1
            cycles.append(length//2 if length % 2 == 0 else length)
    return lcm(cycles)

def main():
    n = ri()
    arr = rints()
    print(solve(arr))

main()
