arr1=input()
arr2=input()
def replace(arr,index,element):
    for i in range(len(arr)):
        if i==index:
            arr[i]=element
        else:
            continue
    return arr
arr1=list(arr1)
arr2=list(arr2)
c=0
for i in range(len(arr1)-1):
    if arr1[i]=="0" and arr2[i]=="0" and arr2[i+1]=="0":
        c+=1
        arr1=replace(arr1,i,"X")
        arr2=replace(arr2,i, "X")
        arr2=replace(arr2,i+1, "X")
    elif arr1[i]=="0" and arr1[i+1]=="0" and arr2[i+1]=="0":
        c+=1
        arr1=replace(arr1,i, "X")
        arr1=replace(arr1,i+1, "X")
        arr2=replace(arr2,i + 1, "X")
    elif arr1[i]=="0" and arr1[i+1]=="0" and arr2[i]=="0":
        c+=1
        arr1=replace(arr1,i, "X")
        arr1=replace(arr1,i+1, "X")
        arr2=replace(arr2,i, "X")
    elif arr1[i+1]=="0" and arr2[i+1]=="0" and arr2[i]=="0":
        c+=1
        arr1=replace(arr1,i+1, "X")
        arr2=replace(arr2,i+1, "X")
        arr2=replace(arr2,i, "X")
print(c)


