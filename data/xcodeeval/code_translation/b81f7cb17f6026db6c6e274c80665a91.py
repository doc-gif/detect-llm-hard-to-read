n = int(input())
k=0
for i in [100, 20, 10, 5]:
    k = k + n // i
    n = n % i
print(k + n)