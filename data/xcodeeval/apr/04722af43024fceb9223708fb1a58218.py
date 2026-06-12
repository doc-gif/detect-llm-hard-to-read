


list1 = list(input())
list2 = list(input())


i=0
count=0
f1=0
up_u=0
d_u=0
if len(list1)==1:
    print(0)
    exit()
while i<len(list1)-1:
    if list1[i]=='0':

        if list1[i+1] =='0' and i+2<len(list1)-1 and list1[i+2]=='0':
            if list2[i]=='0' and list2[i+1]=='0' and list2[i+2]=='0':
                count+=2
                up_u=i+2
                d_u=i+2
                i+=3



        elif list1[i+1]=='0' and (list2[i+1]=='0' or list2[i]=='0'):
            up_u=i+1
            if list2[i]==0:
                d_u=i
            else:
                d_u=i+1
            count+=1
            i+=2


        elif list2[i]=='0' and list2[i+1]=='0':
            count+=1
            up_u=i
            d_u=i+1

            i+=2
        else:
            i+=1

    elif list2[i]=='0':
        if list2[i+1]=='0' and (list1[i+1]=='0'):
            count+=1
            up_u=i+1
            d_u=i+1
            i+=2
        else:
            i+=1
    else:
        i+=1

if list1[-1]=='0':

    if up_u<len(list1)-1:

        if d_u<len(list2)-2:
            if list2[-1]=='0' and list2[len(list2)-2]=='0':
                count+=1
print(count)

