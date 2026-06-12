import sys
def recur(bnry, prefix_sum, idx):
    if bnry[0] == '1':
        prefix_sum[idx] = 2 * prefix_sum[idx - 1] + 1
    elif bnry[0] == '0':
        prefix_sum[idx] = 2 * prefix_sum[idx - 1]
    bnry = bnry[1:]
    if len(bnry):
        recur(bnry,prefix_sum,idx+1)
    else:
        return 0
def cal(bnry,num, prefix_sum,idx):
    if num == pow(2,idx) - 1:
        if bnry[idx-1] == '1':
            return prefix_sum[idx - 1] * 2 + 1
        else:
            return prefix_sum[idx - 1] * 2
    elif num == pow(2,idx-1):
        if bnry[idx-1] == '1':
            return prefix_sum[idx-1] + 1
        else:
            return prefix_sum[idx-1]
    elif num == pow(2,idx-1) -1:
        return prefix_sum[idx-1]
    if num > pow(2,idx-1):
        if bnry[idx-1] == '1':
            return prefix_sum[idx-1] + 1 + cal(bnry,num - pow(2,idx-1) ,prefix_sum, idx - 1)
        else:
            return prefix_sum[idx-1] + cal(bnry,num - pow(2,idx-1), prefix_sum, idx - 1)
    elif num < pow(2,idx-1):
        return cal(bnry,num,prefix_sum,idx-1)

sys.setrecursionlimit(100000)
n,l,r = list(map(int,input().split(' ')))
bnry = bin(n)
prefix_sum = [0] * 51
if n == 0:
    print(0)
else:
    recur(bnry[2:], prefix_sum, 1)
    print(cal(bnry[2:],r,prefix_sum,len(bnry[2:])) - cal(bnry[2:],l-1,prefix_sum,len(bnry[2:])))