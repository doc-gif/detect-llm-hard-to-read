n, p, k = map(int, input().split())
s = p + k
t = p - k
if s >= n and t <= 1:
    for i in range(1, p):
        print(i, end=" ")
    print(f"({p})", end=" ")
    for i in range(p + 1, n + 1):
        print(i, end=" ")
if s >= n and t > 1:
    print("<<", end=" ")
    for i in range(t, p):
        print(i, end=" ")
    print(f"({p})", end=" ")
    for i in range(p + 1, n + 1):
        print(i, end=" ")
if s < n and t <= 1:
    for i in range(1, p):
        print(i, end=" ")
    print(f"({p})", end=" ")
    for i in range(p + 1, s + 1):
        print(i, end=" ")
    print(">>", end=" ")
if s < n and t > 1:
    print("<<", end=" ")
    for i in range(p - k, p):
        print(i, end=" ")
    print(f"({p})", end=" ")
    for i in range(p + 1, s + 1):
        print(i, end=" ")
    print(">>", end=" ")