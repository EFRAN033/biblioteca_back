from aplicacion.dto.UsuarioDTO import UsuarioRegistroDTO
from dominio.entidades.Usuario import Usuario
from dominio.puertos.IRepoUsuario import IRepoUsuario
from infraestructura.seguridad.password_hasher import PasswordHasher

class RegistrarUsuario:
    def __init__(self, repositorio_usuario: IRepoUsuario, hasher: PasswordHasher):
        self.repositorio_usuario = repositorio_usuario
        self.hasher = hasher

    def ejecutar(self, datos_registro: UsuarioRegistroDTO) -> Usuario:
        if self.repositorio_usuario.existe_email(datos_registro.email):
            raise ValueError("El correo electrónico ya está en uso.")

        hash_contrasena = self.hasher.generar_hash(datos_registro.password)
        
        nuevo_usuario = Usuario(
            nombres=datos_registro.nombres,
            email=datos_registro.email,
            hash_contrasena=hash_contrasena,
            rol=datos_registro.rol
        )
        
        return self.repositorio_usuario.guardar(nuevo_usuario)