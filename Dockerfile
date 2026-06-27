# ── Estágio 1: builder ────────────────────────────────────────────────────────
# Instala as dependências. Esse estágio carrega compiladores e headers
# necessários para scikit-learn e numpy — mas não vão para a imagem final.
# Exercício 9.1 (estrutura base) + Exercício 12.3 (multi-stage build)
FROM python:3.11-slim AS builder

WORKDIR /app

# Copia apenas o requirements.txt primeiro.
# Motivo: o pip install só reexecuta quando requirements.txt muda.
# Mudanças no código não invalidam o cache dessa camada.
COPY requirements.txt .

# Instala em /install para facilitar a cópia para o estágio final.
# --no-cache-dir reduz o tamanho do estágio builder.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Estágio 2: final ──────────────────────────────────────────────────────────
# Imagem limpa — sem compiladores, sem cache, sem ferramentas de build.
# Exercício 12.3 (multi-stage) + Exercício 12.2 (usuário não-root)
FROM python:3.11-slim

WORKDIR /app

# Copia apenas os pacotes instalados do estágio builder.
# Nenhum resíduo de compilação entra nesta imagem.
COPY --from=builder /install /usr/local

# Copia o código da aplicação depois das dependências.
# Mudanças no código não invalidam o pip install.
COPY . .

# Cria grupo e usuário sem privilégios.
# A API só precisa ler arquivos e servir HTTP — não precisa de root.
# Princípio do menor privilégio: processo recebe apenas as permissões necessárias.
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app

# Troca para o usuário sem privilégios.
# CMD e qualquer instrução seguinte rodam como appuser.
USER appuser

# Documenta que a aplicação usa a porta 8000.
# Não abre a porta — o -p no docker run (ou o Compose) faz isso.
EXPOSE 8000

# --host 0.0.0.0: necessário para que o mapeamento de portas funcione.
# Sem isso, o uvicorn ouve em 127.0.0.1 (loopback interno do contêiner)
# e requisições externas nunca chegam.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
