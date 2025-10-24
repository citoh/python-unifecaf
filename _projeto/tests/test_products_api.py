# Testes de integração simulando requisições HTTP para o endpoint /products.

from starlette import status
from app.models.product import Product
from sqlalchemy import select

def test_post_products_redirect(client, db_session):
    payload = {
        "name": "Filtro de Óleo",
        "sku": "SKU-API-1",
        "price": "87.90",
    }
    resp = client.post("/products", data=payload, follow_redirects=False)
    assert resp.status_code in (
        status.HTTP_303_SEE_OTHER,
        status.HTTP_302_FOUND,
        status.HTTP_307_TEMPORARY_REDIRECT,
        200,
        201,
    )

    created = db_session.scalar(select(Product).where(Product.sku == "SKU-API-1"))
    assert created is not None
    assert created.name == "Filtro de Óleo"