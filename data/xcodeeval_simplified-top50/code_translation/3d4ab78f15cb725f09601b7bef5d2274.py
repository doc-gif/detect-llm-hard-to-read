def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a
def lcm(a, b):
    return int(a * b / gcd(a, b))
def run(n, crush):
    visited = [False] * n
    cycle_size = 1
    for i in range(n):
        if visited[i]:
            continue
        x = i
        length = 0
        while not visited[x]:
            visited[x] = True
            x = crush[x] - 1
            length += 1
        if x != i:
            return -1
        if length % 2 == 0:
            length //= 2
        cycle_size = lcm(cycle_size, length)
    return cycle_size
n = int(input())
crush = [int(x) for x in input().split()]
print(run(n, crush))