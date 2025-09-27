# Pede para o usuário digitar o RA (Registro Acadêmico)
ra = input("Digite o seu RA: ")

# Pega o primeiro dígito do RA e converte para inteiro
acum = int(ra[0])

# Percorre os demais dígitos do RA (do índice 1 até o último)
for i in range(1, len(ra)):
    # Converte o dígito atual para inteiro
    n = int(ra[i])

    # Se o dígito for par, soma ao acumulador
    if n % 2 == 0:
        acum += n
        
    # Se o dígito for ímpar, multiplica pelo acumulador
    else:
        acum *= n

# Mostra o resultado final
print(acum)



# SIMULANDO ALGORITMO
#
# RA = 12345
# Passo 1 -> acum = 1
# Passo 2 -> n = 2 (par) -> acum = 1 + 2 = 3
# Passo 3 -> n = 3 (ímpar) -> acum = 3 * 3 = 9
# Passo 4 -> n = 4 (par) -> acum = 9 + 4 = 13
# Passo 5 -> n = 5 (ímpar) -> acum = 13 * 5 = 65
# Saída final: 65