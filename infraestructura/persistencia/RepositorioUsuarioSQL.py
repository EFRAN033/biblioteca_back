# efran033/biblioteca_back/biblioteca_back-e45426e2e00fbbc201232909bbf09d0ca9ea44ce/infraestructura/persistencia/RepositorioUsuarioSQL.py
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import Optional

from .configuracion import Base
from dominio.entidades.Usuario import Usuario
from dominio.puertos.IRepoUsuario import IRepoUsuario
from dominio.value_objects.RolUsuario import RolUsuario
from dominio.value_objects.EstadoUsuario import EstadoUsuario # <-- IMPORTAR NUEVO ENUM

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombres = Column(String, index=True)
    apellidos = Column(String, index=True) # <-- AÑADIR APELLIDOS
    email = Column(String, unique=True, index=True)
    hash_contrasena = Column(String, nullable=True) # <-- PERMITIR NULO
    rol = Column(SQLAlchemyEnum(RolUsuario, values_callable=lambda obj: [e.value for e in obj]))
    estado = Column(SQLAlchemyEnum(EstadoUsuario, values_callable=lambda obj: [e.value for e in obj])) # <-- AÑADIR ESTADO
    fecha_creacion = Column(DateTime)


class RepositorioUsuarioSQL(IRepoUsuario):

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, usuario: Usuario) -> Usuario:
        # Convertir la entidad de dominio a un modelo de DB
        usuario_db_data = usuario.model_dump()
        
        # Pydantic y SQLAlchemy manejan los Enums de forma diferente
        # Aseguramos que se guarden los valores string del Enum
        usuario_db_data['rol'] = usuario.rol.value
        usuario_db_data['estado'] = usuario.estado.value

        # Crear instancia de UsuarioDB
        usuario_db = UsuarioDB(**usuario_db_data)
        
        # Usar merge para insertar o actualizar
        usuario_gestionado = self.db.merge(usuario_db)
        self.db.commit()
        
        # Devolver la entidad de dominio validada desde el objeto de DB
        # Es importante recargar el objeto para obtener valores por defecto de la DB (como IDs)
        # Pero para 'merge', el objeto ya está en la sesión. Validamos su __dict__.
        return Usuario.model_validate(usuario_db)

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        usuario_db = self.db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
        if usuario_db:
            return Usuario.model_validate(usuario_db)
        return None

    def existe_email(self, email: str) -> bool:
        return self.db.query(UsuarioDB).filter(UsuarioDB.email == email).count() > 0