# Lista de Tarefas

API REST desenvolvida com FastAPI para gerenciamento de tarefas.

## Funcionalidades

- Adicionar, listar e remover tarefas;
- Marcar tarefa como concluída;
- Autenticação HTTP Basic;
- Persistência em SQLite;
- Containerização com Docker e Docker Compose;
- Gerenciamento de dependências com Poetry

## Tecnologias Utilizadas

- Python 3.14;
- FastAPI;
- SQLAlchemy;
- SQLite;
- Poetry;
- Docker
- Docker Compose

## Passos para clonar e rodar

```bash
git clone https://github.com/tayanibritto/lista-tarefas-python.git
```

```bash
cd lista-tarefas-python
```

Criar o arquivo .env na raiz do projeto:

```env
USUARIO=seu_usuario
SENHA=sua_senha
DATABASE_URL=sqlite:///./tarefas.db
```

### Usuários de Docker Compose:

```bash
docker-compose up --build -d
```

ou

```bash
docker compose up --build -d
```

Acessar a documentação Swagger para testar a aplicação:

```text
http://localhost:8000/docs
```

Para parar a aplicação:

```bash
docker-compose down
```

ou

```bash
docker compose down
```

### Usuários de Podman Compose:

```bash
podman-compose up --build -d
```

ou

```bash
podman compose up --build -d
```

Acessar a documentação Swagger para testar a aplicação:

```text
http://localhost:8000/docs
```

Para parar a aplicação:

```bash
podman-compose down
```

ou

```bash
podman compose down
```

## Endpoints da aplicação

### Criar tarefa

```http
POST /adicionar_tarefa
```

### Listar todas as tarefas cadastradas

```http
GET /tarefas
```

### Marcar tarefa como concluída

```http
PUT /marcar_concluida/{nome}
```

### Excluir tarefa

```http
DELETE /remover_tarefa/{nome}
```

## Estrutura do Projeto

```text
.
├── Dockerfile
├── docker-compose.yml
├── main.py
├── pyproject.toml
├── poetry.lock
├── tarefas.db
└── README.md
```

# Observação

Este projeto foi testado utilizando o Podman Compose.