from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import Optional

from .configuracion import Base
from dominio.entidades.Usuario import Usuario
from dominio.puertos.IRepoUsuario import IRepoUsuario
from dominio.value_objects.RolUsuario import RolUsuario

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombres = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hash_contrasena = Column(String)
    rol = Column(SQLAlchemyEnum(RolUsuario, values_callable=lambda obj: [e.value for e in obj]))
    fecha_creacion = Column(DateTime)


class RepositorioUsuarioSQL(IRepoUsuario):

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, usuario: Usuario) -> Usuario:
        usuario_db = UsuarioDB(
            id=usuario.id,
            nombres=usuario.nombres,
            email=usuario.email,
            hash_contrasena=usuario.hash_contrasena,
            rol=usuario.rol,
            fecha_creacion=usuario.fecha_creacion
        )
        self.db.add(usuario_db)
        self.db.commit()
        self.db.refresh(usuario_db)
        return usuario

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        usuario_db = self.db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
        if usuario_db:
            return Usuario.model_validate(usuario_db.__dict__)
        return None

    def existe_email(self, email: str) -> bool:
        return self.db.query(UsuarioDB).filter(UsuarioDB.email == email).count() > 0