import uuid # Necesario para el user_id en la nueva ruta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# --- Importaciones Agregadas para Aprobación de Usuario y Seguridad ---
from dominio.entidades.Usuario import Usuario
from dominio.value_objects.RolUsuario import RolUsuario 
from aplicacion.casos_uso.CU_AprobarUsuario import AprobarUsuario # Caso de Uso nuevo
# Asume que 'get_usuario_actual' y 'UsuarioDetalleDTO' están disponibles:
from infraestructura.api.market_router import get_usuario_actual 
from aplicacion.dto.UsuarioDTO import UsuarioDetalleDTO 
# ---------------------------------------------------------------------

from aplicacion.dto.UsuarioDTO import UsuarioRegistroDTO, UsuarioLoginDTO, TokenDTO
from aplicacion.casos_uso.CU_RegistrarUsuario import RegistrarUsuario
from aplicacion.casos_uso.CU_AutenticarUsuario import AutenticarUsuario
from infraestructura.persistencia.configuracion import get_db
from infraestructura.persistencia.RepositorioUsuarioSQL import RepositorioUsuarioSQL
from infraestructura.seguridad.password_hasher import PasswordHasher
from infraestructura.seguridad.ServicioAutenticacionJWT import ServicioAutenticacionJWT

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

# --- DEPENDENCIA DE SEGURIDAD PARA ADMINISTRADORES ---
# Función para asegurar que solo los usuarios con rol ADMIN accedan
def solo_admins(usuario_actual: Usuario = Depends(get_usuario_actual)):
    if usuario_actual.rol != RolUsuario.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requiere rol de administrador."
        )
    return usuario_actual
# ----------------------------------------------------


@router.post("/register", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_data: UsuarioRegistroDTO, db: Session = Depends(get_db)):
    try:
        repo = RepositorioUsuarioSQL(db)
        hasher = PasswordHasher()
        caso_uso = RegistrarUsuario(repositorio_usuario=repo, hasher=hasher)
        
        caso_uso.ejecutar(usuario_data) 
        
        # Mensaje de éxito genérico
        if usuario_data.rol == RolUsuario.ESTUDIANTE: # RolUsuario debe estar importado
             return {"mensaje": "Usuario creado exitosamente."}
        else:
             return {"mensaje": "Solicitud de registro enviada para revisión."}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Captura de errores inesperados
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrió un error inesperado.")


@router.post("/login", response_model=TokenDTO)
def login_para_access_token(usuario_data: UsuarioLoginDTO, db: Session = Depends(get_db)):
    try:
        repo = RepositorioUsuarioSQL(db)
        hasher = PasswordHasher()
        servicio_jwt = ServicioAutenticacionJWT()
        caso_uso = AutenticarUsuario(repositorio_usuario=repo, hasher=hasher, servicio_jwt=servicio_jwt)
        token = caso_uso.ejecutar(usuario_data)
        return token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


# --- NUEVO ENDPOINT PARA APROBACIÓN DE USUARIOS ---
@router.patch("/users/{user_id}/approve", response_model=UsuarioDetalleDTO)
def aprobar_usuario(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    # Aplica la dependencia para que solo los ADMIN puedan usar esta ruta
    admin_actual: Usuario = Depends(solo_admins) 
):
    """
    Permite al Administrador cambiar el estado de un usuario de PENDIENTE a ACTIVO.
    """
    try:
        repo = RepositorioUsuarioSQL(db)
        caso_uso = AprobarUsuario(repositorio_usuario=repo)
        
        usuario_aprobado = caso_uso.ejecutar(user_id)
        
        return usuario_aprobado
    except ValueError as e:
        # Errores esperados del caso de uso (ej. usuario no encontrado, ya activo)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
# ----------------------------------------------------