from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Atributos base compartidos
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# Datos obligatorios para crear (POST)
class ProductCreate(ProductBase):
    pass

# Datos opcionales para actualizar (PUT / PATCH)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None

# Datos que la API responde hacia el cliente (GET / respuestas)
class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)