# 🏗️ ML Pipeline Design - FlightOnTime Pro

**Responsável:** @ananda.matos
**Algoritmo Base:** LogisticRegression (class_weight='balanced')
**Métrica Primária:** Recall (> 0.75)

## 1. Fluxo End-to-End
O pipeline foi desenhado para baixa latência, priorizando a identificação de atrasos (Recall) para minimizar custos de operação.



- **Input:** JSON com 5 campos (Origin, Dest, DepTime, DayOfWeek, Carrier).
- **Transform:** One-Hot Encoding (OHE) simplificado + Standard Scaling.
- **Predict:** Logistic Regression (Inferência < 100ms).
- **Output:** JSON com `previsao`, `probabilidade` e `custo_evitado`.

## 2. Justificativa Técnica
Optou-se por Regressão Logística em vez de Ensembles (RandomForest/XGBoost) para garantir:
1. **Integração em 48h:** Menor complexidade de serialização (Pickle/Joblib).
2. **Interpretabilidade:** Pesos dos coeficientes claros para o Backend Java.
3. **Performance:** Cumprimento do timeout de 2s com folga.
