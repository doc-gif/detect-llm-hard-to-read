def main():
    n = int(input()) + 1
    s = " " + input().strip()
    arr = [[0] * 2 for x in range(n)]
    x, y = 0, 0
    ans = 0
    for i in range(len(s)):
        if s[i] == "U":
            y += 1
        elif s[i] == "D":
            y -= 1
        elif s[i] == "L":
            x -= 1
        elif s[i] == "R":
            x += 1
        arr[i] = [x, y]
        for j in range(i):
            if arr[j] == arr[i]:
                ans += 1
    print(ans)
    
main()