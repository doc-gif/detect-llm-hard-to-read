def reflection(num):
    digits = str(num)
    reflected = []
    for digit in digits:
        inverted = 9 - int(digit)
        if inverted == 0 and not reflected:
            continue
        reflected.append(str(inverted))
    return int("".join(reflected)) if reflected else 0
def solve(l, r):
    best = max(l * reflection(l), r * reflection(r))
    power = 0
    while 5 * (10**power) <= l:
        power += 1
    while 5 * (10**power) <= r:
        candidate = 5 * (10**power)
        best = max(best, candidate * reflection(candidate))
        power += 1
    return best
l, r = map(int, input().split())
print(solve(l, r))