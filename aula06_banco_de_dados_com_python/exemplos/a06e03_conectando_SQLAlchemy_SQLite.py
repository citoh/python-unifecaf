from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Conexão com SQLite (arquivo será criado se não existir)
engine = create_engine("sqlite:///teste2.db", echo=True)

# Base declarativa
Base = declarative_base()

# Modelo Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)

# Criar tabela
Base.metadata.create_all(engine)
print("Tabela criada com sucesso!")

# Criar sessão
Session = sessionmaker(bind=engine)
session = Session()

# Inserindo dados
novo = Usuario(nome="Ana", email="ana@email.com")
session.add(novo)
session.commit()

# Consultando dados
usuarios = session.query(Usuario).all()
for u in usuarios:
    print(u.id, u.nome, u.email)

# Fechando sessão
session.close()