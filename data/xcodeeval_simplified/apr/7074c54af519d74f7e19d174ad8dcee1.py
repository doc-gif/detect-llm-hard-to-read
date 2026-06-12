import sys
import math
from decimal import *


def prime_generator(nr_elemente_prime):
    vector_prime = [-1] * nr_elemente_prime
    vector_rasp = [0] * nr_elemente_prime
    vector_prime[1] = 1
    vector_rasp[1] = 1
    contor = 2
    for i in range(2, nr_elemente_prime):
        if vector_prime[i] == -1:
            vector_prime[i] = 1
            vector_rasp[contor] = i
            contor = contor + 1
        for j in range(i + i, nr_elemente_prime, i):
            if vector_prime[j] == -1:
                vector_prime[j] = i
    set_prime = set(vector_rasp)
    sume_disponibile = set()
    for i in range(3, nr_elemente_prime):
        sume_disponibile.add(vector_rasp[i - 1] + vector_rasp[i])
    rasp_final = ""


def transformare_baza(numar, baza):
    transformare = ""
    while numar >= baza:
        rest = numar % baza
        numar = numar // baza
        transformare += str(rest)
    transformare += str(numar)
    noua_baza = transformare[::-1]
    return noua_baza


def bitwise_xor(a, b):
    stringul_1 = transformare_baza(a, 2)
    stringul_2 = transformare_baza(b, 2)
    lungime = max(len(stringul_1), len(stringul_2))
    raspunsul = 0
    str_answ = [0] * lungime
    for i in range(0, lungime):
        j = lungime - 1 - i
        if len(stringul_1) > i and len(stringul_2) > i:
            if (
                stringul_1[len(stringul_1) - 1 - i]
                != stringul_2[len(stringul_2) - 1 - i]
            ):
                raspunsul += 2 ** (i)
                str_answ[i] = "1"
        elif len(stringul_1) > i and stringul_1[len(stringul_1) - 1 - i] == "1":
            raspunsul += 2 ** (i)
            str_answ[i] = "1"
        elif len(stringul_2) > i and stringul_2[len(stringul_2) - 1 - i] == "1":
            raspunsul += 2 ** (i)
            str_answ[i] = "1"
    return raspunsul


def bitwise_or(a, b):
    stringul_1 = transformare_baza(a, 2)
    stringul_2 = transformare_baza(b, 2)
    lungime = max(len(stringul_1), len(stringul_2))
    raspunsul = 0
    str_answ = [0] * lungime
    for i in range(0, lungime):
        j = lungime - 1 - i
        if len(stringul_1) > i and len(stringul_2) > i:
            if (
                stringul_1[len(stringul_1) - 1 - i] == "1"
                or stringul_2[len(stringul_2) - 1 - i] == "1"
            ):
                raspunsul += 2 ** (i)
                str_answ[i] = "1"
        elif len(stringul_1) > i and stringul_1[len(stringul_1) - 1 - i] == "1":
            raspunsul += 2 ** (i)
            str_answ[i] = "1"
        elif len(stringul_2) > i and stringul_2[len(stringul_2) - 1 - i] == "1":
            raspunsul += 2 ** (i)
            str_answ[i] = "1"
    return raspunsul


def exclusive_or(a, b):
    stringul_1 = transformare_baza(min(a, b), 2)
    stringul_2 = transformare_baza(max(a, b), 2)
    lungime = max(len(stringul_1), len(stringul_2))
    raspunsul = 0
    str_answ = [0] * lungime
    for i in range(0, lungime):
        if len(stringul_1) > i and len(stringul_2) > i:
            if (
                stringul_1[len(stringul_1) - 1 - i]
                != stringul_2[len(stringul_2) - 1 - i]
            ):
                raspunsul += 2 ** (i)
                str_answ[i] = "1"
            else:
                str_answ[i] = "0"
        else:
            if stringul_2[len(stringul_2) - 1 - i] == "1":
                raspunsul += 2 ** (i)
                str_answ[i] = "1"
            else:
                str_answ[i] = "0"
    return raspunsul


factorial = [0] * 21
factorial[0] = 1
factorial[1] = 1
constanta = 10**9 + 7
z = int(input())
for contorr in range(z):
    n, k = list(map(int, input().split()))
    if n > 2**k:
        print(0)
    else:
        if n == 1:
            print(1)
        elif n == 2:
            answ = (2 ** (k)) % constanta
            print(answ)
        else:
            answ = (n ** (k)) % constanta
            print(answ)
