from sqlalchemy.orm import Session
from app.models.service import Servico

def criar_servico(db: Session, servico_data: dict):
    servico = Servico(**servico_data)
    db.add(servico)
    db.commit()
    db.refresh(servico)
    return servico

def listar_servicos(db: Session):
    return db.query(Servico).all()

def buscar_servico_por_id(db: Session, servico_id: str):
    return db.query(Servico).filter(Servico.id == servico_id).first()

def atualizar_servico(db: Session, servico: Servico, novos_dados: dict):
    for key, value in novos_dados.items():
        setattr(servico, key, value)
    db.commit()
    db.refresh(servico)
    return servico

def deletar_servico(db: Session, servico: Servico):
    db.delete(servico)
    db.commit()