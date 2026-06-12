def my_get_ans(n, pos, l, r):
    if l == 1 and r == n:
        return 0

    else:
        if l == 1 and r != n:
            return abs(pos - r) + 1

        elif l != 1 and r == n:
            return abs(pos - l) + 1

        else:
            if l <= pos <= r:
                return r - l + 2 + min(abs(pos - l), abs(pos - r))

            elif pos < l:
                return r - l + 2 + abs(pos - l)

            else:
                return r - l + 2 + abs(pos - r)

print(my_get_ans(*map(int, input().split())))