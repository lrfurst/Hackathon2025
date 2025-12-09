# ✈️ FlightOnTime - Previsão de Atrasos Aéreos

Bem-vindo ao repositório de Ciência de Dados do time **FlightOnTime_Equipo22_DS** (Hackathon ONE 2025).

## 🎯 Objetivo
Prever a probabilidade de atraso de um voo com base em dados históricos (Companhia, Origem, Destino, Horário).

## 📂 Estrutura
- `FlightOnTime_Equipo22_DS.ipynb`: Notebook com a análise exploratória e treinamento do modelo.
- `flight_model.joblib`: Modelo serializado (Random Forest) pronto para uso em produção.
- `requirements.txt`: Dependências necessárias.

## 🛠️ Como usar (Para o time de Backend)
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
2. Carregue o modelo no seu código Python/API:
'''Python

import joblib
modelo = joblib.load('flight_model.joblib')
prediction = modelo.predict(dados_do_voo)
'''
📊 Status do Projeto

[x] MVP (Dados Simulados)

[ ] Treinamento com Dados Reais (Kaggle)

[ ] Otimização de Hiperparâmetros
