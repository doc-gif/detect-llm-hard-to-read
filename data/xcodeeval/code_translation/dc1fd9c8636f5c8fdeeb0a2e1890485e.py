def main():
    n=int(input())
    dp=[]
    dp.append(0)
    dp.append(0)
    dp.append(2)
    for i in range(3,n+1):
        dp.append(dp[i-2]*2)
    print(dp[n])
if __name__=="__main__":
    main()