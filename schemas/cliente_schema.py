from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None

class Cliente(ClienteBase):
    id: int

    model_config = {
        "from_attributes": True
    }
