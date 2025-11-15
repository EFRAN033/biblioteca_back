# infraestructura/servicios/ServicioCorreo.py

from dominio.puertos.IServicioCorreo import IServicioCorreo
from dominio.entidades.Usuario import Usuario

class ServicioCorreo(IServicioCorreo):
    """
    Implementación básica para simular el envío de correos.
    En un entorno real, usarías SMTP o un API como SendGrid.
    """
    def enviar_aprobacion(self, usuario: Usuario, contrasena_temporal: str = None) -> bool:
        print("\n" + "="*50)
        print(f"ENVIANDO CORREO DE APROBACIÓN a: {usuario.email}")
        print(f"ROL: {usuario.rol.value.upper()} APROBADO")
        
        if contrasena_temporal:
            print("--- CREDENCIALES ---")
            print(f"Usuario (Email): {usuario.email}")
            print(f"Contraseña Temporal: {contrasena_temporal}")
            print("--------------------")
            print("Instrucción: ¡Por favor, cambia tu contraseña de inmediato!")
        else:
            print("Instrucción: Tu cuenta ha sido activada. Tu acceso es con la contraseña que registraste.")
            
        print("="*50 + "\n")
        
        return True