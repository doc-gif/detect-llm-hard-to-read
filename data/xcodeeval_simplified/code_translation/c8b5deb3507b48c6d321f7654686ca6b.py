n = int(input())
c = 1
if c == 1:
    original = str(n)
    for _ in range(1, 100):
        n += 1
        if str(n).count("8") > 0:
            print(int(n) - int(original))
            c = 0
            break