n = int(input())
dice1 = [int(i) for i in input().split()]
dice2 = [int(i) for i in input().split()]
dice3 = [int(i) for i in input().split()]
h = [0] * 100000
for i in dice1:
    h[i] += 1
    for j in dice2:
        h[j] += 1
        for k in dice3:
            h[k] += 1
            h[i * 10 + j] += 1
            h[j * 10 + i] += 1
            h[i * 10 + k] += 1
            h[k * 10 + i] += 1
            h[k * 10 + j] += 1
            h[j * 10 + k] += 1
            h[i * 100 + j * 10 + k] += 1
            h[i * 100 + k * 10 + j] += 1
            h[k * 100 + i * 10 + j] += 1
            h[k * 100 + j * 10 + i] += 1
            h[j * 100 + i * 10 + k] += 1
            h[j * 100 + k * 10 + i] += 1
h = h[1:]
print(len(h[: h.index(0)]))
