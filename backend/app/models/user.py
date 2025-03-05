from sqlalchemy import Column, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    PRESTADOR = "prestador"
    CLIENTE = "cliente"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # same as google id
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    picture = Column(String, nullable=True)
    verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER)

    #(herança)
    cliente = relationship("Cliente", uselist=False, back_populates="user")
    prestador = relationship("Prestador", uselist=False, back_populates="user")

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(String, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="cliente")

    agendamentos = relationship("Agendamento", back_populates="cliente", cascade="all, delete-orphan")

class Prestador(Base):
    __tablename__ = "prestadores"

    id = Column(String, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="prestador")

    servicos = relationship("Servico", back_populates="prestador")
    agendamentos = relationship("Agendamento", back_populates="prestador", cascade="all, delete-orphan")
    disponibilidades = relationship("Disponibilidade", back_populates="prestador", cascade="all, delete-orphan")