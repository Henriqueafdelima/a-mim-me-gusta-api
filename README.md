# ¡A mi me gusta! 🌮

API REST do restaurante mexicano **¡A mi me gusta!**, construída com **FastAPI** como exercício prático do curso CDIA CD2 2026.

## Sobre o restaurante

| Campo | Info |
|---|---|
| Nome | ¡A mi me gusta! |
| Chef | Seu Burrito |
| Cidade | São Paulo |
| Especialidade | Burritos e pratos mexicanos |

---

## Instalação

```bash
pip install fastapi uvicorn pydantic-settings
```

## Como rodar

```bash
uvicorn main:app --reload
```

Acesse a documentação interativa em: `http://localhost:8000/docs`

---

## Estrutura do projeto

```
a_mi_me_gusta/
├── main.py           # aplicação FastAPI + routers + exception handlers
├── config.py         # configurações com BaseSettings
├── .env              # variáveis de ambiente
├── routers/
│   ├── __init__.py
│   ├── pratos.py     # GET, POST, PUT de pratos
│   ├── bebidas.py    # GET, POST de bebidas
│   ├── pedidos.py    # POST de pedidos
│   └── reservas.py   # CRUD completo de reservas antecipadas
└── models/
    ├── __init__.py
    ├── prato.py      # PratoInput, PratoOutput
    ├── bebida.py     # BebidaInput, BebidaOutput
    ├── pedido.py     # PedidoInput, PedidoOutput
    └── reserva.py    # ReservaInput, ReservaOutput
```

---

## Mapa de rotas

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Informações do restaurante |
| GET | `/pratos` | Lista pratos (filtros: `categoria`, `preco_maximo`, `apenas_disponiveis`) |
| GET | `/pratos/{id}` | Detalha um prato (query: `formato=resumido\|completo`) |
| POST | `/pratos` | Cadastra um prato |
| PUT | `/pratos/{id}/disponibilidade` | Altera disponibilidade de um prato |
| GET | `/bebidas` | Lista bebidas (filtros: `tipo`, `alcoolica`) |
| GET | `/bebidas/{id}` | Detalha uma bebida |
| POST | `/bebidas` | Cadastra uma bebida |
| POST | `/pedidos` | Cria um pedido |
| GET | `/reservas` | Lista reservas (filtros: `data`, `apenas_ativas`) |
| GET | `/reservas/{id}` | Detalha uma reserva |
| GET | `/reservas/mesa/{numero}` | Reservas de uma mesa específica |
| POST | `/reservas` | Cria uma reserva antecipada |
| DELETE | `/reservas/{id}` | Cancela uma reserva |

---

## Exercício 2.1 — Diagnóstico da API sem validações

| Caso | Status retornado | Status correto | Problema |
|---|---|---|---|
| `GET /pratos/99` | 200 | 404 | A API finge que a requisição funcionou |
| `POST /pratos` com `nome=""` e `preco=-10` | 200 | 422 | Dados inválidos eram aceitos sem validação |
| `POST /pratos` com campos obrigatórios faltando | 422 | 422 | ✅ FastAPI/Pydantic já tratava corretamente |
| `GET /pratos?preco_maximo=abc` | 422 | 422 | ✅ FastAPI valida tipos de query params automaticamente |

**Conclusão:** o FastAPI já valida estrutura e tipos. O que faltava era validar regras de negócio e retornar 404 corretamente com `HTTPException`.

---

## Exercício 3.1 — Problemas do main.py monolítico

**1. Onde colocar "promoções"?**
Não há um lugar óbvio. Em um arquivo organizado por domínio, promoções teriam seu próprio arquivo `routers/promocoes.py`.

**2. Dois devs trabalhando ao mesmo tempo (pratos e pedidos):**
Ambos editariam o mesmo `main.py`, gerando conflitos de merge no Git — mesmo que as mudanças fossem em partes distintas do arquivo.

**3. Como encontrar rotas de reservas rapidamente?**
Seria necessário buscar por "reserva" no arquivo e navegar manualmente. Com routers separados, basta abrir `routers/reservas.py`.

---

## Categorias válidas

**Pratos:** `burrito` · `taco` · `quesadilla` · `sobremesa` · `entrada` · `salada`

**Bebidas:** `cerveja` · `agua` · `refrigerante` · `suco` · `destilado`
