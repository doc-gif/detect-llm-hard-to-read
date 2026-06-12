# This is simple recurrence that we had learnt that is
# let S(n) be the number of bills for getting the money out
# then recurrence is
# s(n)=1+min(S(n-1),S(n-5),S(n-10),S(n-20),S(n-100))
# memoization 
# lst conatins list where for each index we have its min bill stores

#  we do this problem iterative
import sys 

def hitLotery(n):
	lst=[-1 for i in range (n+1)]
	# base case
	lst[0]=0
	i=1
	while(i<len(lst)):
		# induction hypothesis
		
		b1=lst[i-1]
		if(i-5>=0):
			b2=lst[i-5]
		else:
			b2=sys.maxsize 

		if(i-10>=0):
			b3=lst[i-10]
		else:
			b3=sys.maxsize 
		if(i-20>=0):
			b4=lst[i-20]
		else:
			b4=sys.maxsize 
		if(i-100>=0):
			b5=lst[i-100]
		else:
			b5=sys.maxsize 


		# now we have got the previous valuies thus 
		# induction step
		lst[i]=1+min(b1,b2,b3,b4,b5)
		i=i+1 

	return(lst[n])

n=int(input())
print(hitLotery(n))