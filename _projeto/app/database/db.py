from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Banco de dados local em SQLite (criado na raiz do projeto)
DATABASE_URL = "sqlite:///./projeto.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necessário para SQLite em apps async
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Base declarativa do SQLAlchemy."""
    pass

def get_db():
    """Dependency do FastAPI para obter/fechar sessão de banco por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()