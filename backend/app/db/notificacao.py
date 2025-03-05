from sqlalchemy.orm import Session
from app.models.notificacao import Notificacao, TipoNotificacao
from app.models.agendamento import Agendamento
from uuid import uuid4
from datetime import datetime
from app.core.email import enviar_email
from app.adapters.email import gerar_email_agendamento

def criar_notificacao(db: Session, agendamento: Agendamento, tipo: TipoNotificacao):

    if tipo == TipoNotificacao.AGENDAMENTO_CRIADO:
        status_texto = "Confirmado"
    else:
        status_texto = "Cancelado"

    email_cliente = gerar_email_agendamento(
        agendamento.cliente.user.name,
        agendamento.servico.nome,
        status_texto,
        agendamento.disponibilidade.inicio.strftime("%d/%m/%Y %H:%M"),
        agendamento.prestador.user.name
    )

    email_prestador = gerar_email_agendamento(
        agendamento.prestador.user.name,
        agendamento.servico.nome,
        status_texto,
        agendamento.disponibilidade.inicio.strftime("%d/%m/%Y %H:%M"),
        agendamento.cliente.user.name
    )

    notificacao = Notificacao(
        id=str(uuid4()),
        agendamento_id=agendamento.id,
        tipo=tipo,
        data_envio=datetime.utcnow()
    )
    db.add(notificacao)
    db.commit()
    db.refresh(notificacao)

    # Enviar e-mail
    enviar_email(agendamento.cliente.user.email, "Atualização no Agendamento", email_cliente)
    enviar_email(agendamento.prestador.user.email, "Atualização no Agendamento", email_prestador)

    return notificacao