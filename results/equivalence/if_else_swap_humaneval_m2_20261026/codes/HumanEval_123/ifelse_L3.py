from typing import *
def get_odd_collatz(n):
    if not (n%2==0):
        odd_collatz = [n]
    else:
        odd_collatz = [] 
    while n > 1:
        if n % 2 == 0:
            n = n/2
        else:
            n = n*3 + 1
            
        if n%2 == 1:
            odd_collatz.append(int(n))

    return sorted(odd_collatz)
