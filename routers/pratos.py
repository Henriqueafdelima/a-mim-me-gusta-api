from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime

from models.prato import PratoInput, PratoOutput

router = APIRouter()

# Exercício 1.2 — lista inicial de pratos (cardápio mexicano)
# Exercício 1.5 — campo 'disponivel' adicionado
pratos = [
    {"id": 1, "nome": "Burrito de Carne Seca", "categoria": "burrito", "preco": 42.0, "preco_promocional": None, "descricao": "Burrito recheado com carne seca desfiada, feijão preto e queijo coalho", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 2, "nome": "Burrito Vegano", "categoria": "burrito", "preco": 38.0, "preco_promocional": None, "descricao": "Burrito com grão-de-bico temperado, guacamole e pico de gallo", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 3, "nome": "Taco de Frango", "categoria": "taco", "preco": 28.0, "preco_promocional": 22.0, "descricao": "Taco com frango grelhado, pico de gallo e coentro fresco", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 4, "nome": "Taco de Camarão", "categoria": "taco", "preco": 36.0, "preco_promocional": None, "descricao": "Taco com camarão empanado, chipotle mayo e repolho roxo", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 5, "nome": "Quesadilla de Queijo", "categoria": "quesadilla", "preco": 32.0, "preco_promocional": None, "descricao": "Quesadilla com blend de queijos mexicanos e jalapeños", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 6, "nome": "Nachos com Guacamole", "categoria": "entrada", "preco": 29.0, "preco_promocional": None, "descricao": "Nachos artesanais com guacamole fresco e sour cream", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
    {"id": 7, "nome": "Salada Mexicana", "categoria": "salada", "preco": 26.0, "preco_promocional": None, "descricao": "Mix de folhas, milho, feijão, tomate cereja e molho jalapeño", "disponivel": False, "criado_em": "2024-01-01T00:00:00"},
    {"id": 8, "nome": "Churros com Doce de Leite", "categoria": "sobremesa", "preco": 24.0, "preco_promocional": None, "descricao": "Churros crocantes com recheio de doce de leite e açúcar canela", "disponivel": True, "criado_em": "2024-01-01T00:00:00"},
]


# Exercício 1.4 / 1.5 — GET /pratos com filtros de categoria, preco_maximo e disponibilidade
@router.get("/")
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    apenas_disponiveis: bool = False
):
    resultado = pratos

    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]

    if preco_maximo:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]

    if apenas_disponiveis:
        resultado = [p for p in resultado if p["disponivel"]]

    return resultado


# Exercício 1.5 / 2.2 — GET /pratos/{id} com path param e HTTPException
@router.get("/{prato_id}")
async def buscar_prato(prato_id: int, formato: str = "completo"):
    for prato in pratos:
        if prato["id"] == prato_id:
            if formato == "resumido":
                return {"nome": prato["nome"], "preco": prato["preco"]}
            return prato
    raise HTTPException(
        status_code=404,
        detail=f"Prato com id {prato_id} não encontrado"
    )


# Exercício 1.7 / 2.3 / 2.4 — POST /pratos com PratoInput, PratoOutput, validações
@router.post("/", response_model=PratoOutput)
async def criar_prato(prato: PratoInput):
    novo_id = max(p["id"] for p in pratos) + 1
    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump()
    }
    pratos.append(novo_prato)
    return novo_prato


# Exercício 2.5 — PUT /pratos/{id}/disponibilidade
from pydantic import BaseModel

class DisponibilidadeInput(BaseModel):
    disponivel: bool

@router.put("/{prato_id}/disponibilidade")
async def alterar_disponibilidade(prato_id: int, body: DisponibilidadeInput):
    for prato in pratos:
        if prato["id"] == prato_id:
            prato["disponivel"] = body.disponivel
            return prato
    raise HTTPException(status_code=404, detail="Prato não encontrado")
