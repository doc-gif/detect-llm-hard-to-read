from itertools import permutations
nums = list(map(int, input().split()))
o = input().split()
print(min(eval("min(((a{0}b){1}c){2}d,(a{0}b){2}(c{1}d))".format(*o)) for a, b, c, d in permutations(nums)))