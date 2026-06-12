def Ordenar(cadena1,cadena2,size):
    if(len(cadena1)==0):
        return cadena2
    else:
        if size%2==0:
            cadena2.append(cadena1.pop(int((len(cadena1)-1)/2)))
            Ordenar(cadena1, cadena2,size)
        else:
            cadena2.append(cadena1.pop(int(len(cadena1)/2)))
            Ordenar(cadena1, cadena2,size)
S=input()
Saux=[]
cadena=[]
for letra in S:
    Saux.append(letra)
Ordenar(Saux, cadena,len(S))
str1=''.join(cadena)
print(str1)