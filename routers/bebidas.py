from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime

from models.bebida import BebidaInput, BebidaOutput

router = APIRouter()

# Exercício 1.8 — lista inicial de bebidas (temática mexicana)
bebidas = [
    {"id": 1, "nome": "Água Mineral", "tipo": "agua", "preco": 8.0, "alcoolica": False, "volume_ml": 500, "criado_em": "2024-01-01T00:00:00"},
    {"id": 2, "nome": "Corona Extra", "tipo": "cerveja", "preco": 18.0, "alcoolica": True, "volume_ml": 355, "criado_em": "2024-01-01T00:00:00"},
    {"id": 3, "nome": "Modelo Especial", "tipo": "cerveja", "preco": 20.0, "alcoolica": True, "volume_ml": 355, "criado_em": "2024-01-01T00:00:00"},
    {"id": 4, "nome": "Margarita Clássica", "tipo": "destilado", "preco": 32.0, "alcoolica": True, "volume_ml": 250, "criado_em": "2024-01-01T00:00:00"},
    {"id": 5, "nome": "Suco de Maracujá", "tipo": "suco", "preco": 14.0, "alcoolica": False, "volume_ml": 400, "criado_em": "2024-01-01T00:00:00"},
    {"id": 6, "nome": "Guaraná Antarctica", "tipo": "refrigerante", "preco": 9.0, "alcoolica": False, "volume_ml": 350, "criado_em": "2024-01-01T00:00:00"},
]


# Exercício 1.8 — GET /bebidas com filtros
@router.get("/")
async def listar_bebidas(
    tipo: Optional[str] = None,
    alcoolica: Optional[bool] = None
):
    resultado = bebidas

    if tipo:
        resultado = [b for b in resultado if b["tipo"] == tipo]

    if alcoolica is not None:
        resultado = [b for b in resultado if b["alcoolica"] == alcoolica]

    return resultado


# Exercício 1.8 / 2.2 — GET /bebidas/{id} com HTTPException
@router.get("/{bebida_id}")
async def buscar_bebida(bebida_id: int):
    for bebida in bebidas:
        if bebida["id"] == bebida_id:
            return bebida
    raise HTTPException(
        status_code=404,
        detail=f"Bebida com id {bebida_id} não encontrada"
    )


# Exercício 1.8 — POST /bebidas com BebidaInput e BebidaOutput
@router.post("/", response_model=BebidaOutput)
async def criar_bebida(bebida: BebidaInput):
    novo_id = max(b["id"] for b in bebidas) + 1
    nova_bebida = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **bebida.model_dump()
    }
    bebidas.append(nova_bebida)
    return nova_bebida
