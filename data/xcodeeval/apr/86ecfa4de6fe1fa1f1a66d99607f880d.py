n = int(input())
d = str(n)
a = []
t = n
if(n<10):
    print(n)
else:
    flag = 0
    while(n>9):
        a.append(9)
        t = n%10
        if(t != 9):
            flag = 1
        n //= 10
    s = n
    #print(s,t,flag)
    a.append(n-1)
    if(a[-1] != 0):
        a1 = 1
        a2 = 1
        if(flag == 0):
            for i in range(1,s+1):
                for j in range(1,10):
                    if((i==s and j<=t) or (i<s)):
                        if(i*j > a1*a2):
                            a1 = i
                            a2 = j
        else:
            for i in range(1,s+1):
                for j in range(1,10):
                    if((i==s and j<t) or (i<s)):
                        if(i*j > a1*a2):
                            a1 = i
                            a2 = j   
        #print(a1,a2)
        a[-1] = a1
        a[-2] = a2
    else:
        a[-1] = 1
    ans = 1

    if(a[-3] == 9 and a[-2] == 7 and d[1] >= '8' and d[2] >= '9'):
        a[-2] = 8
        a[-3] = 8
    #print(a)
    for i in a:
        ans *= i
    print(ans)