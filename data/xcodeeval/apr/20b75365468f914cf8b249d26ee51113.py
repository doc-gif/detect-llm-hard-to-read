def main():
    r,c = map(int, input().split())
    cake = [input() for _ in range(r)]
    rc = r * c
    neigh = []
    for y in range(r):
        for x in range(c):
            if 'S' in cake[y]:
                row = ()
            else:
                row = tuple(range(y * c, y * c + c))
            if any('S' == _[x] for _ in cake):
                col = ()
            else:
                col = tuple(range(x, r * c, c))
            neigh.append((row, col))
    mi = rc
    def deeper(field):
        nonlocal mi
        i = sum(field)
        if mi > i:
            mi = i
        for i, piece in enumerate(field):
            if field:
                row, col = neigh[i]
                if any(field[_] for _ in row):
                    f1 = field[:]
                    for j in row:
                        f1[j] = False
                    deeper(f1)
                if any(field[_] for _ in col):
                    f1 = field[:]
                    for j in col:
                        f1[j] = False
                    deeper(f1)
    fld = [_ == '.' for s in cake for _ in s]
    deeper(fld)
    print(sum(fld) - mi)


main()
