from collections import defaultdict
from typing import List


class Solution:
    def calculate(cls, weight_combo: List[str]) -> str:
        mapping = defaultdict(int)
        for combo in weight_combo:
            first, op, second = combo
            if op == ">":
                mapping[first] += 1
            else:
                mapping[second] += 1
        if mapping["A"] == 1 and mapping["B"] == 1 and mapping["C"] == 1:
            print("Impossible")
        if mapping["A"] == 0:
            print("A", end="")
        elif mapping["B"] == 0:
            print("B", end="")
        elif mapping["C"] == 0:
            print("C", end="")
        if mapping["A"] == 1:
            print("A", end="")
        elif mapping["B"] == 1:
            print("B", end="")
        elif mapping["C"] == 1:
            print("C", end="")
        if mapping["A"] == 2:
            print("A", end="")
        elif mapping["B"] == 2:
            print("B", end="")
        elif mapping["C"] == 2:
            print("C", end="")


if __name__ == "__main__":
    combo = [input() for _ in range(3)]
    Solution.calculate(combo)
