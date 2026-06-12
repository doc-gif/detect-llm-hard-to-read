multiplos_de_onze = [
    0,
    1,
    11,
    111,
    1111,
    11111,
    111111,
    1111111,
    11111111,
    111111111,
    1111111111,
    11111111111,
    111111111111,
    1111111111111,
    11111111111111,
    111111111111111,
    1111111111111111,
    11111111111111111,
]
def procura_onze(n, i):
    divisao = n // multiplos_de_onze[i]
    resto = n % multiplos_de_onze[i]
    if resto == 0:
        return divisao * i
    else:
        opcao1 = i + procura_onze(multiplos_de_onze[i] - resto, i - 1)
        opcao2 = procura_onze(resto, i - 1)
        return divisao * i + min(opcao1, opcao2)
def divide():
    n = int(input())
    m = procura_onze(n, 16)
    print(m)
divide()