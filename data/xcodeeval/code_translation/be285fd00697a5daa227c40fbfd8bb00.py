def digit(x):
    return x if x<10 else x//10+9-(0 if str(x)[0]<=str(x)[-1] else 1)
l,r = map(int,input().split())
print(digit(r) - digit(l-1))