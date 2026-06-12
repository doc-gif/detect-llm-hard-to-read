def divisible_by_25(s):
    n = len(s)
    if n < 2:
        if (s == "0") or (s == "_") or (s == "X"):
            return 1
        return 0

    b = s[:n - 2]
    e = s[n - 2:]
    valid_endings = ["25", "50", "75"]
    if n >= 3:
        valid_endings = ["00", "25", "50", "75"]

    total = 0
    for valid_ending in valid_endings:
        valid, x = can_be_made(valid_ending, e)
        if not valid:
            continue

        total += count_variants(x, b)

    return total


def can_be_made(valid_ending, e):
    if e == "__":
        return True, None

    for underscore in ["0", "2", "5", "7"]:
        for x in ["X", "0", "2", "5", "7"]:
            e_ = e.replace("X", x)
            e_ = e_.replace("_", underscore)
            if e_ == valid_ending:
                if x == "X":
                    x = None
                return True, x
    return False, None


def count_variants(x, b):
    if b == "":
        return 1

    if b[0] == "0":
        return 0

    total = 1
    if b[0] == "X":
        if x == 0:
            return 0
        if x is None:
            total *= 9
            x = 1
    if b[0] == "_":
        total *= 9

    for ch in b[1:]:
        if ch == "_":
            total *= 10
        if ch == "X":
            if x is None:
                total *= 10
                x = 1

    return total


s = input()
print(divisible_by_25(s))
