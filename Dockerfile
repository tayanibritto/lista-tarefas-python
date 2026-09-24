FROM python:3.14-slim

WORKDIR /app

RUN pip install poetry==2.4.1

COPY pyproject.toml poetry.lock ./

# Desabilita ambiente virtual interno - não é necessário venv, o próprio container já é um ambiente isolado.
RUN poetry config virtualenvs.create false

# Instala FastAPI, SQLAlchemy, Uvicorn, etc.
RUN poetry install --no-root

# Copia a aplicação para dentro do container
COPY . .

# Expõe a porta
EXPOSE 8000

# Seria o mesmo que executar poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]