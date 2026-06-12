def divi(n):
    if n == 0:
        return 0
    elif n == 1:
        return n
    elif n == 11:
        return 2
    elif n % 11 <= 6:
        k = n % 11
        j = 0
        cont_um = 0
        while j < n:
            j += 1
            cont_um += 1
        return cont_um
    else:
        k = n % 11
        h = 11
        contador_de_um = 2
        while h > n:
            h -= 1
            contador_de_um += 1
        return contador_de_um


def divide_maior(n):
    divisao = n // 11
    resto = n % 11
    valor_menor_que_onze = divi(resto)
    valor_maior_que_onze = divisao * 2
    return valor_maior_que_onze + valor_menor_que_onze


def execute():
    n = int(input())
    m = divide_maior(n)
    print(m)


execute()
