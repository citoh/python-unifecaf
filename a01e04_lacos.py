# Lista de alunos (intercalando homem e mulher)
alunos = [
    {"nome": "Lucas",   "nota": 8.5},
    {"nome": "Ana",     "nota": 6.0},
    {"nome": "Rafael",  "nota": 7.5},
    {"nome": "Beatriz", "nota": 9.0},
    {"nome": "Mateus",  "nota": 5.5},
    {"nome": "Carla",   "nota": 7.8},
    {"nome": "João",    "nota": 4.0},
    {"nome": "Lívia",   "nota": 10.0},
    {"nome": "Pedro",   "nota": 7.1},
    {"nome": "Marina",  "nota": 6.9}
]

# Ordenar alunos por nome
alunos_ordenados = sorted(alunos, key=lambda aluno: aluno["nome"])

# Mostrar todos os alunos com suas notas
print("Notas dos alunos (ordem alfabética):\n")
for aluno in alunos_ordenados:
    print(f"{aluno['nome']}: {aluno['nota']}")

# Filtrar aprovados pois possuem nota maior que 7
aprovados = []
for a in alunos_ordenados :
    if a["nota"] > 7 :
        aprovados.append(a)

# Mostrar os aprovados ordenados por nome
print("\nAlunos aprovados (nota > 7) - ordenados por nome:\n")
for aluno in aprovados:
    print(f"{aluno['nome']} - Nota: {aluno['nota']}")


# Mostrar os aprovados ordenados por média
print("\nAlunos aprovados (nota > 7) - ordenados por nome:\n")
######## CRIE O ALGORITMO ########


# Outras formas de usar o laço:

# aprovados = [a for a in alunos_ordenados if a["nota"] > 7]

# for i, aluno in enumerate(alunos, start=1):
#    print(f"{i}º aluno: {aluno['nome']} - Nota: {aluno['nota']}")