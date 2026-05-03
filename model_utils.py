"""
model_utils.py — Carregamento do modelo do Hugging Face Hub

Exercício 4.1 do Caderno 2
"""

import os
import joblib
from huggingface_hub import hf_hub_download, login


def load_model(
    repo_id: str,
    filename: str = "model.pkl",
    force_download: bool = False,
):
    """
    Carrega o modelo de pedidos problemáticos do Hugging Face Hub.

    Usa cache automático: primeira chamada baixa, chamadas seguintes
    reutilizam a cópia local. Use force_download=True para forçar
    novo download (ex: após publicar nova versão do modelo).

    Parâmetros
    ----------
    repo_id : str
        ID do repositório no Hub (ex: "Richsk/a-mi-me-gusta-predictor").
    filename : str
        Nome do arquivo do modelo no repositório.
    force_download : bool
        Se True, ignora o cache e baixa novamente.

    Retorna
    -------
    model : sklearn estimator
        Modelo carregado e pronto para predict / predict_proba.
    """
    token = os.environ.get("HF_TOKEN")
    if token:
        login(token=token, add_to_git_credential=False)

    local_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        force_download=force_download,
    )
    return joblib.load(local_path)
