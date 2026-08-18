from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

app = FastAPI()

USUARIO = "admin"
SENHA = "admin"

security = HTTPBasic()

lista_tarefas: list[Tarefa] = []

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
def adicionar_tarefa(tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(validar_usuario)):
    if tarefa.nome in [t.nome for t in lista_tarefas]:
        raise HTTPException(status_code=400, detail="Tarefa já cadastrada.")
    lista_tarefas.append(tarefa)
    return { "message": "Tarefa adicionada com sucesso.", "tarefa": tarefa}

@app.get("/tarefas")
def listar_tarefas(page: int = 1, size: int = 10, sort_by: str = "nome", credentials: HTTPBasicCredentials = Depends(validar_usuario)):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="page ou size inválido.")
    if not lista_tarefas:
        raise HTTPException(status_code=404, detail="Nenhuma tarefa cadastrada.")
    start = (page - 1) * size
    end = start + size
    campos_validos = ["nome", "descricao"]
    if sort_by not in campos_validos:
        raise HTTPException(status_code=400, detail=f"Campo inválido. Use {','.join(campos_validos)}")
    tarefas_ordenadas = sorted(lista_tarefas, key=lambda tarefa: getattr(tarefa, sort_by))
    tarefas_paginadas = tarefas_ordenadas[start:end]
    return {
        "page": page,
        "size": size,
        "total": len(lista_tarefas),
        "tarefas": tarefas_paginadas
    }

@app.put("/marcar_concluida/{nome}")
def marcar_concluida(nome: str, credentials: HTTPBasicCredentials = Depends(validar_usuario)):
    for tarefa in lista_tarefas:
        if tarefa.nome == nome:
            tarefa.concluida = True
            return { "message": "Tarefa marcada como concluída." }
    raise HTTPException(status_code=404, detail="Tarefa não cadastrada.")

@app.delete("/remover_tarefa/{nome}")
def remover_tarefa(nome: str, credentials: HTTPBasicCredentials = Depends(validar_usuario)):
    for tarefa in lista_tarefas:
        if tarefa.nome == nome:
            lista_tarefas.remove(tarefa)
            return { "message": "Tarefa removida com sucesso." }
    raise HTTPException(status_code=404, detail="Tarefa não cadastrada.")