# Responsável por configurar o ambiente de testes, incluindo o banco SQLite isolado e o override de dependências do FastAPI.

# --- garantir que a raiz do projeto esteja no PYTHONPATH ---
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]  # .../_projeto
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# -----------------------------------------------------------

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app
from app.database import Base, get_db
from app.models.product import Product

@pytest.fixture(scope="session")
def engine():
    # Banco isolado para testes (arquivo para permitir múltiplas conexões do TestClient)
    engine = create_engine("sqlite:///./test_projeto.db", connect_args={"check_same_thread": False})
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture
def db_session(engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(autouse=True)
def override_get_db(db_session):
    def _get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)