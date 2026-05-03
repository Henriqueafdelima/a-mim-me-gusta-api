import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """
    Cria um novo TestClient para cada função de teste.
    Melhora a organização, mas NÃO reinicializa o estado interno da aplicação.
    Dados em listas globais persistem entre testes — por isso os testes
    verificam comportamentos relativos, não contagens absolutas.
    """
    return TestClient(app)


@pytest.fixture
def prato_valido():
    """Payload de prato válido para reutilizar nos testes."""
    return {
        "nome": "Burrito de Fixture",
        "categoria": "burrito",
        "preco": 38.0,
        "disponivel": True,
    }


@pytest.fixture
def bebida_valida():
    """Payload de bebida válida para reutilizar nos testes."""
    return {
        "nome": "Agua de Fixture",
        "tipo": "agua",
        "preco": 8.0,
        "alcoolica": False,
        "volume_ml": 500,
    }
