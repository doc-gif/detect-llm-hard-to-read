import string
import re
values = {str(d): d for d in range(10)}
for ch in string.ascii_uppercase:
    values[ch] = ord(ch) - 55
def convert(s, base):
    x = 0
    for ch in s:
        digit = values[ch]
        if digit >= base:
            return None
        x = base * x + digit
    return x
match = re.match(r"0*(\w+):0*(\w+)", input().strip())
hour_part, minute_part = match.groups([1, 2])
valid_bases = []
for base in range(2, 60):
    hour = convert(hour_part, base)
    minute = convert(minute_part, base)
    if hour is None or minute is None:
        continue
    if hour < 24 and minute < 60:
        valid_bases.append(base)
if not valid_bases:
    print(0)
elif len(hour_part) + len(minute_part) == 2:
    print(-1)
else:
    print(*valid_bases)