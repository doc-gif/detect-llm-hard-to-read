n = int(input())
counts = [0, 0, 0, 0, 0]
for _ in range(n):
    a, b = map(int, input().split())
    for value in range(6):
        if a == value:
            counts[value - 1] += 1
        if b == value:
            counts[value - 1] += 1
if counts.count(2) != 5:
    print("WIN")
else:
    print("FAIL")