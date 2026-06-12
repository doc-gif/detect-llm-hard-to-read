import math 

def gcd(x,y):
    while(y):
        x, y = y, x % y
    return x

def lcm(x,y):
    l = (x*y)//gcd(x,y)
    return l

a, b = map(int, input().split(" "))
if a > b:
    a, b = b, a
n = b - a
divisors = [1, n]
k = []
l = []
for i in range(2, int(math.sqrt(n) + 1)):
    if n % i == 0:
        if i * i != n:
            divisors.append(i)
            divisors.append(int(n/i))
        else:
            divisors.append(i)
for i in range(len(divisors)):
    for j in range(1, divisors[i]+1):
        if (j + b) % divisors[i] == 0:
            k.append(j)
            l.append(lcm(a+j, b+j))
            break
mini = min(l)
if lcm(a,b) <= mini:
    print(0)
else:
    idx = l.index(mini)
    print(k[idx])
    