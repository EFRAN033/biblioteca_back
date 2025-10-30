from abc import ABC, abstractmethod
from ..entidades.Alquiler import Alquiler

class IRepoAlquiler(ABC):
    @abstractmethod
    def guardar(self, alquiler: Alquiler) -> Alquiler:
        ...