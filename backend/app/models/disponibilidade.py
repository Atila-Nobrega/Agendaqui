from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base

class Disponibilidade(Base):
    __tablename__ = "disponibilidades"

    id = Column(String, primary_key=True, index=True)
    servico_id = Column(String, ForeignKey("servicos.id"), nullable=False)
    prestador_id = Column(String, ForeignKey("prestadores.id"), nullable=False)
    inicio = Column(DateTime, nullable=False)
    final = Column(DateTime, nullable=False)
    status = Column(Boolean, default=True)

    servico = relationship("Servico", back_populates="disponibilidades")
    prestador = relationship("Prestador", back_populates="disponibilidades")
    agendamentos = relationship("Agendamento", back_populates="disponibilidade")