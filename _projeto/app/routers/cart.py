from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select
from pathlib import Path

from app.database import get_db
from app.models import Cart, CartItem, Product, User
from app.dependencies import get_current_user
from app.helpers import format_brl_price

router = APIRouter()

# Configuração de diretório de templates
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.filters["brl_price"] = format_brl_price


def get_or_create_cart(user_id: int, db: Session) -> Cart:
    """Obtém ou cria o carrinho do usuário."""
    cart = db.scalar(select(Cart).where(Cart.user_id == user_id))
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/cart")
def view_cart(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Exibe o carrinho do usuário."""
    if current_user.is_admin():
        raise HTTPException(status_code=403, detail="Administradores não têm acesso ao carrinho")
    
    cart = get_or_create_cart(current_user.id, db)
    
    # Recarrega os itens com os produtos
    items = db.scalars(
        select(CartItem)
        .where(CartItem.cart_id == cart.id)
        .order_by(CartItem.created_at.desc())
    ).all()
    
    # Força o carregamento dos produtos
    for item in items:
        _ = item.product
    
    return templates.TemplateResponse(
        "cart/view.html",
        {
            "request": request,
            "cart": cart,
            "items": items,
            "total": cart.get_total(),
            "current_user": current_user,
        }
    )


@router.post("/cart/add/{product_id}")
def add_to_cart(
    product_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    quantity: int = Form(default=1),
):
    """Adiciona um produto ao carrinho."""
    if current_user.is_admin():
        raise HTTPException(status_code=403, detail="Administradores não podem adicionar produtos ao carrinho")
    
    # Verifica se o produto existe
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Obtém ou cria o carrinho
    cart = get_or_create_cart(current_user.id, db)
    
    # Verifica se o item já existe no carrinho
    existing_item = db.scalar(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
    )
    
    if existing_item:
        # Atualiza a quantidade
        existing_item.quantity += quantity
        db.add(existing_item)
    else:
        # Cria novo item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
        )
        db.add(cart_item)
    
    db.commit()
    
    # Redireciona de volta para a página de produtos ou carrinho
    referer = request.headers.get("referer", "/products")
    return RedirectResponse(url=referer, status_code=status.HTTP_303_SEE_OTHER)


@router.post("/cart/remove/{item_id}")
def remove_from_cart(
    item_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove um item do carrinho."""
    if current_user.is_admin():
        raise HTTPException(status_code=403, detail="Administradores não têm acesso ao carrinho")
    
    # Busca o item
    item = db.get(CartItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    # Verifica se o item pertence ao carrinho do usuário
    cart = get_or_create_cart(current_user.id, db)
    if item.cart_id != cart.id:
        raise HTTPException(status_code=403, detail="Item não pertence ao seu carrinho")
    
    # Remove o item
    db.delete(item)
    db.commit()
    
    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/cart/update/{item_id}")
def update_cart_item(
    item_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    quantity: int = Form(...),
):
    """Atualiza a quantidade de um item no carrinho."""
    if current_user.is_admin():
        raise HTTPException(status_code=403, detail="Administradores não têm acesso ao carrinho")
    
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")
    
    # Busca o item
    item = db.get(CartItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    # Verifica se o item pertence ao carrinho do usuário
    cart = get_or_create_cart(current_user.id, db)
    if item.cart_id != cart.id:
        raise HTTPException(status_code=403, detail="Item não pertence ao seu carrinho")
    
    # Atualiza a quantidade
    item.quantity = quantity
    db.add(item)
    db.commit()
    
    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)

