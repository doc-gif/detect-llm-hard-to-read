
n,x,y = map(int,input().strip().split())

a = list(map(int,input().strip().split()))

ans_a = 0
ans_b = 0
ans = 1

for i in range(n//2):
    
    if a[i] != a[n-i-1]:
        if a[i]==2 or a[n-i-1]==2:
            if a[i] == 0 or a[n-i-1]==0:
                ans_a+=1
            else:
                if a[i] == 1 or a[n-i-1]==1:
                    ans_b+=1
        else:
            ans = 0
            break
    else:
            if a[i] == 2 and a[n-i-1] == 2:
                if x < y:
                    ans_a+=2
                else:
                    ans_b+=2


if ans:
    temp = 0
    if n%2 == 0:
        temp = 0
    else:
        if a[n//2] == 2:
            temp = min(x,y)
        
    print(ans_a*x + ans_b*y + temp)
else:
    print(-1)
