def answer():
    n = int(input())
    a = [int(x) for x in input().split()]
    a.reverse()
    c = []
    for x in a:
        if x not in c:
            c.append(x)
    c.reverse()
    print(len(c))
    ans = ""
    i = 0
    while i < len(c):
        ans += str(c[i])
        i += 1
        if i != len(c):
            ans += " "
    return ans
print(answer())