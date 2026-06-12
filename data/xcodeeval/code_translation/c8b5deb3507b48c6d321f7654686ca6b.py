n=int(input())
c=1
if c==1 :
    d=str(n)
    for i in range(1,100) :
        n=n+1
        n=str(n)
        if str(n).count('8')>0 :
            print(int(n)-int(d))
            
            c=0
            break
        n=int(n)
    
        
    
        
    


    
