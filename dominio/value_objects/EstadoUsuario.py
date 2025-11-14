from enum import Enum

class EstadoUsuario(str, Enum):
    PENDIENTE = "pendiente"
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    RECHAZADO = "rechazado"