from itertools import chain, combinations
from collections import defaultdict
import math

def powerset(iterable):
    xs = list(iterable)
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def has(s):
	h = 1
	p = [2,3,5,7,11,13,17,19,23,29]
	for i in s:
		h *= p[i-1]
	return h

h = set()
total = 0
ok = [int(i) for i in "1000000000000000000"]
require = set(ok)
 
for s in powerset(ok):
	if has(s) in h or len(s) == 0:
		continue

	h.add(has(s))

	d = defaultdict(int)
	for c in s:
		d[c] += 1

	flag = False
	for i in require:
		if d[i] == 0:
			flag = True
			break
	if flag: continue

	prod = 1
	for k in d:
		prod *= math.factorial(d[k])

	n = len(s)
	total += (n-d[0])*math.factorial(n-1)/prod

print(int(total))