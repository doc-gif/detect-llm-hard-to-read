first = int (input ())

num = [first]

visit1 = 0
while True :
    

    
    if first == 1:
        visit1 += 1
    if visit1 == 2 :
        break

    first = first +1
    while first % 10 == 0:
        first = first //10
    
    if first not in num:
        num.append(first)
    
    
    

    

#num.sort()
#print (num)
print (len(num))
    
