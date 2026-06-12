n=int(input())
inp=" ".join(input()).split()
ris=0
if len(inp)==0 or len(inp) ==1 or len(inp)==2 and inp[0]!=inp[1]:
       print(0)
elif len(inp)==2 and inp[0]==inp[1]:
       print(1)
elif len(list(dict.fromkeys(inp)))==1:
       print(len(inp)-1)
else:
       for x in range(0,len(inp)-1):
              if inp[x]==inp[x+1]:
                     ris+=1
       print(ris)