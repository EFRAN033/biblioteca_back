import logging # <-- NUEVO: Importar librería de logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importaciones de seguridad
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os

# Importaciones de nuestro proyecto
from aplicacion.dto.ProductoMarketDTO import ProductoCrearDTO, ProductoPublicadoDTO
from aplicacion.casos_uso.CU_AgregarProductoMarket import AgregarProductoMarket
from infraestructura.persistencia.configuracion import get_db
from infraestructura.persistencia.RepositorioProductoMarketSQL import RepositorioProductoMarketSQL
from infraestructura.persistencia.RepositorioUsuarioSQL import RepositorioUsuarioSQL 
from dominio.entidades.Usuario import Usuario

# Configuración básica de logging
# Esto ayuda a que los mensajes de log aparezcan en la consola de Uvicorn
logging.basicConfig(level=logging.INFO) # <-- NUEVO

router = APIRouter(
    prefix="/market",
    tags=["Marketplace"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def get_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    logging.info(f"Intentando validar token...") # <-- LOG
    
    try:
        # Intenta decodificar el token usando la clave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        rol: str = payload.get("rol") 
        
        logging.info(f"Token Decodificado. Email: {email}, Rol: {rol}") # <-- LOG
        
        if email is None:
            logging.error("JWT decodificado pero 'sub' (email) es None.") # <-- LOG
            raise credentials_exception
    except JWTError as e:
        # Si la decodificación falla (ej. clave incorrecta o token expirado/manipulado)
        logging.error(f"Error al decodificar JWT: {e}") # <-- LOG
        raise credentials_exception
    except Exception as e:
        logging.error(f"Error inesperado durante la decodificación: {e}") # <-- LOG
        raise credentials_exception
    
    repo_usuario = RepositorioUsuarioSQL(db)
    usuario = repo_usuario.obtener_por_email(email=email)
    
    if usuario is None:
        # Si el usuario no se encuentra en la DB, aunque el token sea válido
        logging.error(f"Usuario con email {email} no encontrado en DB.") # <-- LOG
        raise credentials_exception
        
    logging.info(f"Usuario {usuario.nombres} ({usuario.rol.value}) cargado exitosamente.") # <-- LOG
    return usuario

@router.post("/", response_model=ProductoPublicadoDTO, status_code=status.HTTP_201_CREATED)
def agregar_producto(
    producto_data: ProductoCrearDTO, 
    db: Session = Depends(get_db), 
    usuario_actual: Usuario = Depends(get_usuario_actual)
):
    try:
        repo = RepositorioProductoMarketSQL(db)
        caso_uso = AgregarProductoMarket(repositorio_producto=repo)
        
        producto_creado = caso_uso.ejecutar(producto_data, usuario_actual.id)
        
        return producto_creado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))