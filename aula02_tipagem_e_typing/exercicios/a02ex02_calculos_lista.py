# RESOLVIDO !!
# Dada uma lista de números, calcule:
#   - a soma de todos os números
#   - a média de todos os números
#   - O maior número
#   - o menor número 

def calcular_soma(lista):
    soma = 0
    for i in range(len(lista)):
        soma += lista[i]
    return soma

def calcular_media(lista):
    soma = calcular_soma(lista)
    return soma / len(lista)

def encontrar_maior(lista):
    maior = lista[0]
    for i in range(1, len(lista)):
        if lista[i] > maior:
            maior = lista[i]
    return maior

def encontrar_menor(lista):
    menor = lista[0]
    for i in range(1, len(lista)):
        if lista[i] < menor:
            menor = lista[i]
    return menor


numeros = [9, 4, 7, 2, 1]

print("Lista:", numeros)
print("Soma:", calcular_soma(numeros))
print("Média:", calcular_media(numeros))
print("Maior número:", encontrar_maior(numeros))
print("Menor número:", encontrar_menor(numeros))