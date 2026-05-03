"""
tests/test_modelo.py — Testes de integração com o modelo do Hugging Face Hub

Exercícios 5.2, 5.3 e 5.5 do Caderno 5

Estes testes requerem HF_TOKEN e acesso à internet.
São marcados com @pytest.mark.integracao e só rodam no pipeline
em pushes para o main — nunca em pull requests.

Para rodar localmente:
    export HF_TOKEN=hf_seu_token_aqui
    pytest tests/test_modelo.py -v -m integracao
"""

import pytest
import numpy as np


REPO_ID = "Richsk/a-mi-me-gusta-predictor"
N_FEATURES = 5

# Payload válido para o endpoint /ml/predict
PAYLOAD_VALIDO = {
    "valor_pedido": 65.0,
    "hora_pedido": 13,
    "num_itens": 2,
    "historico_cancelamentos": 0,
    "distancia_entrega": 2.5,
}


# ─── Fixture do modelo (scope=module: carrega UMA vez para todos os testes) ───

@pytest.fixture(scope="module")
def modelo():
    """
    Carrega o modelo uma única vez para todos os testes deste arquivo.
    scope='module' evita múltiplos downloads do Hub no mesmo run.
    """
    from model_utils import load_model
    return load_model(REPO_ID)


@pytest.fixture
def amostra_valida():
    """Amostra com valores típicos de pedido normal."""
    return np.array([[65.0, 13, 2, 0, 2.5]])


# ─── Exercício 5.2 — Testes do artefato ──────────────────────────────────────

@pytest.mark.integracao
def test_modelo_carregado_nao_e_none(modelo):
    assert modelo is not None


@pytest.mark.integracao
def test_modelo_tem_metodo_predict(modelo):
    assert hasattr(modelo, "predict")
    assert callable(modelo.predict)


@pytest.mark.integracao
def test_modelo_tem_metodo_predict_proba(modelo):
    assert hasattr(modelo, "predict_proba")
    assert callable(modelo.predict_proba)


@pytest.mark.integracao
def test_predict_retorna_array_formato_correto(modelo, amostra_valida):
    resultado = modelo.predict(amostra_valida)
    assert resultado.shape == (1,)
    assert resultado[0] in [0, 1]


@pytest.mark.integracao
def test_predict_proba_retorna_probabilidades_validas(modelo, amostra_valida):
    probas = modelo.predict_proba(amostra_valida)
    assert probas.shape == (1, 2)
    assert abs(probas[0].sum() - 1.0) < 1e-6
    assert all(0 <= p <= 1 for p in probas[0])


# ─── Exercício 5.3 — Testes do endpoint /ml/predict ──────────────────────────

@pytest.mark.integracao
def test_predict_retorna_200(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.status_code == 200


@pytest.mark.integracao
def test_predict_retorna_campos_esperados(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    dados = response.json()
    assert "prediction" in dados
    assert "probability" in dados
    assert "label" in dados
    assert "model_version" in dados


@pytest.mark.integracao
def test_predict_prediction_e_binario(client):
    prediction = client.post("/ml/predict", json=PAYLOAD_VALIDO).json()["prediction"]
    assert prediction in [0, 1]


@pytest.mark.integracao
def test_predict_probability_entre_zero_e_um(client):
    probability = client.post("/ml/predict", json=PAYLOAD_VALIDO).json()["probability"]
    assert isinstance(probability, float)
    assert 0.0 <= probability <= 1.0


@pytest.mark.integracao
def test_predict_label_e_string_nao_vazia(client):
    label = client.post("/ml/predict", json=PAYLOAD_VALIDO).json()["label"]
    assert isinstance(label, str)
    assert len(label) > 0


@pytest.mark.integracao
def test_predict_sem_campo_obrigatorio_retorna_422(client):
    response = client.post("/ml/predict", json={"valor_pedido": 65.0})
    assert response.status_code == 422


@pytest.mark.integracao
@pytest.mark.parametrize("campo,valor_invalido", [
    ("hora_pedido", 25),       # hora fora de 0-23
    ("hora_pedido", -1),       # hora negativa
    ("num_itens", 0),          # quantidade inválida
    ("valor_pedido", -50.0),   # valor negativo
])
def test_predict_campo_invalido_retorna_422(client, campo, valor_invalido):
    payload = {**PAYLOAD_VALIDO, campo: valor_invalido}
    response = client.post("/ml/predict", json=payload)
    assert response.status_code == 422


# ─── Exercício 5.5 — Testes de comportamento do modelo ───────────────────────

@pytest.mark.integracao
def test_modelo_distingue_casos_extremos(client):
    """
    Teste de sanidade: pedido típico de almoço vs pedido suspeito de madrugada.
    Construídos com base na lógica do gerar_dataset:
    - pedidos problemáticos: valor alto, madrugada, muitos itens, histórico ruim, distância grande
    - pedidos normais: valor médio, horário comercial, poucos itens, sem histórico, perto
    """
    caso_normal = {
        "valor_pedido": 55.0,
        "hora_pedido": 12,
        "num_itens": 2,
        "historico_cancelamentos": 0,
        "distancia_entrega": 1.5,
    }
    caso_suspeito = {
        "valor_pedido": 480.0,
        "hora_pedido": 2,
        "num_itens": 12,
        "historico_cancelamentos": 5,
        "distancia_entrega": 38.0,
    }

    resp_normal = client.post("/ml/predict", json=caso_normal)
    resp_suspeito = client.post("/ml/predict", json=caso_suspeito)

    assert resp_normal.status_code == 200
    assert resp_suspeito.status_code == 200

    prob_normal = resp_normal.json()["probability"]
    prob_suspeito = resp_suspeito.json()["probability"]

    assert prob_suspeito > prob_normal, (
        f"Esperado: prob_suspeito ({prob_suspeito:.3f}) > "
        f"prob_normal ({prob_normal:.3f})\n"
        "Se falhou após retreinamento, investigue antes de ajustar o teste."
    )


@pytest.mark.integracao
def test_modelo_e_deterministico(client):
    """O mesmo input deve sempre gerar o mesmo resultado."""
    resp_1 = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    resp_2 = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert resp_1.json()["prediction"] == resp_2.json()["prediction"]
    assert resp_1.json()["probability"] == resp_2.json()["probability"]
