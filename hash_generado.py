from passlib.context import CryptContext

# --- CONFIGURACIÓN ---
# Define el contexto de cifrado (debe coincidir con la configuración de tu API, típicamente bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ¡IMPORTANTE! Reemplaza esto con la contraseña que deseas para el administrador.
password_plana = "TU_CONTRASEÑA_ADMINISTRADOR" 
MAX_PASSWORD_LENGTH = 72 # Límite de 72 bytes para Bcrypt

# --- GENERACIÓN DE HASH ---
print("--- Iniciando Generación de Hash Bcrypt ---")

# 1. Verificar la longitud y truncar si es necesario
if len(password_plana.encode('utf-8')) > MAX_PASSWORD_LENGTH:
    # Truncar la contraseña a los primeros 72 caracteres
    password_to_hash = password_plana[:MAX_PASSWORD_LENGTH]
    print(f"ADVERTENCIA: Contraseña truncada de {len(password_plana)} a {len(password_to_hash)} caracteres para Bcrypt.")
else:
    password_to_hash = password_plana

# 2. Generar el hash
try:
    hash_generado = pwd_context.hash(password_to_hash)
    
    # 3. Mostrar el resultado
    print("--------------------------------------------------")
    print(f"Contraseña Plana usada: {password_to_hash}")
    print(f"Hash Generado (¡Cópialo!): {hash_generado}")
    print("--------------------------------------------------")

except Exception as e:
    print(f"ERROR FATAL: No se pudo generar el hash. Mensaje: {e}")
    print("Intenta reinstalar passlib y bcrypt si el problema persiste.")