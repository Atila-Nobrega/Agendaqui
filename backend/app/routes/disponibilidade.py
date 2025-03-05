from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.core.db import get_db
from app.db.disponibilidade import (
    criar_disponibilidade, listar_disponibilidades_por_servico,
    buscar_disponibilidade_por_id, atualizar_disponibilidade, deletar_disponibilidade,
    listar_disponibilidades_por_prestador
)
from app.db.service import buscar_servico_por_id
from app.logic.auth import require_role
from app.models.user import UserRole, User
from app.models.disponibilidade import Disponibilidade

router = APIRouter()

class DisponibilidadeRequest(BaseModel):
    servico_id: str
    inicio: datetime
    final: datetime

@router.get("/servico/{servico_id}")
def listar_disponibilidades(servico_id: str, db: Session = Depends(get_db)):

    return listar_disponibilidades_por_servico(db, servico_id)

@router.get("/prestador/{prestador_id}")
def listar_disponibilidades(prestador_id: str, db: Session = Depends(get_db)):

    disponibilidades = listar_disponibilidades_por_prestador(db, prestador_id)
    
    return [
        {
            "id": disp.id,
            "servico_id": disp.servico_id,
            "servico_nome": disp.servico.nome,
            "inicio": disp.inicio.isoformat(),
            "final": disp.final.isoformat(),
        }
        for disp in disponibilidades
    ]

@router.get("/prestador")
def listar_disponibilidades_por_email(email: str, db: Session = Depends(get_db)):

    prestador = db.query(User).filter(User.email == email, User.role == "PRESTADOR").first()
    
    if not prestador:
        raise HTTPException(status_code=404, detail="Prestador não encontrado.")

    disponibilidades = db.query(Disponibilidade).filter(Disponibilidade.prestador_id == prestador.id).all()

    return [
        {
            "id": disp.id,
            "servico_id": disp.servico_id,
            "servico_nome": disp.servico.nome,
            "inicio": disp.inicio.isoformat(),
            "final": disp.final.isoformat(),
            "status": disp.status,
        }
        for disp in disponibilidades
    ]

@router.post("/")
def criar_nova_disponibilidade(
    request: DisponibilidadeRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_role(UserRole.PRESTADOR))
):
    servico = buscar_servico_por_id(db, request.servico_id)
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")

    if servico.prestador_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Você só pode adicionar disponibilidades aos seus próprios serviços.")

    if request.inicio >= request.final:
        raise HTTPException(status_code=400, detail="Horário de início deve ser antes do horário final.")

    disponibilidade_data = {
        "id": str(uuid4()),
        "servico_id": request.servico_id,
        "prestador_id": user["sub"],
        "inicio": request.inicio,
        "final": request.final,
        "status": True
    }
    disponibilidade = criar_disponibilidade(db, disponibilidade_data)
    return disponibilidade

@router.post("/lote")
def criar_varias_disponibilidades(disponibilidades: List[DisponibilidadeRequest], db: Session = Depends(get_db), user: dict = Depends(require_role(UserRole.PRESTADOR))):
    """Recebe um array de disponibilidades e cria todas de uma vez"""
    
    novas_disponibilidades = []
    for disp in disponibilidades:
        nova_disp = Disponibilidade(
            id=str(uuid4()),
            servico_id=disp.servico_id,
            prestador_id=user["sub"],
            inicio=disp.inicio,
            final=disp.final,
        )
        db.add(nova_disp)
        novas_disponibilidades.append(nova_disp)

    db.commit()
    return {"message": f"{len(novas_disponibilidades)} disponibilidades criadas!"}

@router.put("/{disponibilidade_id}")
def editar_disponibilidade(
    disponibilidade_id: str,
    request: DisponibilidadeRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_role(UserRole.PRESTADOR))
):
    disponibilidade = buscar_disponibilidade_por_id(db, disponibilidade_id)
    if not disponibilidade:
        raise HTTPException(status_code=404, detail="Disponibilidade não encontrada.")

    servico = buscar_servico_por_id(db, disponibilidade.servico_id)
    if not servico or servico.prestador_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Você só pode editar disponibilidades dos seus próprios serviços.")

    disponibilidade_atualizada = atualizar_disponibilidade(db, disponibilidade, request.dict())
    return disponibilidade_atualizada

@router.delete("/{disponibilidade_id}")
def deletar_uma_disponibilidade(
    disponibilidade_id: str, db: Session = Depends(get_db),
    user: dict = Depends(require_role(UserRole.PRESTADOR))
):
    disponibilidade = buscar_disponibilidade_por_id(db, disponibilidade_id)
    if not disponibilidade:
        raise HTTPException(status_code=404, detail="Disponibilidade não encontrada.")

    servico = buscar_servico_por_id(db, disponibilidade.servico_id)
    if not servico or servico.prestador_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Você só pode excluir disponibilidades dos seus próprios serviços.")

    deletar_disponibilidade(db, disponibilidade)
    return {"message": "Disponibilidade deletada com sucesso."}