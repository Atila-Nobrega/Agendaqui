from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security, Depends, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import settings
from app.models.user import UserRole

security = HTTPBearer()

def create_access_token(data: dict):
    "Gera um token JWT com tempo de expiração."

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_access_token(token: str):
    "Valida o JWT e retorna o payload se for válido."

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

def authorize(credentials: HTTPAuthorizationCredentials = Security(security)):
    return verify_access_token(credentials.credentials)

def require_role(required_role: UserRole):
    "Verifica se o usuário autenticado tem o papel necessário"

    def role_dependency(user: dict = Depends(authorize)):
        if user["role"] != required_role.value:
            raise HTTPException(status_code=403, detail="Acesso negado.")
        return user
    return role_dependency