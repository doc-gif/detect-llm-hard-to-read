# https://codeforces.com/contest/47/problem/B


def single_integer():
    return int(input())


def multi_integer():
    return map(int, input().split())


def string():
    return input()


def multi_string():
    return input().split()


left_dict = dict()
right_dict = dict()

for i in range(3):
    c1, s, c2 = input()
    if s == ">":
        left_dict[c1] = left_dict.get(c1, 0) + 1
        right_dict[c2] = right_dict.get(c2, 0) + 1
    else:
        left_dict[c2] = left_dict.get(c2, 0) + 1
        right_dict[c1] = right_dict.get(c1, 0) + 1


if len(left_dict) == 3:
    print("Impossible")
else:
    for k, v in right_dict.items():
        if v == 2:
            print(k, end="")
            break
    for k, v in right_dict.items():
        if v == 1:
            print(k, end="")
            break

    for k, v in left_dict.items():
        if v == 2:
            print(k, end="")
            break


