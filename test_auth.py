import base64
import pytest
import main
from fastapi.testclient import TestClient

client = TestClient(main.app)

@pytest.fixture
def credenciais_validas(monkeypatch):
    usuario = "teste@teste.com"
    senha = "123teste"

    monkeypatch.setattr(
        main,
        "USUARIO",
        "teste@teste.com"
    )

    monkeypatch.setattr(
        main,
        "SENHA",
        "123teste"
    )

    return {
        "usuario": usuario,
        "senha": senha
    }

def basic_auth(username, password):
    credentials = f"{username}:{password}"

    encoded = base64.b64encode(
        credentials.encode()
    ).decode()

    return {
        "Authorization": f"Basic {encoded}"
    }

def test_login_sucesso(credenciais_validas):

    response = client.post(
        "/login",
        headers=basic_auth(
            credenciais_validas["usuario"],
            credenciais_validas["senha"]
        )
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Autenticação realizada com sucesso"
    }

def test_login_falha_usuario_errado(credenciais_validas):

    response = client.post(
        "/login",
        headers=basic_auth(
            "teste_errado@teste.com",
            credenciais_validas["senha"]
        )
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Usuário e/ou senha incorretos"
    }

def test_login_falha_senha_errada(credenciais_validas):

    response = client.post(
        "/login",
        headers=basic_auth(
            credenciais_validas["usuario"],
            "123testeerrado"
        )
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Usuário e/ou senha incorretos"
    }

def test_login_falha_usuario_e_senha_errados(credenciais_validas):
    response = client.post(
        "/login",
        headers=basic_auth(
            "teste_errado@teste.com",
            "123testeerrado"
        )
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Usuário e/ou senha incorretos"
    }