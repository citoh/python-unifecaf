# RESOLVIDO !!
# Retorne todos os números repetidos de uma lista de números
# Exemplo:
#   Entrada: [6, 1, 1, 7, 2 , 6, 1]
#   Saída Esperada: [6, 1]

def numeros_repetidos(lista):
    repetidos = []
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                existente = False
                for k in range(len(repetidos)):
                    if repetidos[k] == lista[i]:
                        existente = True
                        break
                if not existente:
                    repetidos.append(lista[i])
    return repetidos


numeros = [6, 1, 1, 7, 2, 6, 1]
print(numeros_repetidos(numeros))