from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.db import Base
from datetime import datetime
import enum

class StatusAgendamento(str, enum.Enum):
    PENDENTE = "pendente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(String, primary_key=True, index=True)
    cliente_id = Column(String, ForeignKey("clientes.id"), nullable=False)
    prestador_id = Column(String, ForeignKey("prestadores.id"), nullable=False)
    servico_id = Column(String, ForeignKey("servicos.id"), nullable=False)
    disponibilidade_id = Column(String, ForeignKey("disponibilidades.id"), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE)

    cliente = relationship("Cliente", back_populates="agendamentos")
    prestador = relationship("Prestador", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")
    disponibilidade = relationship("Disponibilidade", back_populates="agendamentos")
    notificacoes = relationship("Notificacao", back_populates="agendamento", cascade="all, delete-orphan")