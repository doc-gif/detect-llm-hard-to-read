def main():
    n = int(input()) + 1
    s = " " + input().strip()
    positions = [[0, 0] for _ in range(n)]
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
        positions[i] = [x, y]
        for j in range(i):
            if positions[j] == positions[i]:
                ans += 1
    print(ans)
main()