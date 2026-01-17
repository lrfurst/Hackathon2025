# Guia de Integração – API Python de Previsão de Atrasos

> Guia prático para o time Java integrar com a API Python. Foco no essencial para implementação rápida e confiável.

---

## Checklist de Integração (5 minutos)

### ✅ Pré-requisitos
- [ ] API Python rodando em `http://localhost:8000`
- [ ] Endpoint `/health` respondendo
- [ ] Timeout Java configurado para 3000ms
- [ ] CORS configurado se necessário

### ✅ Implementação Básica
- [ ] Cliente HTTP com timeout
- [ ] Payload JSON correto
- [ ] Tratamento de resposta 200
- [ ] Tratamento de erros 4xx/5xx

### ✅ Resiliência
- [ ] Retry para 5xx
- [ ] Circuit breaker
- [ ] Fallback implementado
- [ ] Logs de erro

---

## Fluxo de Integração

```
1. Verificar /health (opcional)
2. Preparar payload JSON
3. POST /predict com timeout 3s
4. Processar resposta ou fallback
```

### Código Java Mínimo

```java
// 1. Configurar cliente
RestTemplate restTemplate = new RestTemplate();
SimpleClientHttpRequestFactory factory = (SimpleClientHttpRequestFactory) restTemplate.getRequestFactory();
factory.setConnectTimeout(3000);
factory.setReadTimeout(3000);

// 2. Preparar payload
FlightData flight = new FlightData();
flight.companhia_aerea = "AA";
flight.aeroporto_origem = "JFK";
flight.aeroporto_destino = "LAX";
flight.data_hora_partida = "2024-01-15T14:30:00";
flight.distancia_km = 3980.0;

// 3. Headers
HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.APPLICATION_JSON);

// 4. Fazer chamada
try {
    ResponseEntity<PredictionResponse> response = restTemplate.exchange(
        "http://localhost:8000/predict",
        HttpMethod.POST,
        new HttpEntity<>(flight, headers),
        PredictionResponse.class
    );

    if (response.getStatusCode() == HttpStatus.OK) {
        boolean atraso = response.getBody().atraso;
        double probabilidade = response.getBody().probabilidade;
        // Usar resultado
    }
} catch (Exception e) {
    // Fallback
}
```

---

## Mapeamento de Erros

| Situação | Status HTTP | Ação Java | Retry? |
|----------|-------------|-----------|--------|
| Payload inválido | 422 | Corrigir dados | ❌ |
| JSON malformado | 400 | Corrigir serialização | ❌ |
| Erro interno API | 5xx | Fallback | ✅ |
| Timeout | - | Fallback | ✅ |
| Conexão recusada | - | Fallback | ❌ |

---

## Configurações Críticas

### Timeout
- **API Python**: 2500ms
- **Java recomendado**: 3000ms
- **Nunca aumente** permanentemente

### Headers
```java
headers.setContentType(MediaType.APPLICATION_JSON);
headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
```

### CORS (desenvolvimento)
- Origins permitidas: `http://localhost:8080`
- Se erro CORS → problema na API Python

---

## Testes Rápidos

### Health Check
```bash
curl http://localhost:8000/health
# Esperado: {"status": "ok"}
```

### Previsão Válida
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"companhia_aerea":"AA","aeroporto_origem":"JFK","aeroporto_destino":"LAX","data_hora_partida":"2024-01-15T14:30:00","distancia_km":3980.0}'
```

### Previsão Inválida
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"companhia_aerea":"AA"}'
# Esperado: 422
```

---

## Quando Chamar Data Science

❌ **NÃO chamar para**:
- Timeouts esporádicos
- Erros 4xx (problema no Java)
- Questões de performance normal

✅ **CHAMAR para**:
- API sempre retorna 5xx
- Contrato mudou (novos campos/códigos)
- `/health` nunca responde
- Mudanças no formato de resposta

---

## Logs Essenciais

```java
// Sucesso
log.info("Previsao obtida flight={} atraso={} probabilidade={}",
    "JFK-LAX", atraso, probabilidade);

// Erro
log.error("Erro API Python flight={} status={} duration={}ms",
    "JFK-LAX", statusCode, duration);
```

---

## Fallback Recomendado

```java
private PredictionResult fallback(FlightData flight) {
    // Regra simples: atraso se distância > 3000km
    boolean atraso = flight.distancia_km > 3000;
    double probabilidade = atraso ? 0.7 : 0.3;

    log.warn("Usando fallback para flight {}", flight.aeroporto_origem + "-" + flight.aeroporto_destino);

    return new PredictionResult(atraso, probabilidade);
}
```

---

Este guia é **intencionalmente curto**. Se não resolve, consulte o README.md ou TROUBLESHOOTING.md.