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

from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ========================================================
# Configuração do banco SQLite (mesmo banco para toda a app)
# ========================================================
DATABASE_URL = "sqlite:///./db-console.sqlite3"  # arquivo no diretório atual

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necessário no SQLite p/ threads
    echo=False  # coloque True se quiser ver os SQLs no console
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# ========================================================
# Modelo ORM (tabela "clientes")
# ========================================================
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)   # não marcamos unique=True para simplificar
    idade = Column(Integer, nullable=False)

# Cria a tabela caso não exista
Base.metadata.create_all(bind=engine)

# ========================================================
# Funções auxiliares
# ========================================================
def get_db() -> Session:
    """Cria uma sessão do banco; use com try/finally ou with."""
    return SessionLocal()

def existe_nome(db: Session, nome: str) -> bool:
    """Retorna True se já existe um cliente com o mesmo nome."""
    return db.execute(select(Cliente).where(Cliente.nome == nome)).scalar_one_or_none() is not None

def listar_interno(db: Session):
    """Lista os clientes (uso interno)."""
    print('\nLISTA DE CLIENTES')
    print("ID - Nome - Idade")
    for c in db.execute(select(Cliente).order_by(Cliente.id)).scalars():
        print(f"{c.id} - {c.nome} - {c.idade} anos")

# ========================================================
# Operações do menu (CRUD)
# ========================================================
def Inserir():
    print('\nINSERIR NOVO CLIENTE')
    nome = input('Nome: ').strip()
    idade = input('Idade: ').strip()

    # Ignorar nomes iguais: se já existir, não inserir novamente
    with get_db() as db:
        if existe_nome(db, nome):
            print("Nome já existente. Ignorando inserção (conforme solicitado).")
        else:
            try:
                idade_int = int(idade)
            except ValueError:
                print("Idade inválida. Inserção ignorada.")
                listar_interno(db)
                return

            cliente = Cliente(nome=nome, idade=idade_int)
            db.add(cliente)
            db.commit()
            print(f"Cliente inserido: {cliente.nome} ({cliente.idade} anos)")

        listar_interno(db)


def Buscar():
    print('\nBUSCAR CLIENTE')
    busca = input('Digite o nome ou id do cliente: ').strip()

    with get_db() as db:
        encontrado = None
        if busca.isdigit():
            # busca por ID
            encontrado = db.get(Cliente, int(busca))
        else:
            # busca por nome (se houver duplicados, considera apenas um)
            encontrado = db.execute(
                select(Cliente).where(Cliente.nome == busca).limit(1)
            ).scalar_one_or_none()

        if encontrado:
            print(f"{encontrado.id} - Nome: {encontrado.nome}, Idade: {encontrado.idade}")
            return encontrado.id
        else:
            print("Cliente não encontrado.")
            return None


def Remover():
    id_cliente = Buscar()
    if id_cliente is not None:
        with get_db() as db:
            cliente = db.get(Cliente, id_cliente)
            if cliente:
                db.delete(cliente)
                db.commit()
                print(f"Cliente removido: Nome={cliente.nome}, Idade={cliente.idade}")
            listar_interno(db)


def Atualizar():
    id_cliente = Buscar()
    if id_cliente is not None:
        nome = input("Nome: ").strip()
        idade = input("Idade: ").strip()

        with get_db() as db:
            cliente = db.get(Cliente, id_cliente)
            if not cliente:
                print("Cliente não encontrado para atualização.")
                listar_interno(db)
                return

            # Se o novo nome já existe em outro registro, ignoramos a troca de nome
            # (mantemos simples conforme a instrução de 'ignorar nomes iguais')
            if nome and nome != cliente.nome and existe_nome(db, nome):
                print("Já existe cliente com esse nome. Mantendo o nome antigo.")

            try:
                idade_int = int(idade)
            except ValueError:
                print("Idade inválida. Atualização ignorada.")
                listar_interno(db)
                return

            # Atualiza somente o que for permitido
            if nome and (not existe_nome(db, nome) or nome == cliente.nome):
                cliente.nome = nome
            cliente.idade = idade_int

            db.commit()
            print("Cliente atualizado com sucesso!")
            listar_interno(db)


def Listar():
    with get_db() as db:
        listar_interno(db)

# ========================================================
# Loop principal (menu)
# ========================================================
operacoes = {
    '1': Inserir,
    '2': Buscar,
    '3': Remover,
    '4': Atualizar,
    '5': Listar,
}

opcao = ''
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