def answer():
    n = int(input())
    a = [int(x) for x in input().split()]
    c = []
    a.reverse()
    for x in a:
        if x not in c:
            c.append(x)
    i=0
    ans=""
    c.reverse()
    print(len(c))
    while i<len(c):
        ans+=str(c[i])
        i+=1
        if i!=len(c):
            ans+=" "
    return ans
print(answer())