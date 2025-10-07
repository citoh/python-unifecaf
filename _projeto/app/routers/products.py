from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from pathlib import Path

from app.database import get_db, engine, Base
from app.models import Product
from app.helpers import format_brl_price

router = APIRouter()

Base.metadata.create_all(bind=engine)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.filters["brl_price"] = format_brl_price


@router.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/products", status_code=status.HTTP_302_FOUND)

# ---------------- FIXAS/SEMI-FIXAS PRIMEIRO ----------------

@router.get("/products")
def list_products(request: Request, db: Session = Depends(get_db)):
    products = db.scalars(select(Product).order_by(Product.id.desc())).all()
    return templates.TemplateResponse("products/index.html", {"request": request, "products": products})

@router.get("/products/new")
def new_product_form(request: Request):
    return templates.TemplateResponse(
        "products/new.html",
        {"request": request, "action": "/products", "method_override": "POST", "product": None},
    )

@router.get("/products/{product_id}/edit")
def edit_product_form(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return templates.TemplateResponse(
        "products/edit.html",
        {"request": request, "action": f"/products/{product.id}", "method_override": "PUT", "product": product},
    )

# ---------------- AÇÕES (POST/PUT/DELETE) ----------------

@router.post("/products")
def create_product(
    name: str = Form(...),
    sku: str = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db),
):
    if not name.strip() or not sku.strip():
        raise HTTPException(status_code=400, detail="Nome e SKU são obrigatórios")
    if db.scalar(select(Product).where(Product.sku == sku)):
        raise HTTPException(status_code=400, detail="SKU já cadastrado")
    db.add(Product(name=name.strip(), sku=sku.strip(), price=price))
    db.commit()
    return RedirectResponse(url="/products", status_code=status.HTTP_303_SEE_OTHER)

@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    name: str = Form(...),
    sku: str = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if db.scalar(select(Product).where(Product.sku == sku, Product.id != product_id)):
        raise HTTPException(status_code=400, detail="SKU já cadastrado para outro produto")
    product.name, product.sku, product.price = name.strip(), sku.strip(), price
    db.add(product); db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(product); db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

# ------------- DINÂMICA (DETALHE) POR ÚLTIMO ---------------

@router.get("/products/{product_id}")
def get_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return templates.TemplateResponse("products/show.html", {"request": request, "product": product})