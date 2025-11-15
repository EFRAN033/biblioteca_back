# infraestructura/servicios/ServicioCorreo.py (Implementación Real - CORREGIDO)

import os
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from dominio.puertos.IServicioCorreo import IServicioCorreo
from dominio.entidades.Usuario import Usuario
from typing import Optional

# Cargar variables de entorno si no se han cargado (seguridad)
load_dotenv() 

# Configuración del servidor SMTP usando las variables del .env
# Esto requiere que tu app de Gmail o proveedor tenga habilitado el acceso por app password
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASS"),
    
    # 🚨 CORRECCIÓN 1: MAIL_FROM debe ser la dirección de correo
    MAIL_FROM=os.getenv("EMAIL_USER"),
    
    MAIL_PORT=int(os.getenv("EMAIL_PORT")),
    MAIL_SERVER=os.getenv("EMAIL_HOST"),
    
    # 🚨 CORRECCIÓN 2: MAIL_FROM_NAME es el nombre visible
    MAIL_FROM_NAME=os.getenv("EMAIL_SENDER"),
    
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    # Se usa 'FastMail' como motor de correo
)

class ServicioCorreo(IServicioCorreo):
    
    async def enviar_aprobacion(self, usuario: Usuario, contrasena_temporal: Optional[str] = None) -> bool:
        
        # 1. Crear el contenido del mensaje
        if contrasena_temporal:
            body_content = f"""
            ¡Hola {usuario.nombres}!
            
            Tu solicitud como **{usuario.rol.value.capitalize()}** en LibroHub ha sido **APROBADA**.
            
            Tus credenciales temporales son:
            - **Usuario (Email):** {usuario.email}
            - **Contraseña Temporal:** {contrasena_temporal}
            
            Por favor, inicia sesión y cambia tu contraseña de inmediato.
            """
        else:
            body_content = f"""
            ¡Hola {usuario.nombres}!
            
            Tu cuenta como **{usuario.rol.value.capitalize()}** en LibroHub ha sido **ACTIVADA**.
            Ya puedes acceder con tu contraseña registrada.
            """

        # 2. Configurar el mensaje
        message = MessageSchema(
            subject="🚀 Cuenta de LibroHub Aprobada y Activada",
            recipients=[usuario.email],  # Lista de destinatarios
            body=body_content,
            subtype=MessageType.plain,
            # subtype=MessageType.html # Usa HTML si el body es HTML
        )

        # 3. Enviar el correo usando FastAPI-Mail
        fm = FastMail(conf)
        try:
            # 💡 El endpoint aprobar_usuario en auth_router.py es ahora 'async'
            await fm.send_message(message) 
            print(f"INFO: Correo de aprobación enviado realmente a {usuario.email}")
            return True
        except Exception as e:
            # Revisa los detalles aquí si el envío falla (e.g., credenciales incorrectas o puerto bloqueado)
            print(f"ERROR: No se pudo enviar el correo a {usuario.email}. Detalles: {e}")
            return False