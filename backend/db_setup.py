from app.core.db import Base, engine
from app.models.user import User
from app.models.service import Servico
from app.models.disponibilidade import Disponibilidade
from app.models.agendamento import Agendamento
from app.models.notificacao import Notificacao

print("🔹 Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("📌 Tabelas registradas:", Base.metadata.tables.keys())