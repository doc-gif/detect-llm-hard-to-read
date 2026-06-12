def complaint_index(i):
    if i % 2 == 0:
        return i + 1
    return i - 1
def is_same_pair(mas1, mas2, i, j):
    i2 = complaint_index(i)
    j2 = complaint_index(j)
    return mas1[i2] == mas2[j2]
n, m = map(int, input().split())
mas1 = list(map(int, input().split()))
mas2 = list(map(int, input().split()))
n2 = n * 2
m2 = m * 2
st1 = set()
st2 = set()
for i in range(n2):
    for j in range(m2):
        if mas1[i] == mas2[j] and not is_same_pair(mas1, mas2, i, j):
            st1.add(mas1[i])
            st2.add(mas2[j])
if len(st1) == 1:
    print(st1.pop())
    exit(0)
if len(st2) == 1:
    print(st2.pop())
    exit(0)
for i in range(n):
    first_found = second_found = False
    for j in range(m):
        if (mas1[i * 2] == mas2[j * 2] and mas1[i * 2 + 1] == mas2[j * 2 + 1]) or (
            mas1[i * 2 + 1] == mas2[j * 2] and mas1[i * 2] == mas2[j * 2 + 1]
        ):
            continue
        if mas1[i * 2] == mas2[j * 2] or mas1[i * 2] == mas2[j * 2 + 1]:
            first_found = True
        if mas1[i * 2 + 1] == mas2[j * 2] or mas1[i * 2 + 1] == mas2[j * 2 + 1]:
            second_found = True
    if first_found and second_found:
        print(-1)
        exit(0)
for j in range(m):
    first_found = second_found = False
    for i in range(n):
        if (mas1[i * 2] == mas2[j * 2] and mas1[i * 2 + 1] == mas2[j * 2 + 1]) or (
            mas1[i * 2 + 1] == mas2[j * 2] and mas1[i * 2] == mas2[j * 2 + 1]
        ):
            continue
        if mas1[i * 2] == mas2[j * 2] or mas1[i * 2 + 1] == mas2[j * 2]:
            first_found = True
        if mas1[i * 2] == mas2[j * 2 + 1] or mas1[i * 2 + 1] == mas2[j * 2 + 1]:
            second_found = True
    if first_found and second_found:
        print(-1)
        exit(0)
print(0)