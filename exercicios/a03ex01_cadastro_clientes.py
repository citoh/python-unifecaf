# Coloque a aplicação dentro de um while para que rode infinitamente, 
# até que o usuário digite 0.
# Nessa aplicação crie um cadastro de clientes = {nome, idade} e
# com as seguintes operações:
# - Inserção de cliente
# - Busca por nome ou id (índice da lista)
# - Remoção 
# - Atualização
#
# Importante: ignore nomes iguais, mas caso exista considere apenas um sem muitos critérios.

# Cadastro de clientes
clientes = []

while True:
    print("\n--- Sistema de Cadastro de Clientes ---")
    print("1 - Inserir cliente")
    print("2 - Buscar cliente (por nome ou índice)")
    print("3 - Remover cliente")
    print("4 - Atualizar cliente")
    print("5 - Listar clientes")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "0":
        print("Encerrando o sistema... Até logo!")
        break

    elif opcao == "1":  # Inserção
        nome = input("Digite o nome do cliente: ")
        idade = input("Digite a idade do cliente: ")

        # Impede duplicados simples
        existe = any(c["nome"].lower() == nome.lower() for c in clientes)
        if existe:
            print("Cliente já cadastrado, ignorando.")
        else:
            clientes.append({"nome": nome, "idade": idade})
            print(f"Cliente {nome} adicionado com sucesso!")

    elif opcao == "2":  # Busca
        busca = input("Digite o nome ou índice do cliente: ")
        encontrado = None

        if busca.isdigit():
            idx = int(busca)
            if 0 <= idx < len(clientes):
                encontrado = clientes[idx]
        else:
            for c in clientes:
                if c["nome"].lower() == busca.lower():
                    encontrado = c
                    break

        if encontrado:
            print("Cliente encontrado:", encontrado)
        else:
            print("Cliente não encontrado.")

    elif opcao == "3":  # Remoção
        busca = input("Digite o nome ou índice do cliente a remover: ")

        if busca.isdigit():
            idx = int(busca)
            if 0 <= idx < len(clientes):
                removido = clientes.pop(idx)
                print(f"Cliente {removido['nome']} removido.")
            else:
                print("Índice inválido.")
        else:
            for i, c in enumerate(clientes):
                if c["nome"].lower() == busca.lower():
                    removido = clientes.pop(i)
                    print(f"Cliente {removido['nome']} removido.")
                    break
            else:
                print("Cliente não encontrado.")

    elif opcao == "4":  # Atualização
        busca = input("Digite o nome ou índice do cliente a atualizar: ")
        idx = None

        if busca.isdigit():
            idx = int(busca) if 0 <= int(busca) < len(clientes) else None
        else:
            for i, c in enumerate(clientes):
                if c["nome"].lower() == busca.lower():
                    idx = i
                    break

        if idx is not None:
            print(f"Cliente atual: {clientes[idx]}")
            novo_nome = input("Novo nome (pressione Enter para manter): ")
            nova_idade = input("Nova idade (pressione Enter para manter): ")

            if novo_nome.strip():
                clientes[idx]["nome"] = novo_nome
            if nova_idade.strip():
                clientes[idx]["idade"] = nova_idade

            print("Cliente atualizado com sucesso!")
        else:
            print("Cliente não encontrado.")

    elif opcao == "5":  # Listagem
        if clientes:
            print("\n--- Lista de Clientes ---")
            for i, c in enumerate(clientes):
                print(f"{i} - Nome: {c['nome']}, Idade: {c['idade']}")
        else:
            print("Nenhum cliente cadastrado.")

    else:
        print("Opção inválida, tente novamente.")
1