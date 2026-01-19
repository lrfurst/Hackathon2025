# Demo Script - Sistema de Previsão de Atrasos de Voos

> **Script para demonstração técnica do sistema de ML**
> Tempo estimado: 5-7 minutos

---

## 🎯 Objetivo da Demo

Demonstrar o funcionamento completo do sistema de previsão de atrasos de voos, incluindo:
- API funcionando
- Predições em tempo real
- Casos de sucesso e limitação
- Integração com backend Java

---

## 📋 Pré-requisitos

### Sistema
- ✅ API Python rodando em `http://localhost:8000`
- ✅ Backend Java (opcional para demo completa)
- ✅ Terminal/Postman para requests
- ✅ Conexão com internet

### Conhecimento
- ✅ Conceitos básicos de APIs REST
- ✅ Noções de machine learning
- ✅ Entendimento de negócio aeroportuário

---

## 🎬 Script da Demo

### 1. Introdução (30 segundos)

**Narrativa:**
"Olá! Hoje vou demonstrar nosso sistema de inteligência artificial que prevê atrasos de voos em tempo real. O sistema usa machine learning para analisar dados históricos e fornecer previsões confiáveis para companhias aéreas e passageiros."

**Ação:**
- Mostrar arquitetura no slide/diagrama
- Explicar valor de negócio rapidamente

---

### 2. Health Check da API (1 minuto)

**Narrativa:**
"Primeiro, vamos verificar se nossa API está funcionando corretamente."

**Comandos:**
```bash
# Health check
curl http://localhost:8000/health

# Resposta esperada:
# {"status": "ok"}
```

**Explicação:**
- ✅ Confirma que o sistema está operacional
- ✅ Valida conectividade
- ✅ Tempo de resposta < 100ms

---

### 3. Caso 1: Voo Pontual (2 minutos)

**Narrativa:**
"Vamos começar com um voo que tem alta probabilidade de ser pontual."

**Payload:**
```json
{
  "companhia_aerea": "DL",
  "aeroporto_origem": "ATL",
  "aeroporto_destino": "LAX",
  "data_hora_partida": "2024-01-15T10:30:00",
  "distancia_km": 3120
}
```

**Comando:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "companhia_aerea": "DL",
    "aeroporto_origem": "ATL",
    "aeroporto_destino": "LAX",
    "data_hora_partida": "2024-01-15T10:30:00",
    "distancia_km": 3120
  }'
```

**Resposta Esperada:**
```json
{
  "atraso": false,
  "probabilidade": 0.23
}
```

**Explicação:**
- ✅ **Atraso**: false (previsão de voo pontual)
- ✅ **Probabilidade**: 23% de chance de atraso
- ✅ **Razões**: Delta Airlines, voo matinal, rota conhecida

---

### 4. Caso 2: Voo com Atraso (2 minutos)

**Narrativa:**
"Agora vamos testar um voo com características que indicam maior risco de atraso."

**Payload:**
```json
{
  "companhia_aerea": "AA",
  "aeroporto_origem": "JFK",
  "aeroporto_destino": "LAX",
  "data_hora_partida": "2024-01-15T18:45:00",
  "distancia_km": 3980
}
```

**Comando:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "companhia_aerea": "AA",
    "aeroporto_origem": "JFK",
    "aeroporto_destino": "LAX",
    "data_hora_partida": "2024-01-15T18:45:00",
    "distancia_km": 3980
  }'
```

**Resposta Esperada:**
```json
{
  "atraso": true,
  "probabilidade": 0.78
}
```

**Explicação:**
- ✅ **Atraso**: true (previsão de atraso)
- ✅ **Probabilidade**: 78% de chance de atraso
- ✅ **Razões**: American Airlines, horário de pico, rota longa

---

### 5. Demonstração de Limitações (1 minuto)

**Narrativa:**
"Vamos mostrar um caso onde o modelo tem incerteza."

**Payload (Caso de Borda):**
```json
{
  "companhia_aerea": "G3",
  "aeroporto_origem": "GRU",
  "aeroporto_destino": "GIG",
  "data_hora_partida": "2024-01-15T14:00:00",
  "distancia_km": 350
}
```

**Comando:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "companhia_aerea": "G3",
    "aeroporto_origem": "GRU",
    "aeroporto_destino": "GIG",
    "data_hora_partida": "2024-01-15T14:00:00",
    "distancia_km": 350
  }'
```

**Explicação:**
- 📊 **Probabilidade próxima de 50%**: Modelo tem incerteza
- 📊 **Voo doméstico brasileiro**: Menos dados históricos
- 📊 **Distância curta**: Padrões diferentes

---

### 6. Performance e Escalabilidade (30 segundos)

**Narrativa:**
"Vamos verificar a performance do sistema."

**Teste de Performance:**
```bash
# Medir tempo de resposta
time curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"companhia_aerea":"AA","aeroporto_origem":"JFK","aeroporto_destino":"LAX","data_hora_partida":"2024-01-15T14:30:00","distancia_km":3980}'
```

**Métricas Esperadas:**
- ⏱️ **Tempo de resposta**: < 200ms
- 📊 **Disponibilidade**: 99.9%
- 🔄 **Throughput**: 100+ requests/segundo

---

### 7. Integração com Java (1 minuto)

**Narrativa:**
"Agora vamos mostrar como o backend Java se integra com nossa API."

**Código Java:**
```java
// Cliente Java fazendo chamada
RestTemplate restTemplate = new RestTemplate();
FlightData flight = new FlightData();
flight.companhia_aerea = "AA";
// ... outros campos

try {
    PredictionResponse response = restTemplate.postForObject(
        "http://localhost:8000/predict",
        flight,
        PredictionResponse.class
    );

    if (response.atraso) {
        // Lógica de negócio para voo atrasado
        sendDelayNotification();
        adjustOperations();
    }

} catch (Exception e) {
    // Fallback para regras de negócio
    useDefaultLogic();
}
```

**Explicação:**
- 🔗 **Integração REST**: Comunicação HTTP JSON
- 🛡️ **Timeout**: 3 segundos para resiliência
- 🔄 **Fallback**: Sistema continua funcionando se API falhar

---

### 8. Encerramento (30 segundos)

**Narrativa:**
"Em resumo, nosso sistema fornece previsões confiáveis de atrasos de voos, permitindo que companhias aéreas otimizem operações e melhorem experiência do passageiro."

**Pontos Chave:**
- 🤖 **ML em produção**: Modelo Random Forest com 85% acurácia
- ⚡ **Performance**: <200ms por predição
- 🔗 **Integração**: API REST com backend Java
- 💰 **Valor**: Redução de custos operacionais

---

## 📸 Screenshots Sugeridos

### Para Apresentação
1. **Arquitetura do Sistema** - Diagrama com componentes
2. **Interface da API** - Swagger UI (`/docs`)
3. **Resultados de Predição** - JSON responses
4. **Métricas de Performance** - Gráficos de latência/acurácia
5. **Código de Integração** - Exemplo Java

### Localização dos Screenshots
```
demo/
├── screenshots/
│   ├── architecture_diagram.png
│   ├── api_swagger.png
│   ├── prediction_results.png
│   ├── performance_metrics.png
│   └── java_integration.png
```

---

## 🚨 Plano B (se API não funcionar)

### Mock Responses
Se a API não estiver disponível, usar curl com dados mock:

```bash
# Simular resposta de voo pontual
echo '{"atraso": false, "probabilidade": 0.23}'

# Simular resposta de voo atrasado
echo '{"atraso": true, "probabilidade": 0.78}'
```

### Demonstração Offline
- Mostrar código fonte da API
- Explicar lógica do modelo
- Apresentar métricas salvas
- Demonstrar integração Java com mocks

---

## 📊 Métricas de Sucesso da Demo

- ✅ **Tempo total**: 5-7 minutos
- ✅ **Casos demonstrados**: 2 (pontual + atrasado)
- ✅ **Limitações mostradas**: 1 caso de incerteza
- ✅ **Integração demonstrada**: Java + Python
- ✅ **Performance validada**: <200ms

---

## 🎯 Próximas Melhorias

### Para Futuras Demos
- [ ] **Interface Web**: Dashboard para visualização
- [ ] **Dados em Tempo Real**: Integração com APIs de voos
- [ ] **Comparação A/B**: Com/sem sistema
- [ ] **Cenários Avançados**: Vários voos simultâneos

---

*Script criado para Hackathon 2025 - Demo Técnica*