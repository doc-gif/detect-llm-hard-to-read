from sys import stdin, stdout
input = stdin.readline

n = int(input())
a = list(map(int, input().split()))
ans = 0

uni = False
ind = 0

while ind < n-1:
    if a[ind] == 1:
        ans += 1
        ind += 1
        uni = True
    else:
        if a[ind+1] == 0:
            while ind < n and a[ind] == 0:
                ind += 1
            uni = False
        else:
            if uni:
                ans += 1
            ind += 1

if a[n-1] == 1:
    ans += 1

stdout.write(str(ans))


