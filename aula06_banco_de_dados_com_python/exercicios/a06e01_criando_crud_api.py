# RESOLVIDO !! Utilizando FastAPI
# Crie um banco de dados e depois a 4 funções para um CRUD
# C - create (criar ou inserir)
# R - read (ler dados, listar ou buscar)
# U - update (atualizar)
# D - delete (apagar um ou mais dados)

from typing import List, Generator, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

# 1) Configuração da aplicação FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Configuração do banco de dados SQLite + SQLAlchemy
DATABASE_URL = "sqlite:///./db-api.sqlite3"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # exigido pelo SQLite
    echo=False  # coloque True se quiser ver os SQLs no console
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

# Modelo ORM principal da tabela users
class User(Base):
    __tablename__ = "users"   # nome da tabela no banco

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

# Cria a tabela no banco (se não existir)
Base.metadata.create_all(bind=engine)

# Gera/fecha sessões automaticamente por request
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3) Schemas Pydantic
class UserRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)  # ORM -> Pydantic

class UserCreate(BaseModel):
    name: str

class UserUpdate(BaseModel):
    name: str

# 4) Helper de resposta JSON UTF-8
def utf8_json_response(content, status_code=200):
    return JSONResponse(
        content=content,
        status_code=status_code,
        media_type="application/json; charset=utf-8"
    )

# 5) Rotas CRUD

# GET - listar todos os usuários
@app.get("/users", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    users = db.execute(select(User)).scalars().all()
    return utf8_json_response([UserRead.model_validate(u).model_dump() for u in users])

# GET - buscar usuário pelo ID
@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user: Optional[User] = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return utf8_json_response(UserRead.model_validate(user).model_dump())

# POST - criar usuário (só recebe name, id é autogerado)
@app.post("/users", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(name=payload.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return utf8_json_response(UserRead.model_validate(user).model_dump(), status_code=201)

# PUT - atualizar nome de usuário
@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user: Optional[User] = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.name = data.name
    db.commit()
    db.refresh(user)
    return utf8_json_response(UserRead.model_validate(user).model_dump())

# DELETE - remover usuário
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user: Optional[User] = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
    return utf8_json_response({"msg": f"Usuário {user_id} removido"})

# 6) Iniciar servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "a06e01_criando_crud_api:app",  # arquivo:variável
        host="127.0.0.1",
        port=3344,
        reload=True
    )