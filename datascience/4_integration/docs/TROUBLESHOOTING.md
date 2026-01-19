
## ✅ **VERSÃO REVISADA — TROUBLESHOOTING.md**

````markdown
# TROUBLESHOOTING.md

Guia rápido para diagnosticar problemas na integração Java → API Python.
Escopo restrito ao que o time de backend Java precisa verificar.

---

## 1. API Python não responde

**Sintomas**
- `Connection refused`
- `Connection timeout`

**Verificação**
```bash
# API responde?
curl http://localhost:8000/health

# Processo ativo?
ps aux | grep uvicorn

# Porta aberta?
netstat -tulpn | grep 8000
````

**Ação**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Se `/health` não responde, **não é erro de integração**.

---

## 2. Erro de CORS

**Sintoma**

* Erro de CORS no browser ou proxy intermediário

**Teste**

```bash
curl -X OPTIONS http://localhost:8000/predict \
  -H "Origin: http://localhost:8080" \
  -I | grep -i access-control
```

**Nota**

* CORS é responsabilidade da API Python
* Não há workaround seguro no Java backend

---

## 3. Timeout (> 3 segundos)

**Sintoma**

```
Read timed out
```

**Verificação**

```bash
time curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"companhia_aerea":"AA","aeroporto_origem":"JFK","aeroporto_destino":"LAX","data_hora_partida":"2024-01-15T14:30:00","distancia_km":3980}'
```

**Regras**

* Timeout padrão Java: **3000ms**
* Não aumentar permanentemente
* Use fallback se exceder

**Ação temporária (debug apenas)**

```java
factory.setReadTimeout(Duration.ofSeconds(4));
```

---

## 4. Erro de Validação (422)

**Causas comuns**

* Data fora do padrão `YYYY-MM-DDTHH:MM:SS`
* Strings em minúsculo onde o contrato exige maiúsculas
* Campos obrigatórios ausentes
* Valores inválidos (ex: distância ≤ 0)

**Payload válido**

```json
{
  "companhia_aerea": "AA",
  "aeroporto_origem": "JFK",
  "aeroporto_destino": "LAX",
  "data_hora_partida": "2024-01-15T14:30:00",
  "distancia_km": 3980.0
}
```

**Regra**

* 422 **não é retry**
* Corrija o payload no Java

---

## 5. Rate limit (429)

**Sintoma**

```
429 Too Many Requests
```

**Ação**

* Retry com exponential backoff
* Preferir cache no cliente
* Não fazer retry agressivo

---

## 6. Erro 5xx (API Python)

**Sintomas**

* `500 Internal Server Error`
* `503 Service Unavailable`

**Ações**

1. Registrar erro com payload + latência
2. Ativar retry controlado
3. Circuit breaker deve abrir
4. Usar fallback

Se 5xx for consistente → problema é **API Python**, não integração.

---

## Checklist rápido (antes de escalar)

### Básico

* [ ] `/health` responde
* [ ] Endpoint correto
* [ ] Payload válido
* [ ] Timeout = 3s

### Resiliência

* [ ] Circuit breaker ativo
* [ ] Retry limitado
* [ ] Fallback funcionando

---

## Logs que importam

### Java

Procure por:

* Tempo da chamada
* Status HTTP
* Uso de fallback

Exemplo esperado:

```
Erro API Python flight=JFK-LAX status=503 duration=3120ms
```

### Python

Procure por:

* Erros no `/predict`
* Requests > 2000ms

---

## Ações manuais seguras

### Forçar fallback

```java
circuitBreaker.transitionToOpenState();
```

### Nunca faça

* Aumentar timeout indefinidamente
* Retry infinito
* Ignorar 422

---

## Mapa rápido de erros

| Erro               | Significado         | Ação Java      |
| ------------------ | ------------------- | -------------- |
| Connection refused | API fora do ar      | Não retry      |
| Timeout            | API lenta           | Fallback       |
| 422                | Payload inválido    | Corrigir dados |
| 429                | Excesso de chamadas | Backoff        |
| 5xx                | Erro interno        | Retry + CB     |

---

Este documento é intencionalmente curto.
Se não resolver com isso, o problema **não está no Java**.

```