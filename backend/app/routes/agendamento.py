from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.core.db import get_db
from app.db.agendamento import (
    criar_agendamento, listar_agendamentos_por_cliente,
    buscar_agendamento_por_id, cancelar_agendamento
)
from app.db.service import buscar_servico_por_id
from app.logic.auth import require_role
from app.models.user import UserRole

router = APIRouter()

class AgendamentoRequest(BaseModel):
    disponibilidade_id: str
    servico_id: str

@router.post("/")
def criar_novo_agendamento(
    request: AgendamentoRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_role(UserRole.CLIENTE))
):
    
    agendamento_data = {
        "id": str(uuid4()),
        "cliente_id": user["sub"],
        "prestador_id": buscar_servico_por_id(db, request.servico_id).prestador_id,
        "servico_id": request.servico_id,
        "disponibilidade_id": request.disponibilidade_id,
        "data_criacao": datetime.utcnow(),
        "status": "pendente"
    }
    
    agendamento = criar_agendamento(db, agendamento_data)
    if not agendamento:
        raise HTTPException(status_code=400, detail="Disponibilidade não está mais disponível.")

    return agendamento

@router.get("/")
def listar_agendamentos(db: Session = Depends(get_db), user: dict = Depends(require_role(UserRole.CLIENTE))):
    
    return listar_agendamentos_por_cliente(db, user["sub"])

@router.delete("/{agendamento_id}")
def cancelar_um_agendamento(agendamento_id: str, db: Session = Depends(get_db), user: dict = Depends(require_role(UserRole.CLIENTE))):

    agendamento = buscar_agendamento_por_id(db, agendamento_id)
    if agendamento.cliente_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Você não pode cancelar este agendamento.")
    elif not agendamento or agendamento.status.value == "cancelado":
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return cancelar_agendamento(db, agendamento)