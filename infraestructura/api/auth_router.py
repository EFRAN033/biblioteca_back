import uuid 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List # <-- Necesario para el tipo de retorno List[UsuarioDetalleDTO]

# --- Importaciones de Capa de Dominio y Seguridad ---
from dominio.entidades.Usuario import Usuario
from dominio.value_objects.RolUsuario import RolUsuario 
from infraestructura.api.market_router import get_usuario_actual # Dependencia de seguridad
# ----------------------------------------------------

# --- Importaciones de Capa de Aplicación ---
from aplicacion.dto.UsuarioDTO import UsuarioRegistroDTO, UsuarioLoginDTO, TokenDTO, UsuarioDetalleDTO
from aplicacion.casos_uso.CU_RegistrarUsuario import RegistrarUsuario
from aplicacion.casos_uso.CU_AutenticarUsuario import AutenticarUsuario
from aplicacion.casos_uso.CU_AprobarUsuario import AprobarUsuario 
from aplicacion.casos_uso.CU_GestionarUsuarios import GestionarUsuarios 
# ----------------------------------------------------

# --- Importaciones de Capa de Infraestructura (CORREGIDO) ---
from infraestructura.persistencia.configuracion import get_db
from infraestructura.persistencia.RepositorioUsuarioSQL import RepositorioUsuarioSQL
from infraestructura.seguridad.password_hasher import PasswordHasher
from infraestructura.seguridad.ServicioAutenticacionJWT import ServicioAutenticacionJWT
# ⬇️ NUEVA IMPORTACIÓN: Debes asegurar que la ruta a tu ServicioCorreo sea correcta
from infraestructura.servicios.ServicioCorreo import ServicioCorreo 
# ----------------------------------------------------


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
        
        if usuario_data.rol == RolUsuario.ESTUDIANTE:
             return {"mensaje": "Usuario creado exitosamente."}
        else:
             return {"mensaje": "Solicitud de registro enviada para revisión."}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
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


# --- ENDPOINT PARA APROBACIÓN DE USUARIOS (CORREGIDO) ---
@router.patch("/users/{user_id}/approve", response_model=UsuarioDetalleDTO)
def aprobar_usuario(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin_actual: Usuario = Depends(solo_admins) 
):
    """
    Permite al Administrador cambiar el estado de un usuario de PENDIENTE a ACTIVO.
    Inicia la generación de credenciales y el envío de correo.
    """
    try:
        repo = RepositorioUsuarioSQL(db)
        # ⬇️ Instanciar y pasar las dependencias para el nuevo flujo
        servicio_correo = ServicioCorreo() 
        hasher = PasswordHasher()
        
        caso_uso = AprobarUsuario(
            repositorio_usuario=repo,
            servicio_correo=servicio_correo,
            hasher=hasher
        )
        
        usuario_aprobado = caso_uso.ejecutar(user_id)
        
        return usuario_aprobado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# --- ENDPOINT PARA OBTENER TODOS LOS USUARIOS ---
@router.get("/users", response_model=List[UsuarioDetalleDTO]) 
def listar_usuarios(
    db: Session = Depends(get_db),
    admin_actual: Usuario = Depends(solo_admins) # Protegido: Solo ADMIN puede listar
):
    """
    Obtiene la lista de todos los usuarios registrados. Requiere rol de administrador.
    """
    try:
        repo = RepositorioUsuarioSQL(db)
        caso_uso = GestionarUsuarios(repositorio_usuario=repo)
        return caso_uso.obtener_todos_los_usuarios()
    except Exception as e:
        # Esto atraparía errores internos, como si la DB no estuviera accesible.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))