from aplicacion.dto.ProductoMarketDTO import ProductoCrearDTO
from dominio.entidades.ProductoMarket import ProductoMarket
from dominio.puertos.IRepoProductoMarket import IRepoProductoMarket
import uuid

class AgregarProductoMarket:
    def __init__(self, repositorio_producto: IRepoProductoMarket):
        self.repositorio_producto = repositorio_producto

    def ejecutar(self, datos_producto: ProductoCrearDTO, usuario_vendedor_id: uuid.UUID) -> ProductoMarket:
        
        nuevo_producto = ProductoMarket(
            titulo=datos_producto.titulo,
            descripcion=datos_producto.descripcion,
            categoria=datos_producto.categoria,
            precio=datos_producto.precio,
            stock=datos_producto.stock,
            estado=datos_producto.estado,
            usuario_vendedor_id=usuario_vendedor_id
        )
        
        return self.repositorio_producto.guardar(nuevo_producto)