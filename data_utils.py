"""
data_utils.py — Gerador de dataset sintético para o ¡A mi me gusta!

Domínio: previsão de pedido problemático
(risco de cancelamento ou reclamação de entrega)

Exercício 1.2 / 1.3 do Caderno 2
"""

import numpy as np
import pandas as pd
from typing import Tuple


def gerar_dataset(
    n_samples: int = 1000,
    seed: int = 42,
    proporcao_positivos: float = 0.25,
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Gera dataset sintético de pedidos do restaurante ¡A mi me gusta!

    Parâmetros
    ----------
    n_samples : int
        Número de pedidos a gerar.
    seed : int
        Seed para reprodutibilidade.
    proporcao_positivos : float
        Proporção de pedidos problemáticos. Deve estar entre 0.05 e 0.95.

    Retorna
    -------
    df : pd.DataFrame
        Dataset completo com features e target.
    X : np.ndarray
        Matriz de features.
    y : np.ndarray
        Vetor de targets (0 = normal, 1 = problemático).

    Exemplo
    -------
    >>> df, X, y = gerar_dataset(n_samples=500, seed=0)
    >>> df.shape
    (500, 6)
    """
    if not (0.05 <= proporcao_positivos <= 0.95):
        raise ValueError(
            f"proporcao_positivos deve estar entre 0.05 e 0.95, "
            f"recebido: {proporcao_positivos}"
        )

    rng = np.random.default_rng(seed)

    # Target: pedido problemático ou não
    problematico = rng.choice(
        [0, 1],
        size=n_samples,
        p=[1 - proporcao_positivos, proporcao_positivos],
    )

    # Feature 1: valor do pedido (R$)
    # Pedidos problemáticos tendem a ser de valor mais alto
    valor_pedido = np.where(
        problematico,
        rng.uniform(180, 600, n_samples),
        rng.uniform(25, 180, n_samples),
    ).round(2)

    # Feature 2: hora do pedido (0–23)
    # Madrugada (0–5h) concentra mais problemas de entrega
    hora_pedido = np.where(
        problematico,
        rng.integers(0, 6, n_samples),
        rng.integers(11, 23, n_samples),
    )

    # Feature 3: número de itens no pedido
    # Pedidos grandes têm mais chance de erro/demora
    num_itens = np.where(
        problematico,
        rng.integers(6, 15, n_samples),
        rng.integers(1, 6, n_samples),
    )

    # Feature 4: histórico de cancelamentos do cliente
    # Clientes com mais cancelamentos têm maior risco
    historico_cancelamentos = np.where(
        problematico,
        rng.integers(2, 8, n_samples),
        rng.integers(0, 2, n_samples),
    )

    # Feature 5: distância de entrega (km)
    # Distâncias maiores aumentam risco de atraso e reclamação
    distancia_entrega = np.where(
        problematico,
        rng.uniform(12, 50, n_samples),
        rng.uniform(0.5, 10, n_samples),
    ).round(1)

    df = pd.DataFrame(
        {
            "valor_pedido": valor_pedido,
            "hora_pedido": hora_pedido,
            "num_itens": num_itens,
            "historico_cancelamentos": historico_cancelamentos,
            "distancia_entrega": distancia_entrega,
            "target": problematico,
        }
    )

    X = df.drop(columns=["target"]).values
    y = df["target"].values
    return df, X, y


if __name__ == "__main__":
    df, X, y = gerar_dataset(n_samples=2000, seed=42)
    print(df.head())
    print(f"\nDistribuição: {df['target'].value_counts().to_dict()}")
    print(f"\nMédias por classe:\n{df.groupby('target').mean().round(2)}")
