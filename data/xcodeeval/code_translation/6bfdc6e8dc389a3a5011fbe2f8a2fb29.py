import sys
import math
import itertools	
original_stdout = sys.stdout

var_for_sublime = False 


if var_for_sublime:
	fin = open('input.txt' , 'r')
	fout = open('output.txt' , 'w')
	sys.stdout = fout
	def give_string():
		return fin.readline().strip()
else:
	fin = sys.stdin 
	fout = sys.stdout
	def give_string():
		return fin.buffer.readline().strip()

def give_list():
	return list(map(int, give_string().split()))
def give_int():
	return int(give_string())


MOD = 1e9+ 7
def modpow( a , p) :
	ans = 1 
	while p :
		if p&1 :
			ans *= a 
			ans %= MOD 
		p >>= 1
		a *= a
		a %= MOD
	return ans 		



def fac_cal(n):
	ans = 1
	for i in range(1 , n+1):
		ans *= i 
		ans %= MOD 
	return ans 





def solve():
	t = 1
	l = list(itertools.permutations([1 ,2 ,3, 4,5,6]))
	n = give_int()
	a1 ,a2 ,a3 = give_list()
	b1 , b2 , b3 = give_list()
	mx = min(a1 , b2) + min(a2 , b3) + min(a3 , b1)
	temp = 0
	for per in l :
		ta1 ,ta2 , ta3 , tb1 , tb2 ,tb3 = a1 , a2 , a3 , b1 ,b2 , b3
		tmx = 0 
		for el in per :
			if el == 1:
				t1 = min(ta1 , tb1)
				ta1 -= t1 
				tb1 -= t1 
				tmx += t1 
			elif el == 2:
				t1 = min(ta1 , tb3)
				ta1 -= t1
				tb3 -= t1 
				tmx += t1 
			elif el == 3:
				t1 = min(ta2 , tb2)
				ta2 -= t1 
				tb2 -= t1 
				tmx += t1 
			elif el==4:
				t1 = min(ta2 , tb1)
				tb1 -= t1 
				ta2 -= t1
				tmx += t1 
			elif el== 5:
				t1 = min(ta3 , tb3)
				ta3 -= t1 
				tb3 -= t1 
				tmx += t1 
			elif el ==6:
				t1 = min(ta3 , tb2)
				tb2 -= t1 
				ta3 -= t1
				tmx += t1 
		temp = max(temp , tmx)
	print(n-temp , end = ' ')
	print(mx)

def Hey_Yashwant():
	try :
		t = 1 
		# t = give_int()
		for i in range(t):
			solve()
	finally:
		fin.close()
		fout.close()
		sys.stdout = original_stdout





if __name__ == '__main__' :
	Hey_Yashwant()