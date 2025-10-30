from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

# Importamos la lógica de seguridad y los DTOs necesarios
from .market_router import get_usuario_actual
from dominio.entidades.Usuario import Usuario
from dominio.value_objects.RolUsuario import RolUsuario
from aplicacion.dto.LibroDTO import LibroCrearDTO, LibroDetalleDTO
from aplicacion.casos_uso.CU_GestionarLibros import GestionarLibros
from infraestructura.persistencia.configuracion import get_db
from infraestructura.persistencia.RepositorioLibroSQL import RepositorioLibroSQL

router = APIRouter(
    prefix="/libros",
    tags=["Biblioteca"]
)

# --- INICIO DE LA LÓGICA DE SEGURIDAD POR ROL ---

def solo_bibliotecarios(usuario_actual: Usuario = Depends(get_usuario_actual)):
    if usuario_actual.rol != RolUsuario.BIBLIOTECARIO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requiere rol de bibliotecario."
        )
    return usuario_actual

# --- FIN DE LA LÓGICA DE SEGURIDAD POR ROL ---

@router.post("/", response_model=LibroDetalleDTO, status_code=status.HTTP_201_CREATED)
def agregar_libro(
    libro_data: LibroCrearDTO,
    db: Session = Depends(get_db),
    # Esta dependencia asegura que solo los bibliotecarios puedan acceder
    usuario_bibliotecario: Usuario = Depends(solo_bibliotecarios)
):
    repo = RepositorioLibroSQL(db)
    caso_uso = GestionarLibros(repositorio_libro=repo)
    libro_creado = caso_uso.crear_libro(libro_data)
    return libro_creado

@router.get("/", response_model=List[LibroDetalleDTO])
def listar_libros(
    db: Session = Depends(get_db)
):
    repo = RepositorioLibroSQL(db)
    caso_uso = GestionarLibros(repositorio_libro=repo)
    return caso_uso.obtener_todos_los_libros()

@router.get("/{libro_id}", response_model=LibroDetalleDTO)
def obtener_libro(
    libro_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    repo = RepositorioLibroSQL(db)
    caso_uso = GestionarLibros(repositorio_libro=repo)
    libro = caso_uso.obtener_libro_por_id(libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado."
        )
    return libro