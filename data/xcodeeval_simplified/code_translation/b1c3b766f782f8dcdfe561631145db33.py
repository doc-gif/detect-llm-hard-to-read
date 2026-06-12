n, k = map(int, input().split())
k = 10**k
product = n * k
original_product = product
while n * k > 0:
    if n > k:
        n %= k
    else:
        k %= n
result = original_product // (n + k)
print(result)