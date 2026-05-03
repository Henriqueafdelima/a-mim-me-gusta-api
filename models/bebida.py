from pydantic import BaseModel, Field
from typing import Optional


class BebidaInput(BaseModel):
    nome: str = Field(min_length=3, max_length=100, description="Nome da bebida")
    tipo: str = Field(
        pattern="^(cerveja|agua|refrigerante|suco|destilado)$",
        description="Tipo da bebida"
    )
    preco: float = Field(gt=0, description="Preço em reais, deve ser positivo")
    alcoolica: bool
    volume_ml: int = Field(ge=50, le=2000, description="Volume em ml (entre 50 e 2000)")


class BebidaOutput(BaseModel):
    id: int
    nome: str
    tipo: str
    preco: float
    alcoolica: bool
    volume_ml: int
    criado_em: str
