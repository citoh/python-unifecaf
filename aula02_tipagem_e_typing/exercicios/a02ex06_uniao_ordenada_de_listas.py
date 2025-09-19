# Una duas aleatórias listas em uma só com ordenação decrescente de valores
# Exemplo:
#   Entrada: 
#       ListaA = [1, 9, 4 , 5, 7, 2, 1]
#       Listab = [3, 2, 7 , 8, 6]
#   Saída Esperada: [9, 8, 7, 7, 6, 5, 4, 3, 2, 2, 1, 1]


# Função de Insertion Sort (ordenação decrescente)
def insertion_sort_dec(lista):
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] < chave:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
    return lista


#------------------------------------------------------
# Iniciando ordenação
listaA = [1, 9, 4, 5, 7, 2, 1]
listaB = [3, 2, 7, 8, 6]

saida = insertion_sort_dec(listaA + listaB)

print("Lista A:", listaA)
print("Lista B:", listaB)
print("Saída:", saida)