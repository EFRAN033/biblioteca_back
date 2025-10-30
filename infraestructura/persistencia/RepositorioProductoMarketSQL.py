from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Float, Integer, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .configuracion import Base
from dominio.entidades.ProductoMarket import ProductoMarket
from dominio.puertos.IRepoProductoMarket import IRepoProductoMarket
from dominio.value_objects.EstadoProducto import EstadoProducto

class ProductoMarketDB(Base):
    __tablename__ = "productos_market"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String, nullable=False)
    descripcion = Column(String)
    categoria = Column(String)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    estado = Column(SQLAlchemyEnum(EstadoProducto, values_callable=lambda obj: [e.value for e in obj]))
    usuario_vendedor_id = Column(UUID(as_uuid=True), nullable=False) 

class RepositorioProductoMarketSQL(IRepoProductoMarket):

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, producto: ProductoMarket) -> ProductoMarket:
        producto_db = ProductoMarketDB(
            id=producto.id,
            titulo=producto.titulo,
            descripcion=producto.descripcion,
            categoria=producto.categoria,
            precio=producto.precio,
            stock=producto.stock,
            estado=producto.estado,
            usuario_vendedor_id=producto.usuario_vendedor_id
        )
        self.db.add(producto_db)
        self.db.commit()
        self.db.refresh(producto_db)
        return producto