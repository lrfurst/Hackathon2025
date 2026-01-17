# API_SPECS – API Python de Previsão de Atrasos

> **Documento técnico e contratual.**
> Esta especificação descreve **apenas o comportamento garantido pela API**.
> Métricas de negócio, SLA, disponibilidade, cache, rate limit e segurança **não são assumidos** a menos que estejam implementados no código.

---

## Visão Geral

A API fornece uma previsão simples de atraso de voo a partir de dados básicos do voo.
O consumo é feito via **HTTP + JSON**.

* Tecnologia: Python + FastAPI
* Estilo: REST
* Formato: JSON
* Estado: síncrono

**Base URL (local)**

```
http://localhost:8000
```

---

## Fluxo Básico

```
Cliente → POST /predict → API → Resposta JSON
```

O cliente é responsável por:

* Definir timeout
* Tratar erros HTTP
* Implementar fallback

---

## Endpoints

### GET /health

Endpoint simples para verificar se a API está respondendo.

**Resposta esperada:**

```json
{
  "status": "ok"
}
```

Não há garantia de verificação de dependências internas.

---

### POST /predict

Endpoint principal de previsão.

**Headers obrigatórios:**

```
Content-Type: application/json
Accept: application/json
```

---

## Payload de Entrada

Todos os campos são obrigatórios.

```json
{
  "companhia_aerea": "AA",
  "aeroporto_origem": "JFK",
  "aeroporto_destino": "LAX",
  "data_hora_partida": "2024-01-15T14:30:00",
  "distancia_km": 3980.0
}
```

### Regras de Validação

* `companhia_aerea`: string, 2–3 letras maiúsculas
* `aeroporto_origem`: string, 3 letras maiúsculas
* `aeroporto_destino`: string, 3 letras maiúsculas
* `data_hora_partida`: ISO 8601 (`YYYY-MM-DDTHH:MM:SS`)
* `distancia_km`: número positivo

Qualquer violação resulta em erro **422**.

---

## Resposta de Sucesso

```json
{
  "atraso": true,
  "probabilidade": 0.78
}
```

### Significado

* `atraso`: previsão binária do modelo
* `probabilidade`: confiança do modelo (0–1)

Não há garantias estatísticas associadas a essa probabilidade.

---

## Respostas de Erro

### Erro de validação – 422

```json
{
  "detail": [
    {
      "loc": ["body", "data_hora_partida"],
      "msg": "Invalid datetime format",
      "type": "value_error"
    }
  ]
}
```

### Erro interno – 500

```json
{
  "detail": "Internal server error"
}
```

### Timeout

Se a API não responder dentro do tempo configurado no cliente:

* Não há resposta HTTP
* O cliente deve tratar como falha

---

## Códigos HTTP Utilizados

| Código | Significado       |
| ------ | ----------------- |
| 200    | Sucesso           |
| 400    | JSON inválido     |
| 422    | Erro de validação |
| 500    | Erro interno      |

Outros códigos **não são garantidos**.

---

## Autenticação

Atualmente **não há autenticação obrigatória**.

Se headers de autenticação forem enviados, eles são ignorados.

---

## Rate Limiting

Não há rate limiting garantido pela API.

O cliente deve assumir:

* Possibilidade de throttling futuro
* Falhas por excesso de requisições

---

## Versionamento

Atualmente **não há versionamento por URL ou header**.

Qualquer mudança incompatível:

* Será documentada
* Pode exigir ajuste do cliente

---

## Exemplos

### Requisição válida

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "companhia_aerea": "AA",
    "aeroporto_origem": "JFK",
    "aeroporto_destino": "LAX",
    "data_hora_partida": "2024-01-15T14:30:00",
    "distancia_km": 3980.0
  }'
```

---

### Requisição inválida

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"companhia_aerea": "AA"}'
```

Resposta esperada: **422**

---

## Considerações para o Cliente Java

O backend Java deve obrigatoriamente:

* Definir timeout explícito (ex: 3s)
* Tratar timeout como falha
* Não confiar em métricas de negócio
* Não assumir SLA ou disponibilidade
* Implementar fallback

---

## O que esta API NÃO garante

* SLA ou disponibilidade
* Precisão estatística do modelo
* Consistência temporal
* Cache
* Rate limit estável
* Identificadores de requisição
* Métricas de negócio

---

## Regra Final

> **Se a documentação divergir do comportamento da API, o código é a fonte da verdade.**

Este documento existe para reduzir ambiguidades — não para criar promessas implícitas.
