# auth.py

import jwt
from datetime import datetime, timedelta

# Chave secreta para assinar e verificar tokens JWT
SECRET_KEY = "sua_chave_secreta"

def login(username, password):
    if username == "admin" and password == "admin":
        # Gera um token JWT válido por 1 hora
        token = jwt.encode({"username": username, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
        return token
    else:
        return None

def verify_token(token):
    try:
        # Verifica e decodifica o token JWT
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Token expirado
        return None
    except jwt.InvalidTokenError:
        # Token inválido
        return None
