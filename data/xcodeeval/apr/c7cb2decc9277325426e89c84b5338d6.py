from __future__ import print_function
import sys
from collections import deque,defaultdict
import math
import functools
import itertools
from bisect import bisect_left,bisect_right
import operator
import heapq
from random import random,randint,randrange,shuffle
true=True
false=False
null=None
SLOW=True
try:
 range=xrange
except:
 ignored=1
def fast():
 global SLOW
 SLOW=False
def compute(val, func): return func(val)
def seq(lo,hi,step=1): 
 return range(lo,hi+1,step)
def sround(val,nd):
 return '{0:.{1}f}'.format(val,nd)
def ceil(a,b):
 ans=a//b
 if a%b!=0: ans+=1
 return ans
def e1e(d,e): return d*(10**e)
mod=e1e(1,9)+7
try:
 memoi=functools.lru_cache(None)
except:
 class memoize(dict):
  def __init__(self,f):
   self.f=f
  def __call__(self,*args):
   return self[args]
  def __missing__(self,key):
   ans=self[key]=self.f(*key)
   return ans
 memoi=memoize
class ndarray(list):
 def __init__(self,defval,sizes):
  self.sizes=sizes
  self.dimension=len(sizes)
  self.pm=pm=list(sizes)
  pm.append(1)
  for ii in reversed(range(self.dimension)): pm[ii]*=pm[ii+1]
  list.__init__(self,[defval]*pm[0])
 def ___i1d___(self,ixs):
  if SLOW and len(ixs)!=self.dimension: raise LookupError('Dimension must be {}.'.format(self.dimension))
  ans=0
  for ii in range(self.dimension):
   ix=ixs[ii]
   if SLOW and ix>=self.sizes[ii]:
    raise IndexError('Index[{}]={} >= Len[{}]={}.'.format(ii,ix,ii,self.sizes[ii]))
   ans+=ix*self.pm[ii+1]
  return ans
 def __getitem__(self,ixs):
  ixs=self.___i1d___(ixs)
  return list.__getitem__(self,ixs)
 def __setitem__(self,ixs,val):
  ixs=self.___i1d___(ixs)
  list.__setitem__(self,ixs,val)
 def _str_(self,dim0=0,ofs=0):
  lft="  "*dim0
  if dim0+1==self.dimension: return lft+str(list.__getitem__(self,slice(ofs,ofs+self.sizes[dim0])))
  ans=[]
  for ii in range(self.sizes[dim0]):
   ans.append(self._str_(dim0+1,ofs))
   ofs+=self.pm[dim0+1]
  ans="{0}[\n{1}\n{0}]".format(lft,",\n".join(ans))
  return ans
 def __str__(self):
  return self._str_()
def arrays(defval,*sizes):
 if len(sizes)==1: return [defval]*sizes[0]
 return ndarray(defval,sizes)
def perr(*args,**kwargs): 
 if SLOW:
  print(*args,file=sys.stderr,**kwargs)
def line():
 ln=sys.stdin.readline().strip()
 #perr(ln)
 if ln=='': sys.exit()
 return ln
def lines(n): return [line() for i in range(n)]
def split(ln=None): return (ln or line()).split()
def num(str=None):
 str=str or line()
 return float(str) if '.' in str else int(str)
def nums(o=None):
 if o is not None:
  if isinstance(o, int): o=lines(o)
  elif isinstance(o, str): o=split(o)
 return list(map(num, o or split()))
def loop(f,n=0):
 for tcid in range(n or 99999999): f(tcid+1)
def repeat(n,f):
 for _ in range(n): yield f()
def recursi(root,fchildren,ctop):
  p=deque()
  c=deque()
  q=deque()
  q.append(root)
  while len(q)>0:
   pp=q.popleft()
   for cc in fchildren(pp):
    p.append(pp)
    c.append(cc)
    q.append(cc)
  for _ in range(len(p)):
   ctop(c.pop(),p.pop())
"""
recursi(root,fchilds,ctop)
e1e(d,e) mod arrays(defv,*sz) repeat(n,f)
ceil(a,b) sround(val,nd) true false null @memoi
num(?) nums(?) split(?) lines(n) line()
perr(print) seq() loop(f(tcid),0) compute(v,f) fast()
"""
#
def mainloop(tcid): #
 ignored=1 #
 n=num()
 dp=arrays(0,n+1,4)
 dp[0,0]=1
 for ii in seq(1,n):
  for jj in range(4):
   for kk in range(4):
    if jj!=kk:
     dp[ii,jj]+=dp[ii-1,kk]
     dp[ii,jj]%=mod
 print(dp[n,0])
tcmax=0
loop(mainloop,tcmax) #
#