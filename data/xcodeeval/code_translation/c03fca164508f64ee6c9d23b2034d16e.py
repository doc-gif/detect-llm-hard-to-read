n,m,c0,d0 = [int(j) for j in input().split()]
nach = []
nach.append([0,0,c0,d0])
for i in range(m):
    nach.append([int(j) for j in input().split()])

profit = []
nabor = [[0] * (m+1) for i in range(n+1)]
profit = [0] * (n+1)
for nn in range(1,n+1):
    for j in range(m+1):
        if nn - nach[j][2] >= 0:
            if (nabor[nn - nach[j][2]][j] + 1) * nach[j][1] <= nach[j][0] and profit[nn-nach[j][2]]+nach[j][3] > profit[nn]:
                profit[nn] = profit[nn-nach[j][2]]+nach[j][3]
                for k in range(m+1):
                    nabor[nn][k] = nabor[nn - nach[j][2]][k]
                nabor[nn][j] += 1
MaxProfit = 0
for i in range(n+1):
    if MaxProfit < profit[i]:
        MaxProfit = profit[i]

print(MaxProfit)