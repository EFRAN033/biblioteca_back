from aplicacion.dto.UsuarioDTO import UsuarioLoginDTO, TokenDTO
from dominio.puertos.IRepoUsuario import IRepoUsuario
from infraestructura.seguridad.password_hasher import PasswordHasher
from infraestructura.seguridad.ServicioAutenticacionJWT import ServicioAutenticacionJWT

class AutenticarUsuario:
    def __init__(self, repositorio_usuario: IRepoUsuario, hasher: PasswordHasher, servicio_jwt: ServicioAutenticacionJWT):
        self.repositorio_usuario = repositorio_usuario
        self.hasher = hasher
        self.servicio_jwt = servicio_jwt

    def ejecutar(self, datos_login: UsuarioLoginDTO) -> TokenDTO:
        usuario = self.repositorio_usuario.obtener_por_email(datos_login.email)
        
        if not usuario:
            raise ValueError("Email o contraseña incorrectos.")
        
        if not self.hasher.verificar_contrasena(datos_login.password, usuario.hash_contrasena):
            raise ValueError("Email o contraseña incorrectos.")
            
        access_token = self.servicio_jwt.crear_access_token(
            data={"sub": usuario.email, "rol": usuario.rol.value}
        )
        
        return TokenDTO(access_token=access_token)