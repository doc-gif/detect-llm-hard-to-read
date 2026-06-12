a, b, c = [int(x) for x in input().split()]
m = max([a,b,c])
print(max(0, 2*m-a-b-c+1))