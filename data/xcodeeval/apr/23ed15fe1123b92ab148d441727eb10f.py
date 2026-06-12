primes = []

def list_primes_upto(upto :int):
    pcl = [1 for x in range(upto+1)]
    global primes
    primes = []
    if upto >= 2: primes.append(2)
    if upto >= 3: primes.append(3)
    for i in range(6, upto + 2, 6):
        if i-1 <= upto and pcl[i-1] == 1:
            primes.append(i-1)
            for k in range((i-1)**2, upto+1, (i-1)*2):
                pcl[k] = 0
        if i+1 <= upto and pcl[i+1] == 1:
            primes.append(i+1)
            for k in range((i+1)**2, upto+1, (i+1)*2):
                pcl[k] = 0
    return


t = int(input())

tests = []
for q in range(t):
    tests.append([int(x) for x in input().split()])

primes_limit = 0
for tp in tests:
    if tp[0]-tp[1] == 1:
        primes_limit = max(primes_limit, tp[0]+tp[1])

list_primes_upto(primes_limit)

for a, b in tests:
    yes = True
    if a-b != 1:
        yes = False
    if yes:
        apb = a+b
        is_apb_prime = True
        for p in primes:
            if not is_apb_prime or p >= apb:
                break
            is_apb_prime = is_apb_prime and (apb % p != 0)
        yes = yes and is_apb_prime
    print("YES" if yes else "NO")
