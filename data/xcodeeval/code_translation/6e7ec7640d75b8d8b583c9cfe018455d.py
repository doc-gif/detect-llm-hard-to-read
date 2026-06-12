"""."""
import math
l, r, gcd, lcm = (int(x) for x in input().split())
if lcm % gcd != 0:
    print(0)
    quit()

lcm_divisors = set()
for num in range(1, int(lcm**0.5) + 2):
    if lcm % num == 0:
        lcm_divisors.add(num)
        lcm_divisors.add(lcm // num)
product = gcd * lcm
answers = set()
for divisor in lcm_divisors:
    if divisor < l or divisor > r:
        continue
    dop = product // divisor
    if dop < l or dop > r:
        continue
    if math.gcd(divisor, dop) != gcd:
        continue
    answers.add((divisor, dop))
    answers.add((dop, divisor))

print(len(answers))
