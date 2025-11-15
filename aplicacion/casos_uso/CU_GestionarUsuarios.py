from dominio.puertos.IRepoUsuario import IRepoUsuario
from dominio.entidades.Usuario import Usuario
from typing import List

class GestionarUsuarios:
    def __init__(self, repositorio_usuario: IRepoUsuario):
        self.repositorio_usuario = repositorio_usuario

    def obtener_todos_los_usuarios(self) -> List[Usuario]:
        """
        Caso de uso para obtener la lista completa de usuarios del sistema.
        """
        # Llama al método obtener_todos del repositorio, el cual ahora está implementado.
        return self.repositorio_usuario.obtener_todos()