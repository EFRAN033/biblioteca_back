from pydantic import BaseModel
import uuid
from datetime import datetime

class AlquilerSolicitudDTO(BaseModel):
    libro_id: uuid.UUID

class AlquilerRespuestaDTO(BaseModel):
    id: uuid.UUID
    libro_id: uuid.UUID
    usuario_id: uuid.UUID
    fecha_fin: datetime