# infraestructura/seguridad/ServicioAutenticacionJWT.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class ServicioAutenticacionJWT:
    SECRET_KEY = os.getenv("JWT_SECRET")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def crear_access_token(self, data: dict) -> str:
        a_codificar = data.copy()
        expira = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        a_codificar.update({"exp": expira})
        token_jwt_codificado = jwt.encode(a_codificar, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token_jwt_codificado