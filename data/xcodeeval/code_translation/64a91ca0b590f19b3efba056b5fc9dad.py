n = int(input())
num = input()
flag = 0
for i in num:
    if (i < '4') or ('4' < i < '7') or (i > '7'):
        print("NO")
        flag = 1
        break
if flag == 0:
    if sum(map(int, num[:n//2])) == sum(map(int, num[n//2:])):
        print("YES")
    else:
        print("NO")