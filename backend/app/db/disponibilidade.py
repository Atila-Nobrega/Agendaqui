from sqlalchemy.orm import Session
from app.models.disponibilidade import Disponibilidade

def criar_disponibilidade(db: Session, disponibilidade_data: dict):
    disponibilidade = Disponibilidade(**disponibilidade_data)
    db.add(disponibilidade)
    db.commit()
    db.refresh(disponibilidade)
    return disponibilidade

def listar_disponibilidades_por_servico(db: Session, servico_id: str):
    return db.query(Disponibilidade).filter(Disponibilidade.servico_id == servico_id).all()

def listar_disponibilidades_por_prestador(db: Session, prestador_id: str):
    return db.query(Disponibilidade).filter(Disponibilidade.prestador_id == prestador_id).all()

def buscar_disponibilidade_por_id(db: Session, disponibilidade_id: str):
    return db.query(Disponibilidade).filter(Disponibilidade.id == disponibilidade_id).first()

def atualizar_disponibilidade(db: Session, disponibilidade: Disponibilidade, novos_dados: dict):
    for key, value in novos_dados.items():
        setattr(disponibilidade, key, value)
    db.commit()
    db.refresh(disponibilidade)
    return disponibilidade

def deletar_disponibilidade(db: Session, disponibilidade: Disponibilidade):
    db.delete(disponibilidade)
    db.commit()