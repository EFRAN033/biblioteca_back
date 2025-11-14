import uuid
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional 
from ..value_objects.RolUsuario import RolUsuario
from ..value_objects.EstadoUsuario import EstadoUsuario

class Usuario(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    nombres: str
    apellidos: str 
    email: EmailStr
    hash_contrasena: Optional[str] = None 
    rol: RolUsuario
    estado: EstadoUsuario
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"from_attributes": True}