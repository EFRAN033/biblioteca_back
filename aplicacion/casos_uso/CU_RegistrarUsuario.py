# efran033/biblioteca_back/biblioteca_back-e45426e2e00fbbc201232909bbf09d0ca9ea44ce/aplicacion/casos_uso/CU_RegistrarUsuario.py
from aplicacion.dto.UsuarioDTO import UsuarioRegistroDTO
from dominio.entidades.Usuario import Usuario
from dominio.puertos.IRepoUsuario import IRepoUsuario
from infraestructura.seguridad.password_hasher import PasswordHasher
from dominio.value_objects.RolUsuario import RolUsuario # <-- Importar
from dominio.value_objects.EstadoUsuario import EstadoUsuario # <-- Importar

class RegistrarUsuario:
    def __init__(self, repositorio_usuario: IRepoUsuario, hasher: PasswordHasher):
        self.repositorio_usuario = repositorio_usuario
        self.hasher = hasher

    def ejecutar(self, datos_registro: UsuarioRegistroDTO) -> Usuario:
        # Usamos 'datos_registro.correo' como definimos en el DTO
        if self.repositorio_usuario.existe_email(datos_registro.correo):
            raise ValueError("El correo electrónico ya está en uso.")

        hash_contrasena = None
        estado = EstadoUsuario.PENDIENTE # Por defecto es pendiente

        # Lógica condicional basada en el ROL
        if datos_registro.rol == RolUsuario.ESTUDIANTE:
            if not datos_registro.password or len(datos_registro.password) < 6:
                 raise ValueError("La contraseña es obligatoria y debe tener al menos 6 caracteres para estudiantes.")
            hash_contrasena = self.hasher.generar_hash(datos_registro.password)
            estado = EstadoUsuario.ACTIVO # Estudiantes se activan de inmediato
        
        # Para 'bibliotecario' y 'revisor', hash_contrasena queda como None
        # y el estado queda como 'pendiente'

        nuevo_usuario = Usuario(
            nombres=datos_registro.nombres,
            apellidos=datos_registro.apellidos, # <-- AÑADIR APELLIDOS
            email=datos_registro.correo,       # <-- Usar .correo
            hash_contrasena=hash_contrasena,     # <-- Usar variable condicional
            rol=datos_registro.rol,
            estado=estado                        # <-- AÑADIR ESTADO
        )
        
        return self.repositorio_usuario.guardar(nuevo_usuario)