from enum import Enum

class EstadoAlquiler(str, Enum):
    PRESTADO = "prestado"
    DEVUELTO = "devuelto"