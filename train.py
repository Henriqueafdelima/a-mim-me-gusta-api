"""
train.py — Treinamento e serialização do modelo ¡A mi me gusta!

Exercícios 2.1 e 2.2 do Caderno 2

Execute com:
    python train.py
"""

import joblib
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from data_utils import gerar_dataset

# ─── 1. Gerar dados ──────────────────────────────────────────────────────────
df, X, y = gerar_dataset(n_samples=2000, seed=42)
print(f"Dataset gerado: {df.shape[0]} amostras, {X.shape[1]} features")
print(f"Proporção problemático: {y.mean():.1%}\n")

# ─── 2. Split treino / teste ──────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ─── 3. Treinar modelo ────────────────────────────────────────────────────────
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=["normal", "problemático"]))

# ─── 4. Validar serialização (Exercício 2.2) ──────────────────────────────────
joblib.dump(model, "model.pkl")
tamanho_kb = os.path.getsize("model.pkl") / 1024
print(f"Modelo salvo: model.pkl ({tamanho_kb:.1f} KB)")

model_carregado = joblib.load("model.pkl")
amostra = X_test[:5]
pred_original = model.predict(amostra)
pred_carregado = model_carregado.predict(amostra)

assert np.array_equal(pred_original, pred_carregado), "Predições divergem!"
print("✅ Artefato validado — predições idênticas")
print(f"Predições de exemplo: {pred_original}")
