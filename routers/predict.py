"""
routers/predict.py — Endpoints de ML do ¡A mi me gusta!

POST /ml/predict  — prevê se um pedido é problemático
GET  /ml/health   — verifica se a API e o modelo estão ok

Exercícios 4.2 e 4.3 do Caderno 2
"""

import numpy as np
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

router = APIRouter()

REPO_ID = "Richsk/a-mi-me-gusta-predictor"
_model = None


def get_model():
    """Carrega o modelo uma única vez e mantém em memória."""
    global _model
    if _model is None:
        from model_utils import load_model

        _model = load_model(REPO_ID)
    return _model


# ─── Schemas ──────────────────────────────────────────────────────────────────

class PredictInput(BaseModel):
    valor_pedido: float = Field(gt=0, description="Valor total do pedido em reais")
    hora_pedido: int = Field(ge=0, le=23, description="Hora do dia em que o pedido foi feito (0-23)")
    num_itens: int = Field(ge=1, description="Quantidade de pratos no pedido")
    historico_cancelamentos: int = Field(ge=0, description="Número de cancelamentos anteriores do cliente")
    distancia_entrega: float = Field(ge=0, description="Distância de entrega em km")


class PredictOutput(BaseModel):
    prediction: int
    probability: float
    label: str
    model_version: str


# ─── Rotas ────────────────────────────────────────────────────────────────────

@router.post("/predict", response_model=PredictOutput)
async def predict(input: PredictInput):
    """
    Prevê o risco de um pedido ser problemático (cancelamento ou reclamação).

    Retorna prediction (0 ou 1), probabilidade, label e versão do modelo.
    """
    model = get_model()

    # A ordem dos campos DEVE ser idêntica à ordem usada no treino
    features = np.array([[
        input.valor_pedido,
        input.hora_pedido,
        input.num_itens,
        input.historico_cancelamentos,
        input.distancia_entrega,
    ]])

    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])
    label = "problemático" if prediction == 1 else "normal"

    return PredictOutput(
        prediction=prediction,
        probability=round(probability, 4),
        label=label,
        model_version=REPO_ID,
    )


@router.get("/health")
async def health():
    """
    Verifica o status da API e do modelo.

    Retorna 200 quando tudo está ok, 503 quando o modelo está degradado.
    O status 503 avisa load balancers e monitoramento que a API não consegue
    cumprir sua função principal — diferente de um 200 falso.
    """
    try:
        model = get_model()
        test_input = np.zeros((1, 5))
        model.predict(test_input)
        model_ok = True
        detail = None
    except Exception as e:
        model_ok = False
        detail = str(e)

    body = {
        "api": "ok",
        "model": "ok" if model_ok else "degraded",
        "model_repo": REPO_ID,
        "detail": detail,
    }

    return JSONResponse(content=body, status_code=200 if model_ok else 503)
