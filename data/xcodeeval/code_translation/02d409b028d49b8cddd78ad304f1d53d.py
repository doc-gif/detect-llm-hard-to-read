import sys
n=int(sys.stdin.readline())
a=int(sys.stdin.readline())
g=[]
t=a
for i in range(n):
  if int(t%10)!=0:
    g=g+[int(t%10)]
  t=int(t/10)
b=[]
def primes(n):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)
    return primfac

for i in g:
 if i!=1:
  gg = 2
  for j in range(2,i+1):
    if gg<max(primes(j)):
      gg=max(primes(j))
  b=b+[gg]
  if i==9: b=b+[2,3,3]
  else:
   for k in range(gg+1,i+1):
     if k==6: b=b+[3] 
     else:
      b=b+primes(k)
print(int(''.join(map(str, reversed(sorted(b))))))