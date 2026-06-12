n = input()
def ispolindrome(n):
    ans = 0
    if len(n) % 2 == 0:
        ans_len = len(n) // 2
    else:
        ans_len = (len(n) // 2) + 1
    for i in range(ans_len):
        if n[i] == n[len(n) - 1 - i]:
            ans += 1
    if len(n) % 2 and ans == (len(n) // 2) + 1:
        return True
    elif len(n) % 2 == 0 and ans == len(n) // 2:
        return True
    else:
        return False
if ispolindrome(n):
    print("YES")
else:
    n = list(n)
    ans_len = False
    for i in range(len(n)):
        if n[len(n) - 1 - i] == "0":
            ans_len = len(n) - 1 - i
        else:
            break
    if ans_len != False and ispolindrome(n[:ans_len]):
        print("YES")
    else:
        print("NO")