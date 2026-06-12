import sys
# a simple parser for python. use get_number() and get_word() to read
def parser():
    while 1:
        data = list(input().split(' '))
        for number in data:
            if len(number) > 0:
                yield(number)   

input_parser = parser()

def get_word():
    global input_parser
    return next(input_parser)

def get_number():
    data = get_word()
    try:
        return int(data)
    except ValueError:
        return float(data)

def done(x,y):
    print("%d %d"%(x,y))
    sys.exit(0)

def die():
    print(-1)
    sys.exit(0)

def ext_gcd(a,b):
    if b != 0:
        tmp = ext_gcd(b,a%b)
        return [tmp[1], tmp[0] - (a//b)*tmp[1]]
    return [1,0]

def gcd(a,b):
    if b == 0:
        return a
    return gcd(b,a%b)

n = get_number()
m = get_number()
x = get_number()
y = get_number()
vx = get_number()
vy = get_number()

if vx == 0 :
    if x != 0 and x != n :
        die()
    if x == 0:
        if vy > 0:
            done(0,m)
        else:
            done(0,0)
    if x == n:
        if vy > 0:
            done(n,m)
        else:
            done(n,0)

if vy == 0 :
    if y != 0 and y != m:
        die()
    if y == 0:
        if vx > 0:
            done(n,0)
        else:
            done(0,0)
    if y == m:
        if vx > 0:
            done(n,m)
        else:
            done(0,m)

g = gcd(vy*n,vx*m)

if (vy*x-vx*y)%g != 0:
    die()

a = vy*n//g
b = vx*m//g
t = (vy*x-vx*y)//g
res = ext_gcd(a,-b)
if res[0]*a + res[1]*(-b) == -1:
    res[0] = -res[0]
    res[1] = -res[1]

alpha = res[0]*t
beta = res[1]*t
k = b//gcd(a,b)
T = (n*alpha-x)//vx

val = 0
if vx*k > 0 :
    val = 1
else :
    val = -1
high = 98765432198765432198765432199
low = 0
ans = 0

while high >= low:
    mid = (high+low)//2
    nalpha = alpha + mid*val*k
    nT = (n*nalpha-x)//vx
    if nT > 0:
        ans = mid
        high = mid-1
    else:
        low = mid+1

alpha = alpha + ans*val*k
T = (n*alpha-x)//vx

val = 0
if vx*k > 0 :
    val = -1
else :
    val = 1
    
high = 98765432198765432198765432199
low = 0
ans = 0
while high >= low:
    mid = (high+low)//2
    nalpha = alpha + mid*val*k
    nT = (n*nalpha-x)//vx
    if nT >= 0:
        ans = mid
        low = mid+1
    else:
        high = mid-1

alpha = alpha + ans*val*k
T = (n*alpha-x)//vx


X = x + vx*T
Y = y + vy*T
T = t + vy*T
if (X//n)%2 == 0 and (Y//m)%2 == 0 :
    done(0,0)
elif (X//n)%2 == 0:
    done(0,m)
elif (Y//m)%2 == 0:
    done(n,0)
else:
    done(n,m)
    
    
    
    
    
    
    
