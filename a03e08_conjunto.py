# Criando um conjunto
frutas = {"maçã", "banana", "laranja", "maçã"}
vazio = set()


# Operações
impares = {1, 3, 5, 7}
pares = {2, 4, 6, 8}

impares.union(pares) # União -> {1, 2, 3, 4, 5, 6, 7, 8}
impares.intersection(pares) # Interseção -> set()   (nenhum elemento em comum)
impares.difference(pares) # Diferença -> {1, 3, 5, 7}   (apenas os ímpares)
impares.symmetric_difference(pares) # Diferença simétrica -> {1, 2, 3, 4, 5, 6, 7, 8} 