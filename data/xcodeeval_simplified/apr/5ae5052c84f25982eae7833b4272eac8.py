s = input()
global res
res = 0


def is_valid(x):
    if not x:
        return False
    if x[0] == "0" and len(x) > 1:
        return False
    if "_" in x:
        return False
    if "X" in x:
        return False
    if not int(x) % 25:
        return True


def list_to_str(x):
    return "".join(x)


visited = set()


def dfs(x):
    global res
    if is_valid(x) and x not in visited:
        res += 1
        visited.add(x)
    if "X" in x:
        for i in range(10):
            x_replaced = x.replace("X", str(i))
            dfs(x_replaced)
    else:
        x_list = list(x)
        for i in range(len(x_list)):
            if x_list[i] == "_":
                for j in range(10):
                    x_list[i] = str(j)
                    dfs(list_to_str(x_list))
                break


dfs(s)
print(res)
