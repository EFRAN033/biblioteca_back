from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .market_router import get_usuario_actual 
from dominio.entidades.Usuario import Usuario
from aplicacion.dto.AlquilerDTO import AlquilerSolicitudDTO, AlquilerRespuestaDTO
from aplicacion.casos_uso.CU_GestionarAlquiler import GestionarAlquiler
from infraestructura.persistencia.configuracion import get_db
from infraestructura.persistencia.RepositorioAlquilerSQL import RepositorioAlquilerSQL
from infraestructura.persistencia.RepositorioLibroSQL import RepositorioLibroSQL

router = APIRouter(prefix="/alquiler", tags=["Alquileres"])

@router.post("/", response_model=AlquilerRespuestaDTO, status_code=status.HTTP_201_CREATED)
def solicitar_alquiler(
    solicitud: AlquilerSolicitudDTO,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_usuario_actual)
):
    try:
        repo_alquiler = RepositorioAlquilerSQL(db)
        repo_libro = RepositorioLibroSQL(db)
        caso_uso = GestionarAlquiler(repo_alquiler, repo_libro)

        alquiler_creado = caso_uso.solicitar_prestamo(solicitud, usuario_actual.id)

        db.commit() 
        return alquiler_creado
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))