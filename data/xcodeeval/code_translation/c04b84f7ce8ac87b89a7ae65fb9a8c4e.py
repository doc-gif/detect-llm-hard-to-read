import math
s = input().split()
for i in range(4):
    s[i] = int(s[i])
print(min((s[1]-s[0]%s[1])*s[2],(s[0]%s[1])*s[3]))