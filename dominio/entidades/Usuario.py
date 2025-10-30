import uuid
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from ..value_objects.RolUsuario import RolUsuario

class Usuario(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    nombres: str
    email: EmailStr
    hash_contrasena: str 
    rol: RolUsuario
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)