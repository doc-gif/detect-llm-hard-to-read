n, q = map(int, input().split())
rules = {}
to_expand = {"a"}
valid_strings = set()
for _ in range(q):
    a, b = input().split()
    rules.setdefault(b, set()).add(a)
while to_expand:
    current = to_expand.pop()
    if len(current) == n:
        valid_strings.add(current)
        continue
    for replacement in rules.setdefault(current[0], set()):
        to_expand.add(replacement + current[1:])
print(len(valid_strings))