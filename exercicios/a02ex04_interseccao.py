# Retorne todos os números exitentes em ambas as listas
# Exemplo:
#   Entrada: 
#       ListaA = [4, 9, 3 , 7, 8]
#       Listab = [9, 5, 4 , 2, 1]
#   Saída Esperada: [9, 4]

def numeros_comuns(listaA, listaB):
    comuns = []
    for i in range(len(listaA)):
        for j in range(len(listaB)):
            if listaA[i] == listaB[j]:
                existente = False
                for k in range(len(comuns)):
                    if comuns[k] == listaA[i]:
                        existente = True
                        break
                if not existente:
                    comuns.append(listaA[i])
    return comuns


# Exemplo de uso
listaA = [4, 9, 3, 7, 8]
listaB = [9, 5, 4, 2, 1]
saida = numeros_comuns(listaA, listaB)

print("Lista A:", listaA)
print("Lista B:", listaB)
print("Saída:", saida)