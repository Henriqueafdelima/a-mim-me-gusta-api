from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ReservaInput(BaseModel):
    mesa: int = Field(ge=1, le=20, description="Número da mesa (1 a 20)")
    nome: str = Field(min_length=2, max_length=100, description="Nome do responsável pela reserva")
    pessoas: int = Field(ge=1, le=10, description="Número de pessoas (1 a 10)")
    data_hora: datetime

    # Exercício 3.6 — reserva deve ser feita com pelo menos 1h de antecedência
    @field_validator("data_hora")
    @classmethod
    def deve_ser_futura(cls, v):
        agora = datetime.now(tz=v.tzinfo)
        if (v - agora).total_seconds() < 3600:
            raise ValueError("Reserva deve ser feita com pelo menos 1 hora de antecedência")
        return v


class ReservaOutput(BaseModel):
    id: int
    mesa: int
    nome: str
    pessoas: int
    data_hora: str
    ativa: bool
    criada_em: str
