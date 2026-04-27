from fastapi import APIRouter, HTTPException
from models.pedido import PedidoInput, PedidoOutput

router = APIRouter()

pedidos = []


# Exercício 2.5 — POST /pedidos com validação de disponibilidade
@router.post("/", response_model=PedidoOutput)
async def criar_pedido(pedido: PedidoInput):
    # importação local para evitar importação circular
    from routers.pratos import pratos

    prato = next((p for p in pratos if p["id"] == pedido.prato_id), None)

    if not prato:
        raise HTTPException(
            status_code=404,
            detail=f"Prato com id {pedido.prato_id} não encontrado"
        )

    if not prato["disponivel"]:
        raise HTTPException(
            status_code=400,
            detail=f"O prato '{prato['nome']}' não está disponível no momento"
        )

    novo_id = len(pedidos) + 1
    novo_pedido = {
        "id": novo_id,
        "prato_id": pedido.prato_id,
        "nome_prato": prato["nome"],
        "quantidade": pedido.quantidade,
        "valor_total": prato["preco"] * pedido.quantidade,
        "observacao": pedido.observacao
    }
    pedidos.append(novo_pedido)
    return novo_pedido
