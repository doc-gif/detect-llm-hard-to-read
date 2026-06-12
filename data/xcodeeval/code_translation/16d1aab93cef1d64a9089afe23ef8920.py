l=list(input())
if(len(l)<=3 and int("".join(l))>(-129) and int("".join(l))<=127):
    print("byte")
elif(len(l)<=5 and int("".join(l))>(-32769) and int("".join(l))<=32767):
    print("short")
elif(len(l)<=10 and int("".join(l))>(-2147483649) and int("".join(l))<=2147483647):
    print("int")
elif(len(l)<=19 and int("".join(l))>(-9223372036854775809 ) and int("".join(l))<=9223372036854775807 ):
    print("long")
else:
    print("BigInteger")
