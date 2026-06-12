from itertools import permutations
nums = list(map(int, input().split()))
operators = input().split()
result = min(
    eval("min(((a{0}b){1}c){2}d, (a{0}b){2}(c{1}d))".format(*operators))
    for a, b, c, d in permutations(nums)
)
print(result)