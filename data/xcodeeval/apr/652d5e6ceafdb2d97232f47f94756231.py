# def sum_digits(n):
#     s = 0
#     while n:
#         s += n % 10
#         n //= 10
#     return s


# n, s = map(int, input().split())

# count = 0
# summ = sum_digits(n)
# # k = sum_digits(n - n%10 - 1)
# # print(k)
# for num in range(n, 9, -1):
# 	if num % 10 == 9:
# 		summ = sum_digits(num)
# 	# print(num, summ)
# 	if num - summ  >= s:
# 		count += 1
# 	summ -= 1
	


# print(count)


def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s

def binsearch(a, l, r, elem):
	medium = (l + r ) // 2
	s = a[medium] - sum_digits(a[medium])
	s1 = a[medium-1] - sum_digits(a[medium-1])
	s2 = a[medium+1] - sum_digits(a[medium+1])
	while not(s2 >= elem and s < elem): #s >= elem and s1 < elem or 
		# print(l,medium,r)
		if s <= elem:
			l = medium
		elif s >= elem:
			r = medium
		k = medium
		medium = (l + r ) // 2
		if k == medium:
			break
		# print(l,medium,r)
		s = a[medium] - sum_digits(a[medium])
		s2 = a[medium+1] - sum_digits(a[medium+1])
	s1 = a[medium-1] - sum_digits(a[medium-1])
	if s >= elem and s1 < elem:
		return medium
	elif s2 >= elem and s < elem:
		return medium + 1
	else:
		return len(a)	

n, s = map(int, input().split())
a = [i for i in range(n+1)]


y = binsearch(a, 0, len(a)-1, s)
# print(y)
print(n - y + 1)




