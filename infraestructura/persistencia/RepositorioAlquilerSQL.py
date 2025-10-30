from sqlalchemy.orm import Session
from sqlalchemy import Column, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .configuracion import Base
from dominio.entidades.Alquiler import Alquiler
from dominio.puertos.IRepoAlquiler import IRepoAlquiler
from dominio.value_objects.EstadoAlquiler import EstadoAlquiler

class AlquilerDB(Base):
    __tablename__ = "alquileres"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    libro_id = Column(UUID(as_uuid=True), ForeignKey("libros.id"), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    fecha_devolucion = Column(DateTime)
    estado = Column(SQLAlchemyEnum(EstadoAlquiler, values_callable=lambda obj: [e.value for e in obj]))

class RepositorioAlquilerSQL(IRepoAlquiler):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, alquiler: Alquiler) -> Alquiler:
        alquiler_db = AlquilerDB(**alquiler.model_dump())
        self.db.add(alquiler_db)

        return Alquiler.model_validate(alquiler_db.__dict__)