#pip install -r requirements.txt
#uvicorn main:app --reload --host 0.0.0.0 --port 3344

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.routers.products import router as products_router

app = FastAPI(title="Projeto")

# Rotas (produtos)
app.include_router(products_router)

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