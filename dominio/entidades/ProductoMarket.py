import uuid
from pydantic import BaseModel, Field
from typing import Optional
from ..value_objects.EstadoProducto import EstadoProducto

class ProductoMarket(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    titulo: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    precio: float = Field(gt=0) 
    stock: int = Field(ge=0) 
    estado: EstadoProducto
    usuario_vendedor_id: uuid.UUID