import math
def isPrime(num):
    if num % 2 == 0:
        return False
    if num <= 3:
        return True
    a = int(math.sqrt(num)) + 1
    for x in range(3, a, 2):
        if num % x == 0:
            return False

    return True 
def solve(num):

    if isPrime(num):
        return [x for x in range(1, num - 1)]
    out = [1]
    factors = []
    for x in range(2, num):
        if not num % x == 0:
            out.append(x)
        else:
            factors.append(x)

    
    newout = []
    test = 1
    for x in out:
        factor = False
        for y in factors:
            if x % y == 0:
                factor = True
                break
        if not factor:
            test *= x
            newout.append(x)
    
    out = newout
    lose = test % num
    
    while lose != 1:
        test = 1
        newout = []
        for x in out:
            if not x % lose == 0:
                newout.append(x)
                test *= x

        lose = test % num    
        out = newout
    return out

if __name__ == "__main__":
    num = int(input())
    out = solve(num) 
    print(len(out))
    print(' '.join(str(x) for x in out))