n=int(input())
a=int(n**0.5)
n-=a**2

print(a*4+2*(n>0)+2*(n>a))