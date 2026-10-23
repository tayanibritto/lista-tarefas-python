"""
Testes para o endpoint de autenticação.

O objetivo é validar o comportamento de login nos cenários de sucesso e falha, verificando os códigos de status HTTP e as
mensagens retornadas pela API.
"""

import base64
import pytest
import main
from fastapi.testclient import TestClient

# Cliente utilizado na simulação de requisições HTTP para a API durante os testes
client = TestClient(main.app)

@pytest.fixture
def credenciais_validas(monkeypatch):

    """
    Configuração das credenciais para os testes.

    O monkeypatch é utilizado para substituir temporariamente os valores das variáveis de autenticação da aplicação, 
    evitando utilizar as variáveis de ambiente reais durante os testes.
    """
    
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

    """
    Função para gerar o cabeçalho Authorization em HTTP Basic.

    A função recebe usuário e senha, faz a codificação Base64 exigida pelo protocolo HTTP Basic e retorna o cabeçalho que será enviado nas 
    requisições de teste.
    """


    credentials = f"{username}:{password}"

    encoded = base64.b64encode(
        credentials.encode()
    ).decode()

    return {
        "Authorization": f"Basic {encoded}"
    }

def test_login_sucesso(credenciais_validas):

    """
    Teste para validar a autenticação com as credenciais corretas.

    Expectativa: retornar código 200 e mensagem de sucesso.
    """

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

    """
    Teste para validar a autenticação com o login incorreto e a senha correta.

    Expectativa: retornar código 401 e mensagem de falha.
    """

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

    """
    Teste para validar a autenticação com o login correto e a senha incorreta.

    Expectativa: retornar código 401 e mensagem de falha.
    """

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

    """
    Teste para validar a autenticação com o login e a senha incorretos.

    Expectativa: retornar código 401 e mensagem de falha.
    """

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