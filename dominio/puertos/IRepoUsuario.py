from abc import ABC, abstractmethod
from typing import Optional
from .entidades.Usuario import Usuario

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