
M = 998244353

MAXNUM = 260
factor = [1]*(MAXNUM+2)
factor[-1]=0
storecomb = {}


for i in range(1,MAXNUM+1):
    factor[i] = (factor[i-1]*i)%M

def fastfrac(a,b):
    numb = pow(b,M-2,M)
    return ((a%M)*(numb%M))%M

def comb(n,k):
#    print "*",n,k
    if n<k: return 0
    if n==k: return 1
    if (n,k) in storecomb:  return storecomb[(n,k)]

    num1 = factor[n]
    num2 = factor[k]
    num3 = factor[n-k]
    num = (num2*num3)%M
    output = fastfrac(num1,num)
    storecomb[(n,k)] = output
    return output

dic = {}

def getpow(i,j,M):
    if (i,j) in dic: return dic[(i,j)]
    else:
        dic[(i,j)] = pow(i,j,M)
        return dic[(i,j)]



def main(t):

    n,k = map(int,input().split())

    dp = [[0 for q in range(k+1)] for p in range(n+1)]
    
    for j in range(1,k+1):
        dp[2][j] = 1
        dp[1][j] = 1


    for i in range(3,n+1):
        for j in range(1,k+1):
            dp[i][j] = getpow(k-j+1,(i-1)*(i-2)//2,M)





    for i in range(3,n+1): 

        for same in range(1,i-1):

            part1 = 0
            for j in range(2,k+1):



                part1 = (part1 + dp[i-same][j-1])%M
                part2 = ( getpow(k-j+1,same*(i-1-same)+same*(same-1)//2,M) * comb(i-1,same) ) %M

                dp[i][j] += (part1*part2)%M
                
                dp[i][j] %= M 

#    print(dp)

#    print(dp[n])
    print(sum(dp[n])%M)

            
   


































T = 1 #int(input())
t = 1
while t<=T:
    main(t)
    t += 1
