a=input()
b=input()
def isSubSequence(str1,str2): 
   m = len(str1) 
   n = len(str2) 
      
   j = 0    # Index of str1 
   i = 0    # Index of str2 
      
    # Traverse both str1 and str2 
    # Compare current character of str2 with  
    # first unmatched character of str1 
    # If matched, then move ahead in str1 
      
   while j<m and i<n: 
      if str1[j] == str2[i]:     
         j = j+1    
      i = i + 1
          
    # If all characters of str1 matched, then j is equal to m 
   return j==m 
      
c=a
s=0
for i in b:
   if i not in c:
      s=-1
      break
   else:
      d=c.index(i)
      c=c[:d]+c[d+1:]
if s==-1:
   print("need tree")
else:
   if len(b)>len(a):
      print("need tree")
   elif len(b)==len(a):
      print("array")
   else:
      if isSubSequence(b,a):
         print("automaton")
      else:
         print("both")
         
      
   