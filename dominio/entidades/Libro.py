import uuid
from pydantic import BaseModel, Field
from typing import Optional

class Libro(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    titulo: str
    autor: str
    isbn: Optional[str] = None
    editorial: Optional[str] = None
    ano_publicacion: Optional[int] = None
    categoria: Optional[str] = None
    ubicacion: Optional[str] = None
    ejemplares_totales: int = Field(ge=0)
    ejemplares_disponibles: int = Field(ge=0)