from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from app.logic.auth import create_access_token
from sqlalchemy.orm import Session
from app.logic.auth import authorize
from app.models.user import User, Cliente, Prestador, UserRole
from app.core.db import get_db

router = APIRouter()

class RoleUpdateRequest(BaseModel):
    role: UserRole

@router.post("/update-role")
def update_user_role(request: RoleUpdateRequest, db: Session = Depends(get_db), user: dict = Depends(authorize)):
    
    db_user = db.query(User).filter(User.id == user["sub"]).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if db_user.role != UserRole.USER:
        raise HTTPException(status_code=400, detail="Usuário já tem um papel definido.")

    if request.role == UserRole.CLIENTE:
        new_role = Cliente(id=db_user.id, user=db_user)
    elif request.role == UserRole.PRESTADOR:
        new_role = Prestador(id=db_user.id, user=db_user)
    else:
        raise HTTPException(status_code=400, detail="Papel inválido.")

    db.add(new_role)
    db_user.role = request.role
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token(data={"sub": db_user.id, "role": db_user.role.value})
    
    return {"message": f"Usuário agora é {db_user.role.value}!", "access_token": access_token}