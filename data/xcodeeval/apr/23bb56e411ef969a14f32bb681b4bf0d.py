m, s = map(int, input().split())

ans = []
flag = 0
temp = 0
if s!=0:
    while s >= 0 and s//9<m or (s//9==m and s%9==0) and temp<m:
        flag = 1
        temp += 1
        if s-9 > 0:
            ans.append(9)
            s -= 9
        else:
            ans.append(s)
            s = 0
            continue

        if s==0 and temp<m:
            ans.append(0)

if flag:
    ans1 = "".join(map(str,ans))
    if ans[-1]==0:
        for i in range(len(ans)):
            if ans[-1-i]!=0:
                ans[-1-i] -= 1
                break
        ans[-1] = 1

    ans2 = "".join(map(str,ans[::-1]))
    print(ans2, ans1)
elif flag==0 and s==0 and m==1:
    print(0,0)
else:
    print(-1, -1)