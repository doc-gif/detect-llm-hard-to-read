#!/usr/bin/python3
from math import log2 as log
def gen(x,y,z):
	return ["{}^{}^{}".format(x,y,z),"{}^{}^{}".format(x,z,y),"({}^{})^{}".format(x,y,z),"({}^{})^{}".format(x,z,y)]


def f(x):
	return log(x)

def calc1(x,y,z):
	return [z*f(y) + f(f(x)),y*f(z) + f(f(x)),f(y*z) + f(f(x)),f(z*y) + f(f(x))]
	
def calc2(x,y,z):
	return [x**y**z,x**z**y,x**(y*z),x**(z*y)]

def build(x,y,z):
	s1,s2 = [],[]
	if x > 1:
		s1 += gen('x','y','z')
		s2 += calc1(x,y,z)
	
	if y > 1:
		s1 += gen('y','x','z')
		s2 += calc1(y,x,z)
	
	if z > 1:
		s1 += gen('z','x','y')
		s2 += calc1(z,x,y)
		
	return s1,s2
	
def build2(x,y,z):
	s1,s2 = [],[]
	if x > 1:
		s1 += gen('x','y','z')
		s2 += calc2(x,y,z)
	
	if y > 1:
		s1 += gen('y','x','z')
		s2 += calc2(y,x,z)
	
	if z > 1:
		s1 += gen('z','x','y')
		s2 += calc2(z,x,y)
		
	return s1,s2
	
x,y,z = [float(t) for t in input().strip().split()]

s1,s2 = build(x,y,z)
if len(s1) == 0: s1,s2 = build2(x,y,z)
print(s1[s2.index(max(s2))])