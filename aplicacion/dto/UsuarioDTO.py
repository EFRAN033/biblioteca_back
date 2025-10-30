from pydantic import BaseModel, EmailStr
from dominio.value_objects.RolUsuario import RolUsuario

class UsuarioRegistroDTO(BaseModel):
    nombres: str
    email: EmailStr
    password: str
    rol: RolUsuario = RolUsuario.ESTUDIANTE # Rol por defecto

class UsuarioLoginDTO(BaseModel):
    email: EmailStr
    password: str

class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"