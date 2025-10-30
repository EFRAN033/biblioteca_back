from enum import Enum

class RolUsuario(str, Enum):
    ESTUDIANTE = "estudiante"
    BIBLIOTECARIO = "bibliotecario"
    ADMIN = "admin"