from fastapi import APIRouter, Depends
from app.logic.auth import authorize, require_role
from app.models.user import UserRole

router = APIRouter()

@router.get("/public")
def public_route():
    """
    Rota pública acessível a qualquer usuário.
    """
    return {"message": "Esta é uma rota pública!"}

@router.get("/private")
def private_route(user: dict = Depends(authorize)):
    """
    Rota protegida, acessível apenas para usuários autenticados com JWT.
    """
    return {"message": "Esta é uma rota protegida!", "user": user}

@router.get("/cliente")
def cliente_route(user: dict = Depends(require_role(UserRole.CLIENTE))):
    return {"message": "Acesso permitido para CLIENTES!", "user": user}

@router.get("/prestador")
def prestador_route(user: dict = Depends(require_role(UserRole.PRESTADOR))):
    return {"message": "Acesso permitido para PRESTADORES!", "user": user}

@router.get("/admin")
def admin_route(user: dict = Depends(require_role(UserRole.ADMIN))):
    return {"message": "Acesso permitido para ADMIN!", "user": user}