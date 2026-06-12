import sys

input = lambda: sys.stdin.readline().rstrip()
T = int(input())


def dfs(keys, depth, remaining_value, remaining_count):
    if depth == len(keys):
        return False
    key = keys[depth]
    for c in range(remaining_count + 1):
        new_value = remaining_value - key * c
        if new_value < 0:
            return False
        elif new_value == 0 and remaining_count - c == 0:
            return True
        else:
            if depth == len(keys):
                return False
            else:
                if dfs(keys, depth + 1, new_value, remaining_count - c):
                    return True


for _ in range(T):
    n, m, k = map(int, input().split())
    if n % 2 == 0 and m % 2 == 0:
        print("YES" if k % 2 == 0 else "NO")
    else:
        if m % 2 == 0:
            n, m = m, n
        else:
            k = (n * m) // 2 - k
        keys = list(range(1, m + 1, 2))
        if dfs(keys, 0, k, n // 2):
            print("YES")
        else:
            print("NO")
