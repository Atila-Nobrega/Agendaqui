# Agendaqui
Agendaqui é uma plataforma web desenvolvida para facilitar o gerenciamento de agendamentos entre prestadores de serviço e clientes. Utilizando Clean Architecture, autenticação via OAuth 2.0 com Google e uma interface intuitiva, o sistema permite que usuários realizem agendamentos, acompanhem disponibilidades e recebam notificações automáticas.

# Tecnologias Utilizadas
- **Backend**: FastAPI, SQLAlchemy, Python

- **Frontend**: React.js + Vite, Javascript, Tailwind CSS
- **Banco de Dados**: PostgreSQL
- **Autenticação**: Google OAuth 2.0
- **Notificações**: Envio de e-mails via SMTP e biblioteca pythonsmtp

# Executando o projeto
## Clone o repositório
```
git clone https://github.com/seu-usuario/agendaqui.git
```

## Backend
```
cd agendaqui/backend
```

### Crie e ative o ambiente virtual
```
python -m venv venv
```
```
venv\Scripts\activate  # Windows
```

### Instale as dependências
```
pip install -r requirements.txt
```

### Configure as variáveis de ambiente
```
cp .env.example .env
```

### Execute o servidor FastAPI
```
uvicorn app.main:app --reload
```
## Frontend
```
cd agendaqui/frontend
```
### Instale as dependências
```
npm install
```

### Inicie o servidor de desenvolvimento
```
npm run dev
```
