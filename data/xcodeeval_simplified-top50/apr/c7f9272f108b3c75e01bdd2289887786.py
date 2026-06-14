import threading
import sys

input = sys.stdin.readline
threading.stack_size(10**8)
sys.setrecursionlimit(10**7)
from collections import defaultdict


def main():
    s = input()
    global res
    res = 0
    vis = set()

    def valid(x):
        if not x:
            return False
        if x[0] == "0" and len(x) > 1:
            return False
        if "_" in x:
            return False
        if "X" in x:
            return False
        return int(x) % 25 == 0

    def dfs(x):
        global res
        if valid(x) and x not in vis:
            res += 1
            vis.add(x)
        if "X" in x:
            for i in range(10):
                xc = x.replace("X", str(i))
                dfs(xc)
        else:
            x_list = list(x)
            for i in range(len(x_list)):
                if x_list[i] == "_":
                    for j in range(10):
                        x_list[i] = str(j)
                        dfs("".join(x_list))
                    break

    dfs(s)
    print(res)


threading.Thread(target=main).start()
