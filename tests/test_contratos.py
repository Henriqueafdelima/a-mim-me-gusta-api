"""
tests/test_contratos.py — Testes de contrato da API ¡A mi me gusta!

Verificam que a API respeita o schema prometido em cada rota.
Se a API parar de retornar um campo, o teste detecta imediatamente.

Exercício 4.5 do Caderno 4
"""


def test_contrato_get_prato(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()

    campos_obrigatorios = {"id", "nome", "categoria", "preco", "disponivel"}
    assert campos_obrigatorios.issubset(prato.keys())

    assert isinstance(prato["id"], int)
    assert isinstance(prato["nome"], str)
    assert isinstance(prato["categoria"], str)
    assert isinstance(prato["preco"], (int, float))
    assert isinstance(prato["disponivel"], bool)
    assert prato["preco"] > 0
    assert len(prato["nome"]) >= 3


def test_contrato_post_prato(client):
    novo = {"nome": "Prato Contrato Teste", "categoria": "taco", "preco": 30.0}
    response = client.post("/pratos", json=novo)
    assert response.status_code in [200, 201]
    prato = response.json()

    assert "id" in prato
    assert isinstance(prato["id"], int)
    assert prato["nome"] == "Prato Contrato Teste"

    if "criado_em" in prato:
        assert isinstance(prato["criado_em"], str)
        assert len(prato["criado_em"]) > 0


def test_contrato_erro_404(client):
    response = client.get("/pratos/9999")
    assert response.status_code == 404
    corpo = response.json()

    # handler customizado usa 'erro'; padrão FastAPI usa 'detail'
    assert "detail" in corpo or "erro" in corpo
    mensagem = corpo.get("detail") or corpo.get("erro")
    assert isinstance(mensagem, str)
    assert len(mensagem) > 0


def test_contrato_erro_422(client):
    response = client.post("/pratos", json={"nome": "X", "preco": -1})
    assert response.status_code == 422
    corpo = response.json()

    erros = corpo.get("detail") or corpo.get("detalhes")
    assert erros is not None
    assert isinstance(erros, list)
    assert len(erros) > 0


def test_contrato_get_bebida(client):
    response = client.get("/bebidas/1")
    assert response.status_code == 200
    bebida = response.json()

    campos = {"id", "nome", "tipo", "preco", "alcoolica", "volume_ml"}
    assert campos.issubset(bebida.keys())
    assert bebida["preco"] > 0
    assert isinstance(bebida["alcoolica"], bool)
    assert bebida["volume_ml"] >= 50
