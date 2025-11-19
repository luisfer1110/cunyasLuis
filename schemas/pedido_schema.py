from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PedidoBase(BaseModel):
    cliente_id: int
    total: float

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(BaseModel):
    cliente_id: Optional[int] = None
    total: Optional[float] = None

class Pedido(PedidoBase):
    id: int
    fecha_pedido: datetime

    model_config = {
        "from_attributes": True
    }
