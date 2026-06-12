from sys import*
import math
def next_c(c):
	x = int(math.sqrt(c))
	i = 2
	while(i<=x):
		if((c%(i)) == 0):
			return int(c/i)
			break
		else:
			i = i+1
	if(i > x):
		return 1
def game(n):
	sum = n
	r =next_c(n)
	while(r != 1):
		sum = sum + r
		r = next_c(r)
	return sum+1
n = int(input())
print(game(n))