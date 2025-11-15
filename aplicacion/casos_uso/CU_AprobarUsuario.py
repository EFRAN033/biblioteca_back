from dominio.puertos.IRepoUsuario import IRepoUsuario
from dominio.entidades.Usuario import Usuario
from dominio.value_objects.EstadoUsuario import EstadoUsuario
import uuid

class AprobarUsuario:
    def __init__(self, repositorio_usuario: IRepoUsuario):
        self.repositorio_usuario = repositorio_usuario

    def ejecutar(self, usuario_id: uuid.UUID) -> Usuario:
        usuario = self.repositorio_usuario.obtener_por_id(usuario_id) # Se requiere este método en IRepoUsuario

        if not usuario:
            raise ValueError("Usuario no encontrado.")

        if usuario.estado != EstadoUsuario.PENDIENTE:
            raise ValueError(f"El usuario ya se encuentra en estado {usuario.estado.value}.")

        # Actualizar el estado
        usuario.estado = EstadoUsuario.ACTIVO
        
        # Guardar (actualizar) el usuario.
        return self.repositorio_usuario.guardar(usuario)

# Nota: Necesitarás añadir `obtener_por_id` en `IRepoUsuario` y en `RepositorioUsuarioSQL.py`.