def getAllFactors(x): #returns a sorted list of all the factors or divisors of x (including 1 and x)
    factors=[]
    for i in range(1,int(x**0.5)+1):
        if x%i==0:
            factors.append(i)
            if x//i!=i:
                factors.append(x//i)
    return sorted(factors)

def main():
    
    MOD=998244353
    
    n=int(input())
    dp=[0]*(n+1)
    dp[1]=1
    prefixSum=1
    for i in range(2,n+1):
        dp[i]=prefixSum+2
        # add 1 for every factor excluding 1 and n
        factors=getAllFactors(i)
        dp[i]+=(len(factors)-2)
        dp[i]%=MOD
        prefixSum+=dp[i]
        prefixSum%=MOD
    print(dp[n])
    
    return

import sys
input=sys.stdin.buffer.readline #FOR READING PURE INTEGER INPUTS (space separation ok)
# input=lambda: sys.stdin.readline().rstrip("\r\n") #FOR READING STRING/TEXT INPUTS.

def oneLineArrayPrint(arr):
    print(' '.join([str(x) for x in arr]))
def multiLineArrayPrint(arr):
    print('\n'.join([str(x) for x in arr]))
def multiLineArrayOfArraysPrint(arr):
    print('\n'.join([' '.join([str(x) for x in y]) for y in arr]))
 
def readIntArr():
    return [int(x) for x in input().split()]
# def readFloatArr():
#     return [float(x) for x in input().split()]

def makeArr(defaultValFactory,dimensionArr): # eg. makeArr(lambda:0,[n,m])
    dv=defaultValFactory;da=dimensionArr
    if len(da)==1:return [dv() for _ in range(da[0])]
    else:return [makeArr(dv,da[1:]) for _ in range(da[0])]
 
def queryInteractive(i,j):
    print('? {} {}'.format(i,j))
    sys.stdout.flush()
    return int(input())
 
def answerInteractive(ans):
    print('! {}'.format(' '.join([str(x) for x in ans])))
    sys.stdout.flush()
 
inf=float('inf')
MOD=10**9+7
# MOD=998244353
 
 
for _abc in range(1):
    main()