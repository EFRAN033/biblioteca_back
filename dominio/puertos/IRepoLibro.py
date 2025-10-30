from abc import ABC, abstractmethod
from typing import List, Optional
from ..entidades.Libro import Libro

class IRepoLibro(ABC):
    @abstractmethod
    def guardar(self, libro: Libro) -> Libro:
        ...

    @abstractmethod
    def obtener_todos(self) -> List[Libro]:
        ...

    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Libro]:
        ...
    
    