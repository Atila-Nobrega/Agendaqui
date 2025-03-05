from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    prestador_id = Column(String, ForeignKey("prestadores.id"), nullable=False)

    prestador = relationship("Prestador", back_populates="servicos")
    disponibilidades = relationship("Disponibilidade", back_populates="servico", cascade="all, delete-orphan")
    agendamentos = relationship("Agendamento", back_populates="servico", cascade="all, delete-orphan")