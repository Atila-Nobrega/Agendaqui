from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from app.core.db import get_db
from app.db.service import criar_servico, listar_servicos, buscar_servico_por_id, atualizar_servico, deletar_servico
from app.logic.auth import authorize, require_role
from app.models.user import UserRole

router = APIRouter()

class ServicoCreateRequest(BaseModel):
    nome: str
    descricao: str
    preco: float

class ServicoUpdateRequest(BaseModel):
    nome: str
    descricao: str
    preco: float

@router.post("/")
def criar_novo_servico(request: ServicoCreateRequest, db: Session = Depends(get_db), user: dict = Depends(require_role(UserRole.PRESTADOR))):

    servico_data = {
        "id": str(uuid4()),
        "nome": request.nome,
        "descricao": request.descricao,
        "preco": request.preco,
        "prestador_id": user["sub"]  # Pegando o ID do usuário autenticado
    }
    servico = criar_servico(db, servico_data)
    return servico

@router.get("/")
def listar_todos_servicos(db: Session = Depends(get_db)):

    return listar_servicos(db)

@router.put("/{servico_id}")
def editar_servico(servico_id: str, request: ServicoUpdateRequest, db: Session = Depends(get_db), user: dict = Depends(require_role(UserRole.PRESTADOR))):

    servico = buscar_servico_por_id(db, servico_id)
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")

    if servico.prestador_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Você não pode editar um serviço de outro prestador.")

    servico_atualizado = atualizar_servico(db, servico, {"nome": request.nome, "descricao": request.descricao, "preco": request.preco})
    return servico_atualizado

@router.delete("/{servico_id}")
def deletar_um_servico(servico_id: str, db: Session = Depends(get_db), user: dict = Depends(require_role(UserRole.PRESTADOR))):

    servico = buscar_servico_por_id(db, servico_id)
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")

    if servico.prestador_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Você não pode excluir um serviço de outro prestador.")

    deletar_servico(db, servico)
    return {"message": "Serviço deletado com sucesso."}