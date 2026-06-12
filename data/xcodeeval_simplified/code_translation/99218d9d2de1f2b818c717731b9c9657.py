n, k = map(int, input().split())
if k > 70:
    print("No")
    exit(0)
remainders = {n % i for i in range(1, k + 1)}
print("Yes" if len(remainders) == k else "No")