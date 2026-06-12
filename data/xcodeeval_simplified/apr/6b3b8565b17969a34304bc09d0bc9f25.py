def divi(n):
    if n == 0:
        return 0
    elif n == 1:
        return n
    elif n == 11:
        return 2
    elif n % 11 <= 6:
        k = n % 11
        count = 0
        for _ in range(n):
            count += 1
        return count
    else:
        k = n % 11
        h = 11
        count = 2
        while h > n:
            h -= 1
            count += 1
        return count


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
