# importações necessárias de hora e data
from datetime import datetime, timedelta
# Importa o JWT para manipulação de tokens
from jose import JWTError, jwt

# FastAPI Authentication Module
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer


# Importa o modelo de usuário e a função de obter o banco de dados
from app.database import get_db
from app.models import User

# 🔑 Chave secreta para assinar os tokens (use uma chave forte em produção!)
SECRET_KEY = "minha_chave_super_secreta"
ALGORITHM = "HS256"

# Tempo padrão de expiração do token (30 min)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Função para criar um token de acesso JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Gera um token JWT com os dados fornecidos (ex: {"sub": email}).
    """
    to_encode = data.copy()

    # Define expiração do token
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # Cria e retorna o token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# validate and decode a JWT access token
def decode_access_token(token: str) -> dict | None:
    """
    Valida e decodifica um token JWT. Retorna o payload ou None se inválido/expirado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Endpoint de login que fornece o token
# Vai buscar o token diretamente no header Authorization
# Agora o Swagger sabe que para autenticar deve usar /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para obter o usuário atual a partir do token
# Esta função é usada como dependência nas rotas que precisam de autenticação
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # Remove o prefixo Bearer se vier junto
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user
