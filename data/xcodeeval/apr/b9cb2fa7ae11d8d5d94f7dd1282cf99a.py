def cifreDuzina(x):
    cifre = {-1}
    br = 0
    while x:
        tmp = x % 10
        cifre.add(tmp)
        x //= 10
        br += 1
    cifre.remove(-1)
    l = []
    l.append(cifre)
    l.append(br)
    return l

def resi():
    n, x = map(int, input().split())
    #print(najvecaCifra(x))
    l = najvecaCifra(x)
    br = 0
    while l[1] < n:
        if l[0] == 1:
            print(-1)
            return
        x *= l[0]
        br += 1
        l = najvecaCifra(x)
    print(br)

def rekurzija(n, x):
    #print(x, cifreDuzina(x)[1])
    if cifreDuzina(x)[1] == n:
        return 0
    else:
        mn = 100000
        for c in cifreDuzina(x)[0]:
            if c == 0 or c == 1:
                continue
            if mn > rekurzija(n, c*x):
                mn = rekurzija(n, c*x)
        return mn + 1
        


n, x = map(int, input().split())
if rekurzija(n, x) != 100001:
    print(rekurzija(n, x))
else:
    print(-1)
#print(cifreDuzina(int(input())))
