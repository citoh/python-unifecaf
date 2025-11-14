#pip install -r requirements.txt
#uvicorn main:app --reload --host 0.0.0.0 --port 3344

from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
from app.routers.products import router as products_router
from app.routers.auth import router as auth_router
from app.routers.cart import router as cart_router
from app.dependencies import get_current_user_optional

app = FastAPI(title="Projeto")

# Configuração de sessões (necessário para autenticação)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-in-production")

# Configuração de templates para a rota raiz
TEMPLATES_DIR = Path(__file__).resolve().parent / "app" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Rotas
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(cart_router)

# Rota raiz - redireciona baseado no estado de autenticação
@app.get("/", include_in_schema=False)
def root(request: Request, current_user = Depends(get_current_user_optional)):
    """Página inicial: login se não autenticado, produtos se autenticado."""
    if not current_user:
        # Não autenticado - mostra tela de login
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "current_user": None}
        )
    else:
        # Autenticado - redireciona para produtos (admin vê gerenciamento, user vê lista)
        return RedirectResponse(url="/products", status_code=302)

# Arquivos estáticos (CSS, imagens, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Status/saúde do servidor (com host/porta)
@app.get("/status")
def status(request: Request):
    return {
        "status": "ok",
        "host": request.client.host,
        "port": request.url.port or 80,
        "scheme": request.url.scheme,
        "path": request.url.path,
    }