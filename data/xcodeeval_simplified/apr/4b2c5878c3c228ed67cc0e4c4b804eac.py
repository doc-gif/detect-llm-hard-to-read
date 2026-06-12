n, k = map(int, input().split())
a = input().split()
master = []
current_group = []
for i in range(1, n + 1):
    if i % k == 0:
        current_group.append(a[i - 1])
        master.append(current_group)
        current_group = []
    else:
        current_group.append(a[i - 1])


def count(lst, item):
    cnt = 0
    for elem in lst:
        if elem == item:
            cnt += 1
    return cnt


def common(lst):
    max_count = 0
    max_item = None
    for elem in lst:
        if count(lst, elem) >= max_count:
            max_item = elem
            max_count = count(lst, elem)
    return max_item


has_duplicate_groups = False
for group in master:
    if count(master, group) > 1:
        has_duplicate_groups = True
answer = 0
if has_duplicate_groups == False:
    reference = common(a)
    for elem in a:
        if elem != reference:
            answer += 1
if has_duplicate_groups == True:
    ref_group = common(master)
    for group in master:
        if group != ref_group:
            for j in range(len(group)):
                if group[j] != ref_group[j]:
                    answer += 1
print(answer)
