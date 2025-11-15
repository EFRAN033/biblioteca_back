from abc import ABC, abstractmethod
from typing import Optional, List # <-- AGREGADO: List
from ..entidades.Usuario import Usuario
import uuid # <-- AGREGADO: uuid

class IRepoUsuario(ABC):

    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        ...

    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        ...

    @abstractmethod
    def existe_email(self, email: str) -> bool:
        ...

    @abstractmethod
    def obtener_todos(self) -> List[Usuario]: # <-- NUEVO: Para listar usuarios en el Dashboard
        ...
        
    @abstractmethod
    def obtener_por_id(self, id: uuid.UUID) -> Optional[Usuario]: # <-- NUEVO: Necesario para la aprobación
        ...