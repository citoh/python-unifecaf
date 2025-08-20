# RESOLVIDO !!
# Retorne apenas os números pares de uma lista de números
# Exemplo:
#   Entrada: [9, 4, 7 , 2, 1]
#   Saída Esperada: [4, 2]

def numeros_pares(lista):
    pares = []
    for i in range(len(lista)):
        if lista[i] % 2 == 0:
            pares.append(lista[i])
    return pares


numeros = [9, 4, 7, 2, 1]
print(numeros_pares(numeros))