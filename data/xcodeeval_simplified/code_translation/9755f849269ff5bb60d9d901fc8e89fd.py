n = int(input())
A = list(map(int, input().split()))
A.sort()
median_index = n // 2
print(A[median_index])