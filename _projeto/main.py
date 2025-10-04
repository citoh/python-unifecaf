from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.routers import products_router  # import direto do __init__.py de routers

app = FastAPI(title="Projeto")

# Rotas
app.include_router(products_router)

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Rota simples de status do servidor
@app.get("/status")
def status(request: Request):
    return {
        "status": "ok",
        "host": request.client.host,
        "port": request.url.port or 80,  # porta padrão se não estiver explícita
        "scheme": request.url.scheme,
        "path": request.url.path,
    }