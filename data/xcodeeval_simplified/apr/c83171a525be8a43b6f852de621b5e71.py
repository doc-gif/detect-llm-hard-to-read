import sys

lines = [line for line in sys.stdin]
n = int(lines[0].rstrip("\r\n\t "))
max_price = n * 2 - 1
nines = 0
mp = max_price
while mp >= 9:
    nines += 1
    mp = int(mp / 10)
if nines < 1:
    print("0")
    exit()
price_suffix = "9" * nines
pairs = set()


def add_pairs(max_x: int, price: int):
    from_max = price // 2
    to_min = from_max + 1
    to_max = price - 1
    if to_max > max_x:
        to_max = max_x
    from_min = price - to_max
    for x in range(from_min, from_max + 1):
        pairs.add(f"{x}:{price - x}")


for d in range(10):
    price = int(str(d) + price_suffix) if d > 0 else int(price_suffix)
    if price <= max_price:
        add_pairs(n, price)
print(len(pairs))
