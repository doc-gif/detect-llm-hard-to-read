import math
d, k, a, b, t = map(int, input().split())

distance = a * t /((b -a )*b) + t /b
time = 0
n = math.ceil((d-distance)/k)

# print(distance)
# print(n)
if (k>d):
    print(d*a)
    exit(0)
if (k<distance):
    time = k*a + (d-k)*b
    print(time)
    exit(0)
if (n*k >=d):
    time = a*d + d//k*t
    if (d%k==0):
        time -= t
else:
    time = n*k*a + (n-1)*t +(d - n*k)*b
print(time)
