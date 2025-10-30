import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from ..value_objects.EstadoAlquiler import EstadoAlquiler
from typing import Optional

class Alquiler(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    usuario_id: uuid.UUID
    libro_id: uuid.UUID
    fecha_inicio: datetime = Field(default_factory=datetime.utcnow)
    fecha_fin: datetime
    fecha_devolucion: Optional[datetime] = None
    estado: EstadoAlquiler = EstadoAlquiler.PRESTADO