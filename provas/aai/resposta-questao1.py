# Somar os números pares de 1 a n
def soma_pares(n):
    soma = 0
    for i in range(1, n+1):
        if i % 2 == 0:
            soma += i
    return soma


# Contar quantos números negativos existem em uma lista
def contar_negativos(lista):
    count = 0
    for num in lista:
        if num < 0:
            count += 1
    return count


# Retornar o maior número de uma lista
def maior_numero(lista):
    maior = lista[0]
    for num in lista:
        if num > maior:
            maior = num
    return maior


# Inverter uma string
def inverter_string(s):
    invertida = ""  
    for letra in s:
        invertida = letra + invertida 
    return invertida


# Contar quantas vezes a letra “a” aparece em uma palavra
def contar_a(palavra):
    count = 0
    for letra in palavra:
        if letra.lower() == "a":
            count += 1
    return count