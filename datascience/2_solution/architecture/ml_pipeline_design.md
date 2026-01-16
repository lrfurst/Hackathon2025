# 🏗️ ML Pipeline Design - FlightOnTime Pro
**Data:** 16/01/2026 | **Responsável:** @ananda.matos

## Steps: input → transform → predict → output
1. **Input:** JSON (5 campos: Origin, Dest, DepTime, DayOfWeek, Carrier).
2. **Transform:** Encoder simples (OHE) e Scaler.
3. **Predict:** LogisticRegression(class_weight='balanced').
4. **Output:** {previsao: int, probabilidade: float, custo_evitado: float}

## Escolha do Algoritmo
- **Modelo:** Regressão Logística.
- **Justificativa:** Menor latência, integração rápida em 48h e facilidade de depuração em relação a Ensembles.
- **Métrica Alvo:** RECALL > 0.75.
