def palindromeString(n):
    s = str(n)
    myList = list(s)
    for i in range(len(s)):
        myList.append(s[len(s) - i - 1])
    return int("".join(myList))
k, p = map(int, input().split())
total = 0
for i in range(1, k + 1):
    total += palindromeString(i)
print(total % p)