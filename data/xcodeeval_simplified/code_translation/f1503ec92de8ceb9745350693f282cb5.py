import math
data = input().split()
N, K = int(data[0]), int(data[1])
if K <= math.ceil(N / 2):
    print(K + (K - 1))
else:
    if K == N and K % 2 != 0:
        print(K - 1)
    elif (N % 2 != 0 and K % 2 == 0) or (N % 2 != 0 and K % 2 != 0):
        print((K - (N - K)) - 1)
    else:
        print(K - (N - K))