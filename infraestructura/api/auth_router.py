# efran033/biblioteca_back/biblioteca_back-e45426e2e00fbbc201232909bbf09d0ca9ea44ce/infraestructura/api/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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

@router.post("/register", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_data: UsuarioRegistroDTO, db: Session = Depends(get_db)):
    try:
        repo = RepositorioUsuarioSQL(db)
        hasher = PasswordHasher()
        caso_uso = RegistrarUsuario(repositorio_usuario=repo, hasher=hasher)
        
        # El DTO 'usuario_data' ahora coincide con el JSON del frontend
        # y el caso de uso 'ejecutar' maneja la nueva lógica
        caso_uso.ejecutar(usuario_data) 
        
        # Mensaje de éxito genérico
        if usuario_data.rol == RolUsuario.ESTUDIANTE:
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