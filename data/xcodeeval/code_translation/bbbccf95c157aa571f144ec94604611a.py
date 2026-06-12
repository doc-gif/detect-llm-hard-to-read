x = input()
y = 1
k = 1
bea = []
while y <= 100000:
    y = ((2**k)-1)*(2**(k-1))
    bea.append(y)
    k = k + 1
bea.pop(len(bea)-1)
temp = 0
for j in range(len(bea)):
    if int(x)%bea[j]==0:
        temp = bea[j]
print(temp)