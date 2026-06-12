s=[int(c) for c in input()]
ok=1
for i in range(1,len(s)):
  if abs(s[i]-s[i-1])>1: ok=0; break
w=[1]*10
for v in s[1:]:
  ww=w[:]
  w=[0]*10
  for d in range(10):
    q,r=divmod(v+d,2)
    w[q]+=ww[d]
    if r>0:
      w[q+1]+=ww[d]

print(sum(w)-ok)      
