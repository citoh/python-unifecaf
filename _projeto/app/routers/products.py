# Importações principais do FastAPI
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette import status

# ORM e utilitários de banco de dados
from sqlalchemy.orm import Session
from sqlalchemy import select
from pathlib import Path

# Importações do projeto
from app.database import get_db, engine, Base
from app.models import Product
from app.helpers import format_brl_price, format_brl_date 

# Cria o roteador de produtos
router = APIRouter()

# Cria as tabelas do banco na primeira importação do módulo
Base.metadata.create_all(bind=engine)

# Configuração de diretório de templates
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Adiciona o filtro para formatação de preço (ex: 1.500,00)
templates.env.filters["brl_price"] = format_brl_price
templates.env.filters["brl_date"] = format_brl_date


# ------------------------------------------------------------------
# Redireciona a raiz "/" para "/products"
# ------------------------------------------------------------------
@router.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/products", status_code=status.HTTP_302_FOUND)


# ------------------------------------------------------------------
# LISTAR PRODUTOS (GET)
# Exibe a lista completa de produtos cadastrados
# ------------------------------------------------------------------
@router.get("/products")
def list_products(request: Request, db: Session = Depends(get_db)):
    # Busca todos os produtos, ordenando do mais recente para o mais antigo
    products = db.scalars(select(Product).order_by(Product.id.desc())).all()
    # Renderiza a página de listagem
    return templates.TemplateResponse(
        "products/index.html",
        {"request": request, "products": products}
    )


# ------------------------------------------------------------------
# FORMULÁRIO DE NOVO PRODUTO (GET)
# Exibe o formulário vazio para cadastro de um novo produto
# ------------------------------------------------------------------
@router.get("/products/new")
def new_product_form(request: Request):
    return templates.TemplateResponse(
        "products/new.html",
        {
            "request": request,
            "action": "/products",             # rota de envio do formulário
            "method_override": "POST",         # método HTTP utilizado
            "product": None                    # sem produto (novo cadastro)
        }
    )


# ------------------------------------------------------------------
# FORMULÁRIO DE EDIÇÃO DE PRODUTO (GET)
# Exibe o formulário preenchido com os dados de um produto existente
# ------------------------------------------------------------------
@router.get("/products/{product_id}/edit")
def edit_product_form(product_id: int, request: Request, db: Session = Depends(get_db)):
    # Busca o produto pelo ID
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Renderiza o formulário com dados preenchidos
    return templates.TemplateResponse(
        "products/edit.html",
        {
            "request": request,
            "action": f"/products/{product.id}",  # rota para envio da atualização
            "method_override": "PUT",             # método de atualização
            "product": product
        }
    )


# ------------------------------------------------------------------
# CRIAÇÃO DE PRODUTO (POST)
# Recebe os dados do formulário e insere um novo registro no banco
# ------------------------------------------------------------------
@router.post("/products")
def create_product(
    name: str = Form(...),
    sku: str = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db),
):
    # Validação simples de campos obrigatórios
    if not name.strip() or not sku.strip():
        raise HTTPException(status_code=400, detail="Nome e SKU são obrigatórios")

    # Verifica se já existe um produto com o mesmo SKU
    if db.scalar(select(Product).where(Product.sku == sku)):
        raise HTTPException(status_code=400, detail="SKU já cadastrado")

    # Cria o objeto e salva no banco
    db.add(Product(name=name.strip(), sku=sku.strip(), price=price))
    db.commit()

    # Redireciona para a listagem de produtos
    return RedirectResponse(url="/products", status_code=status.HTTP_303_SEE_OTHER)


# ------------------------------------------------------------------
# ATUALIZAÇÃO DE PRODUTO (PUT)
# Atualiza os dados de um produto existente
# ------------------------------------------------------------------
@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    name: str = Form(...),
    sku: str = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db),
):
    # Busca o produto pelo ID
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Verifica se o SKU já pertence a outro produto
    if db.scalar(select(Product).where(Product.sku == sku, Product.id != product_id)):
        raise HTTPException(status_code=400, detail="SKU já cadastrado para outro produto")

    # Atualiza os campos
    product.name = name.strip()
    product.sku = sku.strip()
    product.price = price

    # Confirma no banco
    db.add(product)
    db.commit()

    # Retorna sucesso sem conteúdo (204)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


# ------------------------------------------------------------------
# EXCLUSÃO DE PRODUTO (DELETE)
# Remove um produto do banco de dados
# ------------------------------------------------------------------
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Busca o produto pelo ID
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Remove e confirma
    db.delete(product)
    db.commit()

    # Retorna sucesso sem conteúdo (204)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


# ------------------------------------------------------------------
# DETALHE DE PRODUTO (GET)
# Exibe os dados detalhados de um produto específico
# ------------------------------------------------------------------
@router.get("/products/{product_id}")
def get_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    # Busca o produto pelo ID
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Renderiza a página de detalhes
    return templates.TemplateResponse(
        "products/show.html",
        {"request": request, "product": product}
    )