n, k = map(int, input().split())

s = list(input())
if n == 1 and k:
    print("0")
    exit()
if k:
    for i in range(n):
        if not(i):
            if k and s[i] != "1":
                s[i] = "1"
                k -= 1
        else:
            if k:
                if s[i] != "0":
                    s[i] = "0"
                    k -= 1
            else:
                break
print("".join(s))
        
