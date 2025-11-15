from pydantic import BaseModel, Field, EmailStr
from typing import Optional 
import uuid 
from datetime import datetime

# Importaciones de value_objects necesarias para los DTOs
from dominio.value_objects.RolUsuario import RolUsuario
from dominio.value_objects.EstadoUsuario import EstadoUsuario 

# ----------------------------------------------
# 1. DTOs de Entrada (Input)
# ----------------------------------------------

# DTO para el registro de usuarios
class UsuarioRegistroDTO(BaseModel):
    nombres: str
    apellidos: str
    correo: EmailStr 
    rol: RolUsuario
    password: Optional[str] = None

# DTO para el login de usuarios
class UsuarioLoginDTO(BaseModel):
    email: EmailStr
    password: str


# ----------------------------------------------
# 2. DTOs de Salida (Output)
# ----------------------------------------------

# DTO para el token de autenticación
class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
# DTO para mostrar detalles completos del usuario (Usado en el nuevo endpoint PATCH)
class UsuarioDetalleDTO(BaseModel):
    id: uuid.UUID
    nombres: str
    apellidos: str 
    email: EmailStr
    rol: RolUsuario
    estado: EstadoUsuario # Importante para saber si está ACTIVO/PENDIENTE
    fecha_creacion: datetime

    class Config:
        # Permite la inicialización directa desde el modelo ORM (Entidad de Dominio o SQLAlchemy)
        from_attributes = True