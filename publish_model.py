"""
publish_model.py — Publica o modelo no Hugging Face Hub

Exercício 3.3 do Caderno 2

Antes de rodar:
    export HF_TOKEN=hf_seu_token_aqui   # Linux/macOS
    set HF_TOKEN=hf_seu_token_aqui      # Windows CMD

Execute com:
    python publish_model.py
"""

import os
import joblib
import numpy
import sklearn
from huggingface_hub import HfApi, login

# ─── Autenticação ─────────────────────────────────────────────────────────────
token = os.environ.get("HF_TOKEN")
if not token:
    raise EnvironmentError(
        "HF_TOKEN não encontrado. Configure a variável de ambiente antes de rodar."
    )

login(token=token, add_to_git_credential=False)
api = HfApi()
username = api.whoami()["name"]
print(f"✅ Autenticado como: {username}")

# ─── Criar repositório ────────────────────────────────────────────────────────
repo_id = f"{username}/a-mi-me-gusta-predictor"
repo_url = api.create_repo(
    repo_id=repo_id,
    repo_type="model",
    exist_ok=True,
    private=False,
)
print(f"✅ Repositório: {repo_url}")

# ─── Criar requirements.txt do artefato ──────────────────────────────────────
model_requirements = (
    f"scikit-learn=={sklearn.__version__}\n"
    f"joblib=={joblib.__version__}\n"
    f"numpy=={numpy.__version__}\n"
)
with open("model_requirements.txt", "w") as f:
    f.write(model_requirements)

# Renomear model card para README.md temporariamente para upload
import shutil
shutil.copy("HF_MODEL_CARD.md", "README.md_upload")

# ─── Publicar arquivos ────────────────────────────────────────────────────────
arquivos = [
    ("model.pkl", "model.pkl"),
    ("HF_MODEL_CARD.md", "README.md"),
    ("model_requirements.txt", "requirements.txt"),
]

for local, remote in arquivos:
    api.upload_file(
        path_or_fileobj=local,
        path_in_repo=remote,
        repo_id=repo_id,
        repo_type="model",
        commit_message=f"chore: add {remote}",
    )
    print(f"✅ {remote} publicado")

os.remove("model_requirements.txt")

print(f"\n🔗 https://huggingface.co/{repo_id}")
