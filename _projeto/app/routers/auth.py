from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select
from pathlib import Path

from app.database import get_db
from app.models import User, UserRole, Cart
from app.dependencies import get_current_user_optional

router = APIRouter()

# Configuração de diretório de templates
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/register")
def register_form(request: Request, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Exibe o formulário de registro."""
    if current_user:
        return RedirectResponse(url="/products", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("auth/register.html", {"request": request, "current_user": None})


@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(default="user"),
    db: Session = Depends(get_db),
):
    """Registra um novo usuário."""
    errors = []
    
    # Validação de campos
    if not username.strip() or not password.strip():
        errors.append("Username e senha são obrigatórios")
    
    if len(password) < 6:
        errors.append("A senha deve ter pelo menos 6 caracteres")
    
    # Validação de role
    if role not in ["admin", "user"]:
        role = "user"
    
    # Verifica se username já existe
    if db.scalar(select(User).where(User.username == username.strip())):
        errors.append("Username já cadastrado")
    
    # Se houver erros, mostra na mesma página
    if errors:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "current_user": None,
                "errors": errors,
                "username": username,
                "role": role
            }
        )
    
    # Cria o usuário
    user_role = UserRole.ADMIN if role == "admin" else UserRole.USER
    user = User(
        username=username.strip(),
        hashed_password=User.hash_password(password),
        role=user_role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Cria o carrinho para o usuário
    cart = Cart(user_id=user.id)
    db.add(cart)
    db.commit()
    
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/login")
def login_form(request: Request, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Exibe o formulário de login."""
    if current_user:
        return RedirectResponse(url="/products", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("auth/login.html", {"request": request, "current_user": None})


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Autentica o usuário e cria a sessão."""
    error = None
    
    if not username.strip() or not password.strip():
        error = "Username e senha são obrigatórios"
    else:
        # Busca o usuário
        user = db.scalar(select(User).where(User.username == username.strip()))
        if not user:
            error = "Username ou senha incorretos"
        elif not user.verify_password(password):
            error = "Username ou senha incorretos"
        else:
            # Cria a sessão
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["role"] = user.role.value
            return RedirectResponse(url="/products", status_code=status.HTTP_303_SEE_OTHER)
    
    # Se houver erro, mostra na mesma página
    return templates.TemplateResponse(
        "auth/login.html",
        {
            "request": request,
            "current_user": None,
            "error": error,
            "username": username
        }
    )


@router.get("/logout")
def logout(request: Request):
    """Encerra a sessão do usuário."""
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

