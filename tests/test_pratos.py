import pytest


# ─── GET /pratos ──────────────────────────────────────────────────────────────

@pytest.mark.smoke
def test_listar_pratos_retorna_200(client):
    response = client.get("/pratos")
    assert response.status_code == 200


@pytest.mark.smoke
def test_listar_pratos_retorna_lista_nao_vazia(client):
    response = client.get("/pratos")
    pratos = response.json()
    assert isinstance(pratos, list)
    assert len(pratos) > 0


@pytest.mark.smoke
def test_listar_pratos_tem_estrutura_correta(client):
    response = client.get("/pratos")
    pratos = response.json()
    assert "id" in pratos[0]
    assert "nome" in pratos[0]
    assert "preco" in pratos[0]
    assert "categoria" in pratos[0]


def test_filtro_por_categoria_retorna_apenas_categoria_correta(client):
    response = client.get("/pratos?categoria=burrito")
    assert response.status_code == 200
    for prato in response.json():
        assert prato["categoria"] == "burrito"


def test_filtro_apenas_disponiveis(client):
    response = client.get("/pratos?apenas_disponiveis=true")
    assert response.status_code == 200
    for prato in response.json():
        assert prato["disponivel"] is True


def test_filtro_preco_maximo(client):
    response = client.get("/pratos?preco_maximo=30")
    assert response.status_code == 200
    for prato in response.json():
        assert prato["preco"] <= 30


# ─── GET /pratos/{id} ─────────────────────────────────────────────────────────

@pytest.mark.smoke
def test_buscar_prato_existente_retorna_200(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200


def test_buscar_prato_existente_retorna_campos_esperados(client):
    response = client.get("/pratos/1")
    prato = response.json()
    assert "id" in prato
    assert "nome" in prato
    assert "preco" in prato
    assert "disponivel" in prato


def test_buscar_prato_inexistente_retorna_404(client):
    response = client.get("/pratos/9999")
    assert response.status_code == 404


def test_formato_resumido_retorna_apenas_nome_e_preco(client):
    response = client.get("/pratos/1?formato=resumido")
    assert response.status_code == 200
    dados = response.json()
    assert "nome" in dados
    assert "preco" in dados


# ─── POST /pratos ─────────────────────────────────────────────────────────────

@pytest.mark.smoke
def test_criar_prato_valido(client, prato_valido):
    response = client.post("/pratos", json=prato_valido)
    assert response.status_code in [200, 201]
    dados = response.json()
    assert dados["nome"] == prato_valido["nome"]
    assert "id" in dados


def test_prato_criado_aparece_na_listagem(client):
    nome_unico = "Taco Fixture Teste XYZ-7742"
    client.post("/pratos", json={
        "nome": nome_unico,
        "categoria": "taco",
        "preco": 28.0,
    })
    response = client.get("/pratos")
    nomes = [p["nome"] for p in response.json()]
    assert nome_unico in nomes


def test_novo_prato_recebe_id_valido(client, prato_valido):
    response = client.post("/pratos", json=prato_valido)
    dados = response.json()
    assert isinstance(dados["id"], int)
    assert dados["id"] > 0


# ─── Validações (Exercício 4.3 — parametrize) ─────────────────────────────────

@pytest.mark.validacao
@pytest.mark.parametrize("preco_invalido", [-1.0, -0.01, 0.0, -100.0])
def test_preco_invalido_retorna_422(client, preco_invalido):
    prato = {"nome": "Prato Teste", "categoria": "burrito", "preco": preco_invalido}
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
@pytest.mark.parametrize("categoria_invalida", [
    "esoterico", "fastfood", "italiana", "BURRITO", "taco extra",
])
def test_categoria_invalida_retorna_422(client, categoria_invalida):
    prato = {"nome": "Prato Teste", "categoria": categoria_invalida, "preco": 30.0}
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
def test_nome_muito_curto_retorna_422(client):
    prato = {"nome": "AB", "categoria": "burrito", "preco": 30.0}
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
def test_preco_promocional_maior_que_preco_retorna_422(client):
    prato = {
        "nome": "Burrito Caro",
        "categoria": "burrito",
        "preco": 30.0,
        "preco_promocional": 40.0,
    }
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
def test_desconto_acima_50_retorna_422(client):
    prato = {
        "nome": "Burrito Desconto",
        "categoria": "burrito",
        "preco": 40.0,
        "preco_promocional": 15.0,  # desconto de 62.5%
    }
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


# ─── IDs inexistentes (parametrize) ──────────────────────────────────────────

@pytest.mark.parametrize("id_inexistente", [9999, 123456, 99999])
def test_prato_inexistente_retorna_404(client, id_inexistente):
    response = client.get(f"/pratos/{id_inexistente}")
    assert response.status_code == 404


# ─── Filtros por categoria válida ─────────────────────────────────────────────

@pytest.mark.parametrize("categoria_valida", [
    "burrito", "taco", "quesadilla", "sobremesa", "entrada", "salada",
])
def test_filtro_por_categoria_valida(client, categoria_valida):
    response = client.get(f"/pratos?categoria={categoria_valida}")
    assert response.status_code == 200
    for prato in response.json():
        assert prato["categoria"] == categoria_valida


# ─── PUT disponibilidade ──────────────────────────────────────────────────────

def test_alterar_disponibilidade(client):
    client.put("/pratos/1/disponibilidade", json={"disponivel": False})
    response = client.get("/pratos/1")
    assert response.json()["disponivel"] is False
    # restaura
    client.put("/pratos/1/disponibilidade", json={"disponivel": True})
