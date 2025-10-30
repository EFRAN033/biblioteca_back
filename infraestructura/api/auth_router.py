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
        caso_uso.ejecutar(usuario_data)
        return {"mensaje": "Usuario creado exitosamente."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


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