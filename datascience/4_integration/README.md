# Integração – API Python de Previsão de Atrasos

> Este documento descreve **exclusivamente** o que o time Java precisa saber para integrar com a API Python de previsão de atrasos.
> Tudo o que não é garantido pelo código **não é afirmado aqui**.

---

## Visão Geral

A API expõe um endpoint HTTP para prever a probabilidade de atraso de um voo com base em dados básicos do voo.
A integração é feita via **REST (JSON)**.

**Tecnologia da API**

* Python
* FastAPI

**URL (ambiente local)**

```
http://localhost:8000
```

---

## Fluxo de Integração

```
Backend Java  →  HTTP POST (/predict)  →  API Python  →  Resposta JSON
```

Fluxo recomendado:

1. (Opcional) Verificar `/health`
2. Enviar payload para `/predict`
3. Validar resposta
4. Em caso de erro ou timeout, usar fallback no Java

---

## Endpoints Disponíveis

### Health Check

```
GET /health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

Uso recomendado apenas para monitoramento ou diagnóstico.

---

### Previsão de Atraso (endpoint principal)

```
POST /predict
Content-Type: application/json
```

---

## Formato dos Dados

### Payload de Entrada (obrigatório)

```json
{
  "companhia_aerea": "AA",
  "aeroporto_origem": "JFK",
  "aeroporto_destino": "LAX",
  "data_hora_partida": "2024-01-15T14:30:00",
  "distancia_km": 3980.0
}
```

Regras:

* Todos os campos são obrigatórios
* `data_hora_partida` deve estar no formato **ISO 8601** (`YYYY-MM-DDTHH:MM:SS`)
* `distancia_km` deve ser numérico e positivo

---

### Resposta de Sucesso

```json
{
  "atraso": true,
  "probabilidade": 0.78
}
```

Significado:

* `atraso`: indica se o modelo prevê atraso
* `probabilidade`: confiança do modelo (0 a 1)

---

### Respostas de Erro

#### Erro de validação (422)

```json
{
  "detail": "Payload inválido"
}
```

#### Erro interno (500)

```json
{
  "detail": "Erro interno"
}
```

Em caso de erro HTTP ou timeout, o backend Java **deve assumir falha da previsão** e aplicar fallback.

---

## Exemplo de Integração em Java (pseudocódigo)

```java
String url = "http://localhost:8000/predict";
int timeoutMs = 3000;

try {
    ApiResponse response = httpClient.post(url, payload, timeoutMs);

    if (response.isOk()) {
        boolean atraso = response.getBoolean("atraso");
        double prob = response.getDouble("probabilidade");
        return new Prediction(atraso, prob);
    }

} catch (TimeoutException e) {
    // fallback
} catch (Exception e) {
    // fallback
}
```

---

## Timeouts e Confiabilidade

* A API Python **não garante resposta em tempo real**
* O backend Java deve:

  * Definir timeout explícito (ex: 3s)
  * Tratar timeout como erro
  * Ter fallback local

---

## CORS (ambiente local)

Se o backend Java rodar em:

```
http://localhost:8080
```

A API Python deve permitir essa origem. Caso haja erro de CORS, o problema é **configuração da API**, não do Java.

---

## Testes Rápidos

### Health

```bash
curl http://localhost:8000/health
```

### Previsão válida

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

## Problemas Comuns

### Connection refused

* API não está rodando

### Timeout

* API demorou para responder
* Java deve seguir com fallback

### Erro de data

* Verificar formato ISO 8601

---

## Estrutura da Pasta

```
datascience/4_integration/
├── README.md
├── api_client_example.py
├── tests/
│   └── test_integration.py
└── examples/
    └── payload_examples.json
```

---

## Responsabilidades

* **API / Modelo**: Time de Data Science
* **Tratamento de erro, timeout e fallback**: Time Java

---

## Resumo para o Time Java

✔ Um endpoint (`POST /predict`)
✔ Payload JSON simples
✔ Timeout obrigatório no Java
✔ Fallback é responsabilidade do consumidor
✔ Não assumir métricas, SLA ou disponibilidade implícita
