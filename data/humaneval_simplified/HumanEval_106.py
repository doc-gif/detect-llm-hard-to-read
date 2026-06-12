from typing import List


def f(n: int) -> List[int]:
    ret = []
    for i in range(1, n + 1):
        if i % 2 == 0:
            x = 1
            for j in range(1, i + 1):
                x *= j
            ret.append(x)
        else:
            x = 0
            for j in range(1, i + 1):
                x += j
            ret.append(x)
    return ret
