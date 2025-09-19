# RESOLVIDO !!
# Coloque a aplicação dentro de um while para que rode infinitamente, 
# até que o usuário digite 0.
# Nessa aplicação crie um cadastro de clientes = {nome, idade} e
# com as seguintes operações:
# - Inserção de cliente
# - Busca por nome ou id (índice da lista)
# - Remoção 
# - Atualização
# - Listar Clientes
# - Sair
# Importante: ignore nomes iguais, mas caso exista considere apenas um sem muitos critérios.


# SOLUÇÃO
# Na solução abaixo foram desconsiderados os tratamentos de erros para simplicação 
# do entendimento do código

clientes = []  # lista global
opcao = ''


def Inserir():
    print('\nINSERIR NOVO CLIENTE')
    nome = input('Nome: ')
    idade = input('Idade: ')
    cliente = {"nome": nome, "idade": idade}
    clientes.append(cliente)
    Listar()


def Buscar():
    print('\nBUSCAR CLIENTE')
    busca = input('Digite o nome ou id do cliente: ')
    idEncontrado = None  # índice real (base 0)

    if busca.isdigit():  # busca por número/id
        idx = int(busca) - 1  # usuário digita começando em 1
        if 0 <= idx < len(clientes):
            c = clientes[idx]
            print(f"{idx+1} - Nome: {c['nome']}, Idade: {c['idade']}")
            idEncontrado = idx
    else:  # busca por nome
        for i, c in enumerate(clientes, 1):  # começa do 1 só para exibir
            if c["nome"] == busca:
                print(f"{i} - Nome: {c['nome']}, Idade: {c['idade']}")
                if idEncontrado is None:
                    idEncontrado = i - 1  # índice real
                break

    return idEncontrado


def Remover():
    idx = Buscar()
    if idx is not None:
        removido = clientes.pop(idx)
        print(f"Cliente removido: Nome={removido['nome']}, Idade={removido['idade']}")
    Listar()


def Atualizar():
    idx = Buscar()
    if idx is not None:
        nome = input("Nome: ")
        idade = input("Idade: ")
        clientes[idx] = {"nome": nome, "idade": idade}
        print("Cliente atualizado com sucesso!")
    Listar()


def Listar():
    print('\nLISTA DE CLIENTES')
    print("ID - Nome - Idade")
    for i, c in enumerate(clientes, 1):
        print(f"{i} - {c['nome']} - {c['idade']} anos")


operacoes = {
    '1': Inserir,
    '2': Buscar,
    '3': Remover,
    '4': Atualizar,
    '5': Listar,
}

# Interação do usuário
while opcao != '0':
    print('\n')
    print('CADASTRO CLIENTES')
    print('1 - Inserir')
    print('2 - Buscar por nome ou id')
    print('3 - Remover')
    print('4 - Atualizar')
    print('5 - Listar')
    print('0 - Sair')
    print('\n')

    opcao = input("Escolha uma opção: ").strip()

    if opcao in operacoes:
        operacoes[opcao]()
    elif opcao == '0':
        print("Encerrando aplicacao...")
    else:
        print("Opção inexistente")