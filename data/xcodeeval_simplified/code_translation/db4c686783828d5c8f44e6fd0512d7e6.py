a, b = map(int, input().split())
a, b = min(a, b), max(a, b)
if b % a == 0:
    print(0)
    exit(0)
x = b - a
divisors = set()
for i in range(1, int(x**0.5) + 1):
    if x % i == 0:
        divisors.add(i)
        divisors.add(x // i)
min_diff = 10**20
for d in divisors:
    if d >= a:
        min_diff = min(min_diff, d - a)
print(min((x % a - a) % x, min_diff))