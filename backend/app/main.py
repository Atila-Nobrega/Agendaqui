from fastapi import FastAPI
from app.routes import auth, example, user, service, disponibilidade, agendamento
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(example.router, prefix="/example", tags=["Exemplo"])
app.include_router(user.router, prefix="/user", tags=["Usuário"])
app.include_router(service.router, prefix="/servicos", tags=["Serviços"])
app.include_router(disponibilidade.router, prefix="/disponibilidade", tags=["Disponibilidade"])
app.include_router(agendamento.router, prefix="/agendamento", tags=["Agendamento"])

@app.get("/")
async def root():
    return {"message": "Hello World"}