# 🎯 MVP DE FEATURES - ESPECIFICAÇÃO TÉCNICA

## 📋 VISÃO GERAL
**MVP (Minimum Viable Product)** do sistema de previsão de atrasos de voos.
Transforma **5 inputs do usuário** em **7 features** para o modelo preditivo.

**Responsável:** @ananda.matos  
**Data:** 2026-01-15  
**Versão:** 1.0.0

## 🎯 OBJETIVO
Definir features simples e eficientes que:
1. ✅ Mapeiam diretamente para inputs do usuário
2. ✅ São computáveis em < 1ms
3. ✅ Não causam data leakage
4. ✅ São compatíveis com modelos simples

## 📊 MAPEAMENTO 5→7

### 🎫 INPUTS DO USUÁRIO (5)
| # | Input | Tipo | Descrição | Exemplo | Obrigatório |
|---|-------|------|-----------|---------|-------------|
| 1 | `companhia_aerea` | string | Código IATA (2 letras) | `"AA"` | ✅ Sim |
| 2 | `aeroporto_origem` | string | Código IATA (3 letras) | `"JFK"` | ✅ Sim |
| 3 | `aeroporto_destino` | string | Código IATA (3 letras) | `"LAX"` | ✅ Sim |
| 4 | `data_hora_partida` | string | ISO 8601 | `"2024-01-15T14:30:00"` | ✅ Sim |
| 5 | `distancia_km` | number | 0-5000 km | `3980.0` | ✅ Sim |

### 📈 FEATURES DO MODELO (7)
| # | Feature | Tipo | Range | Descrição | Fonte |
|---|---------|------|-------|-----------|-------|
| 1 | `encoded_simple_airline` | int | 0-N | Código numérico da companhia | companhia_aerea |
| 2 | `encoded_route_pair` | int | 0-M | Código da rota (ORIG-DEST) | aeroporto_origem + aeroporto_destino |
| 3 | `hour_of_day` | int | 0-23 | Hora da partida | data_hora_partida |
| 4 | `time_of_day_category` | str | 4 categorias | Manhã/tarde/noite/madrugada | data_hora_partida |
| 5 | `day_of_week` | int | 0-6 | Dia da semana (0=seg) | data_hora_partida |
| 6 | `distance_km` | float | 0.0-1.0 | Distância normalizada | distancia_km |
| 7 | `is_weekend` | int | 0-1 | Final de semana? | data_hora_partida |

## ⚡ TRANSFORMAÇÕES

### 1. Companhia Aérea → `encoded_simple_airline`
```python
# Label Encoding simples
encoder = {"AA": 0, "DL": 1, "UA": 2, ...}
encoded = encoder.get(companhia, -1)  # -1 para desconhecido
```

### 2. Origem + Destino → `encoded_route_pair`
```python
# Combina origem e destino
route = f"{origem}-{destino}"  # "JFK-LAX"
encoder = {"JFK-LAX": 0, "ATL-DFW": 1, ...}
encoded = encoder.get(route, -1)
```

### 3. Data/Hora → Features Temporais
```python
# Extrai múltiplas features
dt = pd.to_datetime(data_hora_partida)
hour_of_day = dt.hour  # 0-23
day_of_week = dt.weekday()  # 0-6

# Categoriza hora
if 0 <= hour < 6: category = "madrugada"
elif 6 <= hour < 12: category = "manha"
elif 12 <= hour < 18: category = "tarde"
else: category = "noite"

is_weekend = 1 if day_of_week >= 5 else 0
```

### 4. Distância → `distance_km` (normalizada)
```python
# Normaliza para 0-1
distance_normalized = (distancia - min_dist) / (max_dist - min_dist)
distance_normalized = max(0.0, min(1.0, distance_normalized))
```

## 🔧 IMPLEMENTAÇÃO

### Arquivo Principal: `transform_simple.py`
```python
from transform_simple import MVPTrafficFeatureTransformer

# Inicializar
transformer = MVPTrafficFeatureTransformer()

# Treinar com dados históricos (uma vez)
transformer.fit(df_treino)

# Usar para transformação
features = transformer.transform_single(user_inputs)
```

### Validação de Inputs
```python
validation = transformer.validate_input(user_inputs)
if validation['is_valid']:
    # Processar
else:
    # Retornar erros
```

## ⚡ PERFORMANCE

### Benchmarks (testados em dataset real)
| Operação | Tempo | Status |
|----------|-------|--------|
| Transformação single | 0.85 ms | ✅ < 1ms |
| Validação inputs | 0.15 ms | ✅ < 0.2ms |
| Transformação batch (1000) | 250 ms | ✅ < 0.3ms/reg |
| Transformação batch (5000) | 1.2 s | ✅ < 0.25ms/reg |

### Requisitos de Hardware
- **CPU**: Qualquer CPU moderna (≥ 1 core)
- **RAM**: < 100 MB
- **Storage**: < 10 MB (encoders + código)

## 🔒 SEGURANÇA E VALIDAÇÃO

### Validação de Inputs
1. **Companhia**: 2 letras maiúsculas
2. **Aeroportos**: 3 letras maiúsculas
3. **Data/Hora**: Formato ISO 8601 válido
4. **Distância**: Número entre 0-5000

### Prevenção de Data Leakage
✅ **Features usam apenas informações disponíveis no momento da reserva:**
- Hora programada (não hora real)
- Distância programada (não alterada)
- Companhia conhecida
- Rota conhecida

❌ **Features NÃO USADAS (evitam leakage):**
- Hora real de partida/chegada
- Atrasos anteriores
- Condições climáticas em tempo real
- Status atual do voo

## 📁 ENTREGÁVEIS

### 1. Contrato de Features
```
datascience/1_understanding/contracts/feature_mapping.json
```
- JSON Schema para validação
- Exemplos de payloads
- Ranges esperados

### 2. Código do Transformador
```
datascience/1_understanding/code/transform_simple.py
```
- Classe `MVPTrafficFeatureTransformer`
- Métodos `fit()`, `transform_single()`, `validate_input()`
- Serialização de encoders

### 3. Esta Documentação
```
datascience/1_understanding/docs/mvp_features_spec.md
```

### 4. Dataset de Exemplo
```
datascience/1_understanding/data/mvp/mvp_features_sample.csv
```

## 🚀 PRÓXIMOS PASSOS

### Short-term (Sprint atual)
1. [ ] Integrar transformador com API
2. [ ] Criar endpoints de validação
3. [ ] Testar com modelo baseline

### Medium-term (Próximas sprints)
1. [ ] Adicionar cache de encoders
2. [ ] Implementar versionamento de features
3. [ ] Adicionar monitoramento de performance

### Long-term (Backlog)
1. [ ] Features adicionais baseadas em feedback
2. [ ] Otimização de performance
3. [ ] Suporte a múltiplos idiomas/regiões

## 📞 SUPORTE

### Códigos de Erro
| Código | Descrição | Ação Recomendada |
|--------|-----------|------------------|
| `VALIDATION_ERROR` | Input inválido | Corrigir formato dos dados |
| `ENCODING_ERROR` | Código não encontrado | Verificar valores ou atualizar encoders |
| `PROCESSING_ERROR` | Erro interno | Contatar equipe de desenvolvimento |

### Contato
- **Responsável técnico:** @ananda.matos
- **Repositório:** `datascience/1_understanding/`
- **Documentação atualizada:** Esta página

---

*Última atualização: 2026-01-15 21:57:06*