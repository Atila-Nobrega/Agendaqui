from sqlalchemy.orm import Session
from app.models.agendamento import Agendamento, StatusAgendamento
from app.models.disponibilidade import Disponibilidade
from app.models.notificacao import TipoNotificacao
from app.db.notificacao import criar_notificacao

def criar_agendamento(db: Session, agendamento_data: dict):
    disponibilidade = db.query(Disponibilidade).filter(
        Disponibilidade.id == agendamento_data["disponibilidade_id"]
    ).first()

    if not disponibilidade or not disponibilidade.status:
        return None  # Horário não disponível

    agendamento = Agendamento(**agendamento_data)
    disponibilidade.status = False  # Marca a disponibilidade como ocupada

    db.add(agendamento)
    db.commit()
    db.refresh(agendamento)

    # NOTIFICAR
    criar_notificacao(db, agendamento, TipoNotificacao.AGENDAMENTO_CRIADO)

    return agendamento

def listar_agendamentos_por_cliente(db: Session, cliente_id: str):
    return db.query(Agendamento).filter(Agendamento.cliente_id == cliente_id).all()

def buscar_agendamento_por_id(db: Session, agendamento_id: str):
    return db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()

def cancelar_agendamento(db: Session, agendamento: Agendamento):
    disponibilidade = db.query(Disponibilidade).filter(
        Disponibilidade.id == agendamento.disponibilidade_id
    ).first()
    
    if disponibilidade:
        disponibilidade.status = True  # Libera a disponibilidade novamente

    agendamento.status = StatusAgendamento.CANCELADO
    db.commit()

    # NOTIFICACAO
    criar_notificacao(db, agendamento, TipoNotificacao.AGENDAMENTO_CANCELADO)

    return agendamento