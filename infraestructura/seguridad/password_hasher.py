import bcrypt

class PasswordHasher:
    @staticmethod
    def generar_hash(contrasena: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verificar_contrasena(contrasena_plana: str, hash_contrasena: str) -> bool:
        return bcrypt.checkpw(contrasena_plana.encode('utf-8'), hash_contrasena.encode('utf-8'))