from abc import ABC, abstractmethod
from ..entidades.ProductoMarket import ProductoMarket

class IRepoProductoMarket(ABC):

    @abstractmethod
    def guardar(self, producto: ProductoMarket) -> ProductoMarket:
        ...