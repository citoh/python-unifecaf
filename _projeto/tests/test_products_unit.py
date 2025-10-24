# Testes unitários para inserção direta de produtos via SQLAlchemy.

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.product import Product

def test_insercao_produto_simples(db_session):
    p = Product(name="Monitor", sku="MON-TEST", price=1234.56)
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)

    assert p.id is not None
    found = db_session.scalar(select(Product).where(Product.sku == "MON-TEST"))
    assert found is not None
    assert found.name == "Monitor"

def test_sku_unico(db_session):
    db_session.add(Product(name="A", sku="UNICO-1", price=10))
    db_session.commit()

    db_session.add(Product(name="B", sku="UNICO-1", price=20))
    try:
        db_session.commit()
        assert False, "Esperava IntegrityError por SKU duplicado"
    except Exception as e:
        db_session.rollback()
        # SQLAlchemy pode encapsular a IntegrityError dependendo do driver
        assert isinstance(e, IntegrityError) or "UNIQUE" in str(e).upper()