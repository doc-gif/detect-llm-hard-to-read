'''
t=int(input())
for _ in range(t):
    n=int(input())
    if n%2==0:
        print([1,1000]*(n//2))
    else:
        print([1,1000]*((n-1)//2)+[1000])
'''

t=int(input())
for _ in range(t):
    n=int(input())
    if n%2==0:
        print(n//2,n//2)
    else:
        multiples = set()
        sol=1
        multiples.update(range(4,n+1,2))
        for i in range(3, n,2):
            if i not in multiples:
                multiples.update(range(i*i, n+1, i))
            if n%i==0:
                sol=i
        print(sol,n-sol)
'''
n=int(input())
multiples = set()
sol=1
multiples.update(range(4,n+1,2))
for i in range(3, n,2):
    if i not in multiples:
        multiples.update(range(i*i, n+1, i))
    if n%i==0:
        sol=i
print(sol)
'''



