from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


# Configuração do banco de dados via ORM

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "sqlite:///tarefas.db"

engine = create_engine(DATABASE_URL, connect_args={ "check_same_thread": False })

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelo da tabela

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

class TarefaDB(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    descricao = Column(String, nullable=False)
    concluida = Column(Boolean, default=False)

# Criação da tabela

Base.metadata.create_all(bind=engine)

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

app = FastAPI()

USUARIO = "admin"
SENHA = "admin"

security = HTTPBasic()

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário e/ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/adicionar_tarefa")
def adicionar_tarefa(tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(validar_usuario)):
    db_tarefa = (db.query(TarefaDB).filter(TarefaDB.nome == tarefa.nome).first())

    if db_tarefa:
        raise HTTPException(status_code=400, detail="Tarefa já cadastrada.")

    nova_tarefa = TarefaDB(
        nome=tarefa.nome,
        descricao=tarefa.descricao,
        concluida=tarefa.concluida
    )

    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return { "message": "Tarefa adicionada com sucesso." }

@app.get("/tarefas")
def listar_tarefas(page: int = 1, size: int = 10, sort_by: str = "nome", db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(validar_usuario)):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="page ou size inválido.")

    if sort_by == "nome":
        query = db.query(TarefaDB).order_by(TarefaDB.nome)
    elif sort_by == "descricao":
        query = db.query(TarefaDB).order_by(TarefaDB.descricao)

    if not tarefas:
        raise HTTPException(status_code=404, detail="Nenhuma tarefa cadastrada.")

    total = query.count()

    tarefas = (query.offset((page - 1) * size).limit(size).all())

    return {
        "page": page,
        "size": size,
        "total": total,
        "tarefas": tarefas
    }

@app.put("/marcar_concluida/{nome}")
def marcar_concluida(nome: str, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(validar_usuario)):
    db_tarefa = (db.query(TarefaDB).filter(TarefaDB.nome == nome).first())

    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não cadastrada.")

    db_tarefa.concluida = True
    db.commit()
    db.refresh(db_tarefa)

    return { message: "Tarefa '{nome}' marcada como concluída." }

@app.delete("/remover_tarefa/{nome}")
def remover_tarefa(nome: str, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(validar_usuario)):
    db_tarefa = (db.query(TarefaDB).filter(TarefaDB.nome == nome).first())

    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não cadastrada.")

    db.delete(db_tarefa)
    db.commit()

    return { message: "Tarefa excluída com sucesso."}