import pytest


@pytest.mark.smoke
def test_listar_bebidas_retorna_200(client):
    response = client.get("/bebidas")
    assert response.status_code == 200


def test_listar_bebidas_retorna_lista_nao_vazia(client):
    bebidas = client.get("/bebidas").json()
    assert isinstance(bebidas, list)
    assert len(bebidas) > 0


def test_filtro_por_tipo(client):
    response = client.get("/bebidas?tipo=cerveja")
    assert response.status_code == 200
    for bebida in response.json():
        assert bebida["tipo"] == "cerveja"


def test_filtro_alcoolica_false(client):
    response = client.get("/bebidas?alcoolica=false")
    for bebida in response.json():
        assert bebida["alcoolica"] is False


def test_filtro_alcoolica_true(client):
    response = client.get("/bebidas?alcoolica=true")
    for bebida in response.json():
        assert bebida["alcoolica"] is True


@pytest.mark.smoke
def test_buscar_bebida_existente_retorna_200(client):
    response = client.get("/bebidas/1")
    assert response.status_code == 200


def test_buscar_bebida_inexistente_retorna_404(client):
    response = client.get("/bebidas/9999")
    assert response.status_code == 404


@pytest.mark.smoke
def test_criar_bebida_valida(client, bebida_valida):
    response = client.post("/bebidas", json=bebida_valida)
    assert response.status_code in [200, 201]
    dados = response.json()
    assert dados["nome"] == bebida_valida["nome"]
    assert "id" in dados


@pytest.mark.validacao
@pytest.mark.parametrize("tipo_invalido", [
    "vinho", "chopp", "coquetél", "CERVEJA",
])
def test_tipo_invalido_retorna_422(client, tipo_invalido):
    bebida = {
        "nome": "Bebida Teste",
        "tipo": tipo_invalido,
        "preco": 12.0,
        "alcoolica": False,
        "volume_ml": 350,
    }
    response = client.post("/bebidas", json=bebida)
    assert response.status_code == 422


@pytest.mark.validacao
def test_volume_fora_do_limite_retorna_422(client):
    bebida = {
        "nome": "Bebida Gigante",
        "tipo": "suco",
        "preco": 20.0,
        "alcoolica": False,
        "volume_ml": 5000,  # acima do limite de 2000
    }
    response = client.post("/bebidas", json=bebida)
    assert response.status_code == 422
