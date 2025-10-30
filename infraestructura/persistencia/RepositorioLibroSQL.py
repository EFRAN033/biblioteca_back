from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List, Optional

from .configuracion import Base
from dominio.entidades.Libro import Libro
from dominio.puertos.IRepoLibro import IRepoLibro

class LibroDB(Base):
    __tablename__ = "libros"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    isbn = Column(String, unique=True)
    editorial = Column(String)
    ano_publicacion = Column(Integer)
    categoria = Column(String)
    ubicacion = Column(String)
    ejemplares_totales = Column(Integer, nullable=False)
    ejemplares_disponibles = Column(Integer, nullable=False)

class RepositorioLibroSQL(IRepoLibro):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, libro: Libro) -> Libro:
        libro_db = LibroDB(**libro.model_dump())
        libro_gestionado = self.db.merge(libro_db)
        return Libro.model_validate(libro_gestionado.__dict__)

    def obtener_todos(self) -> List[Libro]:
        libros_db = self.db.query(LibroDB).all()
        return [Libro.model_validate(libro.__dict__) for libro in libros_db]

    def obtener_por_id(self, libro_id: uuid.UUID) -> Optional[Libro]:
        libro_db = self.db.query(LibroDB).filter(LibroDB.id == libro_id).first()
        if libro_db:
            return Libro.model_validate(libro_db.__dict__)
        return None