n=int(input())
m=int(n**(1/2))
for i in range(max(0,m-10**3),m+10**3):
    if i*i+sum(list(map(int,str(i))))*i==n:
        print(i)
        exit()
print(-1)