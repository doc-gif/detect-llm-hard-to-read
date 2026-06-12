x = input().split()      
 
hazZero = False

binary = bin(int(x[0]))
binary = binary[2:]

for i in range(len(binary)):
    if (binary[i] == '0'):
        hazZero = True

if (not hazZero):
    binary = bin(int(x[0]) + 1)
    binary = binary[2:]
 
isFirst = True
new_binary = ''
 
for i in range(len(binary)):
    if (binary[i] == '0'):
        if (isFirst):
            new_binary = new_binary + '0'
            isFirst = False
        else:
            new_binary = new_binary + '1'
    else:          
        new_binary = new_binary + binary[i]
 
inDecimal = int(new_binary, 2)
 
total = 0
 
while (int(x[0]) <= inDecimal and inDecimal <= int(x[1]) ):
    total += 1
    if (new_binary == '1'):
        total -= 1
        new_binary = '10'
    elif (new_binary[-1] == '0'):
        new_binary = '10' + new_binary[:-1]
    else:    
        new_binary = '1' + new_binary[:-1]
    inDecimal = int(new_binary, 2)
 
print(total)