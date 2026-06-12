def main():
    p = [1]
    for i in range(1,11):
        p.append(p[i-1]*2)
    hr = '12345RGBYW'
    gt = {'1': 0,'2': 1,'3': 2,'4': 3,'5': 4,'R': 5,'G': 6,'B': 7,'Y': 8,'W': 9}
 
    def check(c,mask):
        tmp = gt[c]
        if (mask // p[tmp]) % 2 == 1:
            return True
        return False
 
    def count(mask):
        tmp = 0
        while mask>0:
            tmp+=mask % 2
            mask//=2
        return tmp
 
    n = int(input())
    a = list(input().split())
    ans = 10
    for mask in range(1024):
        f = True
        for i in range(n):
            for j in range(n):
                if a[i] == a[j]:
                    pass
                elif (a[i][1] != a[j][1]) and (check(a[i][1],mask) or check(a[j][1],mask)):
                    pass
                elif (a[i][0] != a[j][0]) and (check(a[i][0],mask) or check(a[j][0],mask)):
                    pass
                else:
                    f = False
                    break
            if not f:
                break
        if f:
            ans = min(ans,count(mask))
    print(ans)
main()