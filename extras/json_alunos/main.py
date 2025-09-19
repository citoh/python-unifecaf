# INSTALANDO A APLICAÇÃO:
# python3 -m venv venv
# source venv/bin/activate
# pip install pandas openpyxl

import json
import pandas as pd
import os

# -------- LENDO ARQUIVO alunos.json --------

base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, "alunos.json")

with open(json_path, "r", encoding="utf-8") as f:
    alunos = json.load(f)




# -------- OPERAÇÕES --------

def buscar_por_nome(nome):
    for aluno in alunos:
        if aluno["nome"].lower() == nome.lower():
            return aluno
    return None

def listar_aprovados():
    return sorted([a for a in alunos if a["nota"] >= 6.0], key=lambda a: a["nome"])

def listar_reprovados():
    return sorted([a for a in alunos if a["nota"] < 6.0], key=lambda a: a["nome"])

def exportar_para_excel(registros, nome_arquivo):
    if not registros:
        print("Não há dados para exportar.")
        return
    df = pd.DataFrame(registros)
    path = os.path.join(base_dir, nome_arquivo)
    df.to_excel(path, index=False)
    print(f"Arquivo exportado com sucesso: {path}")

def imprimir_lista(lista, titulo):
    print(f"\n\n========== {titulo} ==========\n")
    for a in lista:
        print(f"{a['nome']} - Nota: {a['nota']}")



# -------- ACOES DE MENU --------

def acao_buscar(estado):
    nome = input("Digite o nome do aluno: ")
    aluno = buscar_por_nome(nome)
    if aluno:
        print(f"Aluno encontrado: {aluno['nome']} - Nota: {aluno['nota']}")
        estado["ultimo"] = [aluno]
    else:
        print("Aluno não encontrado.")
        estado["ultimo"] = []
    return estado

def acao_aprovados(estado):
    lista = listar_aprovados()
    imprimir_lista(lista, "Aprovados")
    estado["ultimo"] = lista
    return estado

def acao_reprovados(estado):
    lista = listar_reprovados()
    imprimir_lista(lista, "Reprovados")
    estado["ultimo"] = lista
    return estado

def acao_exportar(estado):
    print("\n\n========== Exportação ==========\n")
    print("1 - Exportar TODOS os alunos")
    print("2 - Exportar apenas APROVADOS")
    print("3 - Exportar apenas REPROVADOS")
    print("4 - Exportar o ÚLTIMO RESULTADO mostrado")
    sub = input("Escolha: ")

    export_map = {
        "1": lambda: exportar_para_excel(alunos, "alunos.xlsx"),
        "2": lambda: exportar_para_excel(listar_aprovados(), "alunos_aprovados.xlsx"),
        "3": lambda: exportar_para_excel(listar_reprovados(), "alunos_reprovados.xlsx"),
        "4": lambda: exportar_para_excel(estado.get("ultimo", []), "alunos_ultimo_resultado.xlsx"),
    }
    (export_map.get(sub, lambda: print("Opção de exportação inválida.")))()
    return estado

def acao_sair(_):
    print("Encerrando o programa.")
    raise SystemExit

def acao_invalida(estado):
    print("Opção inválida, tente novamente.")
    return estado




# -------- INTERAÇÕES COM O USUÁRIO --------
if __name__ == "__main__":
    estado = {"ultimo": []}

    menu_actions = {
        "1": acao_buscar,
        "2": acao_aprovados,
        "3": acao_reprovados,
        "4": acao_exportar,
        "0": acao_sair
    }

    while True:
        print("\n\n========== MENU ==========\n")
        print("1 - Buscar por nome")
        print("2 - Listar aprovados")
        print("3 - Listar reprovados")
        print("4 - Exportar para Excel")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")
        acao = menu_actions.get(opcao, acao_invalida)
        estado = acao(estado)
        input('\n\nPressione qualquer tecla para continuar')