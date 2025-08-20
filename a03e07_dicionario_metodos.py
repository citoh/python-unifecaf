d = {"nome": "Ana", "idade": 25}

d.keys() # retorna todas as chaves
d.values() # retorna todos os valores
d.items() # retorna pares (chave, valor)

d.get("nome") # Ana
d.get("cidade", "SP") # retornará SP pois a chave não existe

d.pop("idade") # remove o item idade e retorna o valor

d.update({"cidade": "São Paulo", "nome": "Marcos"}) # adiciona ou atualiza pares
