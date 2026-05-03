from pydantic import BaseModel, Field
from typing import Optional


class PedidoInput(BaseModel):
    prato_id: int
    quantidade: int = Field(ge=1, description="Quantidade de pratos pedidos")
    observacao: Optional[str] = Field(default=None, max_length=300)


class PedidoOutput(BaseModel):
    id: int
    prato_id: int
    nome_prato: str
    quantidade: int
    valor_total: float
    observacao: Optional[str]
