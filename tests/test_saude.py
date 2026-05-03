import pytest


def test_pytest_funcionando():
    """Confirma que o pytest encontrou e executou este arquivo."""
    assert 1 + 1 == 2


@pytest.mark.smoke
def test_raiz_retorna_200(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.smoke
def test_raiz_retorna_nome_restaurante(client):
    response = client.get("/")
    dados = response.json()
    assert "¡A mi me gusta!" in dados["restaurante"]


@pytest.mark.smoke
def test_raiz_retorna_campos_esperados(client):
    response = client.get("/")
    dados = response.json()
    assert "restaurante" in dados
    assert "chef" in dados
    assert "especialidade" in dados
