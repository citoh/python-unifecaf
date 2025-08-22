carros = ["Fiat", "Chevrolet", "Volkswagen", "Ford", "Honda", "Toyota"]

carros.append("Audi") # adiciona UM item ao final

carros.extend(["BMW", "Mercedes"]) # adiciona VÁRIOS itens de outra lista
carros.insert(2, "Ferrari") # insere item em posição específica
carros.remove("Ford") # remove a PRIMEIRA ocorrência de um valor

carros.pop() # remove o último item e retorna o seu valor
carros.pop(1)  # também pode remover um item de posição específica

carros.clear() # clear -> remove TODOS os elementos

carros.sort() # sort -> ordena a lista em ordem alfabética
carros.sort(reverse=True) # com reverse=True a lista é ordenada de forma decrescente
carros.reverse() # reverse -> inverte a ordem atual