from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime

from models.reserva import ReservaInput, ReservaOutput

router = APIRouter()

reservas = []


# Exercício 3.6 — POST /reservas com regras de negócio
@router.post("/", response_model=ReservaOutput)
async def criar_reserva(reserva: ReservaInput):
    data_reserva = reserva.data_hora.date()

    # Regra: mesa não pode estar ocupada no mesmo dia
    conflito = any(
        r["mesa"] == reserva.mesa
        and r["ativa"]
        and datetime.fromisoformat(r["data_hora"]).date() == data_reserva
        for r in reservas
    )
    if conflito:
        raise HTTPException(
            status_code=400,
            detail=f"Mesa {reserva.mesa} já está reservada para o dia {data_reserva}"
        )

    nova = {
        "id": len(reservas) + 1,
        "mesa": reserva.mesa,
        "nome": reserva.nome,
        "pessoas": reserva.pessoas,
        "data_hora": reserva.data_hora.isoformat(),
        "ativa": True,
        "criada_em": datetime.now().isoformat()
    }
    reservas.append(nova)
    return nova


# Exercício 3.6 — GET /reservas com filtros de data e status
@router.get("/")
async def listar_reservas(data: Optional[str] = None, apenas_ativas: bool = True):
    resultado = reservas

    if apenas_ativas:
        resultado = [r for r in resultado if r["ativa"]]

    if data:
        resultado = [
            r for r in resultado
            if datetime.fromisoformat(r["data_hora"]).date().isoformat() == data
        ]

    return resultado


# Exercício 3.6 — GET /reservas/mesa/{numero}
@router.get("/mesa/{numero}")
async def reservas_por_mesa(numero: int):
    return [r for r in reservas if r["mesa"] == numero]


# Exercício 3.6 — GET /reservas/{id}
@router.get("/{reserva_id}", response_model=ReservaOutput)
async def buscar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva não encontrada")


# Exercício 3.6 — DELETE /reservas/{id}
@router.delete("/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            if not r["ativa"]:
                raise HTTPException(status_code=400, detail="Reserva já está cancelada")
            r["ativa"] = False
            return {"mensagem": "Reserva cancelada com sucesso"}
    raise HTTPException(status_code=404, detail="Reserva não encontrada")
