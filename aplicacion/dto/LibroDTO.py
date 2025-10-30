from pydantic import BaseModel
from typing import Optional
import uuid

class LibroCrearDTO(BaseModel):
    titulo: str
    autor: str
    isbn: Optional[str] = None
    editorial: Optional[str] = None
    ano_publicacion: Optional[int] = None
    categoria: Optional[str] = None
    ubicacion: Optional[str] = None
    ejemplares_totales: int
    ejemplares_disponibles: int

class LibroDetalleDTO(BaseModel):
    id: uuid.UUID
    titulo: str
    autor: str
    ejemplares_disponibles: int

class LibroDetalleDTO(BaseModel):
    id: uuid.UUID
    titulo: str
    autor: str
    isbn: Optional[str] = None
    editorial: Optional[str] = None
    ano_publicacion: Optional[int] = None
    categoria: Optional[str] = None
    ejemplares_totales: int
    ejemplares_disponibles: int