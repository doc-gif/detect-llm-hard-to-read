import math
def find(n, k, length):
    if k < n:
        return [k]
    max_val = 0
    index = 1
    for i in range(1, length + 1):
        temp = k % (10**i)
        if temp >= n:
            break
        if temp >= 10 ** (i - 1):
            max_val = temp
            index = i
    remainder = k - max_val
    remainder = remainder // (10**index)
    return find(n, remainder, length) + [max_val]
n = int(input())
k = int(input())
length = int(math.log(n - 1, 10)) + 1
ANS = find(n, k, length)[::-1]
ans = 0
temp = 1
for i in range(len(ANS)):
    ans += ANS[i] * temp
    temp *= n
print(ans)