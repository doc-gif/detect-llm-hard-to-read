import time
import random
W = int(input())
M = [int(x) for x in input().split()]
A = [0] * 8
start_time = time.time()
current_sum = 0
min_diff = 10**20
for i in range(8):
    weight = i + 1
    if current_sum + M[i] * weight <= W:
        current_sum += M[i] * weight
        A[i] = M[i]
    else:
        t = (W - current_sum) // weight
        current_sum += t * weight
        A[i] += t
    if current_sum <= W:
        min_diff = min(min_diff, W - current_sum)
while time.time() - start_time < 1.7:
    i = random.randrange(8)
    a = random.randrange(2)
    weight = i + 1
    if W - current_sum >= 20 or (current_sum - W < 10 and a == 0):
        if A[i] < M[i]:
            A[i] += 1
            current_sum += weight
    else:
        if A[i] > 0:
            A[i] -= 1
            current_sum -= weight
    if current_sum <= W:
        min_diff = min(min_diff, W - current_sum)
print(W - min_diff)