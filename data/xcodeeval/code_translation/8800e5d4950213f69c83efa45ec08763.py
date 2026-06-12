string = input()
ss = string.count('-')
os = string.count('o')

if os == 0:
    print("YES")
elif ss%os == 0:
    print("YES")
else:
    print("NO")
