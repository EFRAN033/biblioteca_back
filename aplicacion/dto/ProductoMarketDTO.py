from pydantic import BaseModel, Field
from typing import Optional
import uuid
from dominio.value_objects.EstadoProducto import EstadoProducto

class ProductoCrearDTO(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    estado: EstadoProducto

class ProductoPublicadoDTO(BaseModel):
    id: uuid.UUID
    titulo: str
    precio: float
    # LÍNEA CORREGIDA:
    vendedor_id: uuid.UUID = Field(alias='usuario_vendedor_id')

    class Config:
        populate_by_name = True 