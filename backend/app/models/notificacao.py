from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.db import Base
from datetime import datetime
import enum

class TipoNotificacao(str, enum.Enum):
    AGENDAMENTO_CRIADO = "agendamento_criado"
    AGENDAMENTO_CANCELADO = "agendamento_cancelado"

class Notificacao(Base):
    __tablename__ = "notificacoes"

    id = Column(String, primary_key=True, index=True)
    agendamento_id = Column(String, ForeignKey("agendamentos.id"), nullable=False)
    tipo = Column(Enum(TipoNotificacao), nullable=False)
    data_envio = Column(DateTime, default=datetime.utcnow)

    agendamento = relationship("Agendamento", back_populates="notificacoes")