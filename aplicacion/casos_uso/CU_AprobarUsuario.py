from dominio.puertos.IRepoUsuario import IRepoUsuario
from dominio.entidades.Usuario import Usuario
from dominio.value_objects.EstadoUsuario import EstadoUsuario
import uuid
from typing import Optional # <--- AÑADIDO: Necesario para el tipado de contrasena_plana
# --- NUEVAS IMPORTACIONES PARA CORREO Y HASH ---
from dominio.puertos.IServicioCorreo import IServicioCorreo 
from infraestructura.seguridad.password_hasher import PasswordHasher 
import secrets 
import string 
# -----------------------------------------------

class AprobarUsuario:
    # ⬇️ CONSTRUCTOR CORREGIDO: Inyectar servicio_correo y hasher
    def __init__(self, repositorio_usuario: IRepoUsuario, servicio_correo: IServicioCorreo, hasher: PasswordHasher):
        self.repositorio_usuario = repositorio_usuario
        self.servicio_correo = servicio_correo 
        self.hasher = hasher

    # 🚨 CORRECCIÓN CLAVE 1: La función debe ser asíncrona
    async def ejecutar(self, usuario_id: uuid.UUID) -> Usuario:
        usuario = self.repositorio_usuario.obtener_por_id(usuario_id) 

        if not usuario:
            raise ValueError("Usuario no encontrado.")

        if usuario.estado != EstadoUsuario.PENDIENTE:
            raise ValueError(f"El usuario ya se encuentra en estado {usuario.estado.value}.")

        # --- LÓGICA DE GENERACIÓN Y HASH DE CONTRASEÑA ---
        contrasena_plana: Optional[str] = None # Tipado correcto
        
        # Si no tiene hash (es bibliotecario o revisor pendiente), se genera una contraseña temporal
        if usuario.hash_contrasena is None:
            # Crea un alfabeto de letras y dígitos
            alfabeto = string.ascii_letters + string.digits
            # Genera la contraseña temporal
            contrasena_plana = ''.join(secrets.choice(alfabeto) for i in range(12))
            
            # 1. Hashea la contraseña temporal
            usuario.hash_contrasena = self.hasher.generar_hash(contrasena_plana)
        # --------------------------------------------------

        # 2. Actualizar el estado
        usuario.estado = EstadoUsuario.ACTIVO
        
        # 3. Guardar (actualizar) el usuario en la DB con el nuevo hash
        usuario_aprobado = self.repositorio_usuario.guardar(usuario)

        # 4. Enviar notificación por correo (se pasa la contraseña plana si se generó)
        # 🚨 CORRECCIÓN CLAVE 2: Se usa await para la llamada asíncrona
        await self.servicio_correo.enviar_aprobacion(usuario_aprobado, contrasena_plana) 
        
        return usuario_aprobado