from enum import Enum

class EstadoProducto(str, Enum):
    NUEVO = "nuevo"
    USADO = "usado"