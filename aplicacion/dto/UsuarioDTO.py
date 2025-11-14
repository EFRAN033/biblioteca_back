# efran033/biblioteca_back/biblioteca_back-e45426e2e00fbbc201232909bbf09d0ca9ea44ce/aplicacion/dto/UsuarioDTO.py
from pydantic import BaseModel, EmailStr
from typing import Optional # <-- IMPORTAR OPTIONAL
from dominio.value_objects.RolUsuario import RolUsuario

class UsuarioRegistroDTO(BaseModel):
    nombres: str
    apellidos: str # <-- AÑADIR APELLIDOS
    correo: EmailStr # <-- Cambiar 'email' por 'correo' para que coincida con Vue
    rol: RolUsuario
    password: Optional[str] = None # <-- HACER OPCIONAL
    
    # Esto permite que Pydantic use 'correo' del JSON 
    # para llenar el campo 'email' si lo necesitaras,
    # pero es más fácil simplemente renombrar el campo en Python.
    # Vamos a mantenerlo simple:
    
    class Config:
        alias_generator = lambda string: string.replace('correo', 'email')
        populate_by_name = True

# Renombraremos los campos en el DTO para que coincidan 1:1 con el JSON de Vue
# para evitar confusión con los alias.

class UsuarioRegistroDTO(BaseModel):
    nombres: str
    apellidos: str
    correo: EmailStr # Coincide con formData.correo
    rol: RolUsuario    # Coincide con formData.rol
    password: Optional[str] = None # Coincide con formData.password

class UsuarioLoginDTO(BaseModel):
    email: EmailStr
    password: str

class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"