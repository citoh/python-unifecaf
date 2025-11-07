# Ordene a lista de forma crescente
# Exemplo:
#   Entrada: [5, 7, 2 , 1]
#   Saída Esperada: [1, 2, 5, 7]


# USANDO ALGORITMOS CLÁSSICOS


#------------------------------------------------------
# Bubble Sort - método da bolha
def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                # troca
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista



#------------------------------------------------------
# Insertion Sort - ordenação como um jogo de baralho
def insertion_sort(lista):
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        # move os maiores para frente
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
    return lista



#------------------------------------------------------
# Merge Sort - uso de recursão
def merge_sort(lista):
    # Caso base: lista com 1 ou 0 elementos já está ordenada
    if len(lista) <= 1:
        return lista
    
    # Divide a lista em duas metades
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])
    
    # Combina (merge) as duas metades ordenadas
    return merge(esquerda, direita)


def merge(esquerda, direita):
    resultado = []
    i = j = 0
    
    # Intercala enquanto houver elementos nas duas listas
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] < direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    
    # Se sobrar elementos em uma das listas
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    
    return resultado



#------------------------------------------------------
# Quick Sort - uso de recursão
def quick_sort(lista):
    # Caso base: lista com 0 ou 1 elementos já está ordenada
    if len(lista) <= 1:
        return lista
    
    # Escolhe o pivô (aqui escolhi o último elemento)
    pivo = lista[-1]
    
    # Divide em duas listas: menores e maiores que o pivô
    menores = []
    maiores = []
    for i in range(len(lista) - 1):  # ignora o pivô
        if lista[i] <= pivo:
            menores.append(lista[i])
        else:
            maiores.append(lista[i])
    
    # Ordena recursivamente e concatena
    return quick_sort(menores) + [pivo] + quick_sort(maiores)



#------------------------------------------------------
# Iniciando ordenação
numeros = [5, 7, 2, 1]
print("Entrada:", numeros)
print("Bubble Sort:", bubble_sort(numeros))
print("Insertion Sort:", insertion_sort(numeros))
print("Merge Sort:", merge_sort(numeros))
print("Quick Sort:", quick_sort(numeros))