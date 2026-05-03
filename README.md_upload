---
language: pt
tags:
  - sklearn
  - classification
  - restaurant
  - mlops
  - order-risk
---

# a-mi-me-gusta-predictor

Modelo de classificação binária para previsão de **pedidos problemáticos**
(risco de cancelamento ou reclamação) no restaurante **¡A mi me gusta!**

Desenvolvido como parte do curso CDIA CD2 2026 — Semana 2.

## Uso

```python
from huggingface_hub import hf_hub_download
import joblib

model = joblib.load(hf_hub_download("Richsk/a-mi-me-gusta-predictor", "model.pkl"))

# Exemplo: pedido suspeito (alto valor, madrugada, muitos itens)
features = [[350.0, 2, 10, 3, 22.0]]
prediction = model.predict(features)
probability = model.predict_proba(features)[0][1]
print(f"Problemático: {prediction[0]} | Probabilidade: {probability:.2%}")
```

## Features de entrada

A ordem das features **deve** ser respeitada:

| # | Feature | Tipo | Descrição |
|---|---------|------|-----------|
| 1 | `valor_pedido` | float | Valor total do pedido em reais |
| 2 | `hora_pedido` | int | Hora do dia em que o pedido foi feito (0–23) |
| 3 | `num_itens` | int | Quantidade de pratos no pedido |
| 4 | `historico_cancelamentos` | int | Número de cancelamentos anteriores do cliente |
| 5 | `distancia_entrega` | float | Distância de entrega em km |

## Métricas (test set, 20% dos dados, 2000 amostras)

- **Precision (problemático):** ~0.97
- **Recall (problemático):** ~0.97
- **F1 (problemático):** ~0.97

## Dependências

```
scikit-learn
joblib
numpy
```

## Limitações

Modelo treinado com dados **sintéticos**. As distribuições foram construídas
com intuição de negócio (pedidos de madrugada, distância grande, histórico
de cancelamentos), mas não refletem dados reais de operação.

Não deve ser usado em produção sem retreinamento com dados reais e
validação adequada com métricas de negócio.
