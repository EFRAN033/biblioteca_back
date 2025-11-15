# dominio/puertos/IServicioCorreo.py
from abc import ABC, abstractmethod
from dominio.entidades.Usuario import Usuario

class IServicioCorreo(ABC):
    
    @abstractmethod
    def enviar_aprobacion(self, usuario: Usuario, contrasena_temporal: str = None) -> bool:
        """Envía el correo de notificación al usuario aprobado."""
        pass