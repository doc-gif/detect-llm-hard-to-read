def main():
    n, k = map(int, input().split())
    s = list(input())
    t = list(input())
    ans = 0
    if t[0] == t[1]:
        #special case
        string = t[0]
        cnt = k
        for i in range(n):
            if cnt == 0:
                break
            if cnt > 0 and s[i] != string:
                s[i] = string
                cnt -= 1

        stringcnt = 0
        for i in range(n):
            if s[i] == string:
                ans += stringcnt
                stringcnt += 1
            else:
                continue

        print(ans)
        return
    else:
        #normal case
        dp = [[[-10**10]*(n+10) for i in range(n+10)] for j in range(n+10)]
        #dp[ind][stringcnt][leftchange] := max subcnt
        dp[0][0][0] = 0
        for i in range(1, n+1):
            now_string = s[i-1]
            for j in range(n+1):
                for m in range(n+1):
                    # whether change to t[0],t[1],or not.
                    if now_string == t[1]:
                        dp[i][j][m] = max(dp[i-1][j-1][m-1],
                                          dp[i-1][j][m-1] + j, dp[i-1][j][m]+j)
                    elif now_string == t[0]:
                        dp[i][j][m] = max(dp[i-1][j-1][m-1],
                                          dp[i-1][j][m-1]+j, dp[i-1][j-1][m])
                    else:
                        dp[i][j][m] = max(dp[i-1][j-1][m-1],
                                          dp[i-1][j][m-1]+j, dp[i-1][j][m])

        ans = max(dp[n][cnt][changed] for cnt in range(n+1)
                  for changed in range(k+1))

        print(ans)
        return


if __name__ == "__main__":
    main()

