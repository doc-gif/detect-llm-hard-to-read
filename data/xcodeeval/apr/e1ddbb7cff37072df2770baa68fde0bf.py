#bayan bus c328

from sys import stdin

def bayan():
    while True:
        n=int(stdin.readline().strip())
        if n=="":
            break
        else:
            mat=[["#","#","#","#","#","#","#","#","#","#","#"],["#","#","#","#","#","#","#","#","#","#","#"],["#","","","","","","","","","",""],["#","#","#","#","#","#","#","#","#","#","#"]]
            mat=pasajero(n,mat)
            imp(mat)

def pasajero(n,mat):
    col=0
    while col<=10:
        fila=0
        while fila<=3:
            if n==0:
                break
            else:
                if fila==2 and col>0:
                    n=n+1
                else:
                    mat[fila][col]="O"
            n-=1
            fila+=1
        col+=1
    return mat
def imp(mat):
    f1=mat[0]
    f2=mat[1]
    f3=mat[2]
    f4=mat[3]
    f1=".".join(f1)
    f2=".".join(f2)
    f3=".".join(f3)
    f4=".".join(f4)
    print("+"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"+")
    print("|"+f1+"."+"|"+"D"+"|"+")")
    print("|"+f2+"."+"|"+"."+"|")
    print("|"+f3+"."+"."+"."+"."+"."+"."+"."+"."+"."+"."+"."+"."+"."+"|")
    print("|"+f4+"."+"|"+"."+"|"+")")
    print("+"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"-"+"+")

    
    
            
bayan()
