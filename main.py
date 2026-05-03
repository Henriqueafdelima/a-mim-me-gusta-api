"""
¡A mi me gusta! — API do restaurante mexicano
Construída seguindo o tutorial FastAPI na Prática (Blocos 1, 2 e 3)
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from config import settings
from routers import pratos, bebidas, pedidos, reservas, predict


# Exercício 1.1 — instância do FastAPI com metadados
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)


# ─────────────────────────────────────────────
# Exercício 2.6 — Exception handlers globais
# ─────────────────────────────────────────────



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Formato unificado para erros de validação (422)."""
    return JSONResponse(
        status_code=422,
        content={
            "erro": "Dados de entrada inválidos",
            "status": 422,
            "path": str(request.url),
            "detalhes": [
                {
                    "campo": " -> ".join(str(loc) for loc in e["loc"]),
                    "mensagem": e["msg"]
                }
                for e in exc.errors()
            ]
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Formato unificado para erros HTTP (404, 400, etc.)."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": exc.detail,
            "status": exc.status_code,
            "path": str(request.url),
            "detalhes": []
        }
    )


# ─────────────────────────────────────────────
# Exercício 3.2 / 3.3 — Routers por domínio
# ─────────────────────────────────────────────

app.include_router(pratos.router,   prefix="/pratos",   tags=["Pratos"])
app.include_router(bebidas.router,  prefix="/bebidas",  tags=["Bebidas"])
app.include_router(pedidos.router,  prefix="/pedidos",  tags=["Pedidos"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
app.include_router(predict.router, prefix="/ml", tags=["ML"])



# ─────────────────────────────────────────────
# Exercício 1.1 — Rota raiz
# ─────────────────────────────────────────────

@app.get("/", tags=["Geral"])
async def root():
    return {
        "restaurante": settings.app_name,
        "mensagem": "¡Bienvenidos! Bem-vindo à nossa API",
        "chef": "Seu Burrito",
        "cidade": "São Paulo",
        "especialidade": "Burritos e pratos mexicanos"
    }
