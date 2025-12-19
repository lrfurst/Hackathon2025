# ✈️ FlightOnTime: Predição de Atrasos Aéreos

> **Status:** MVP Entregue 🚀

## 📋 Sobre o Projeto
O **FlightOnTime** é uma solução de Data Science e Engenharia de Software desenvolvida durante o Hackathon. O objetivo é prever a probabilidade de atraso de um voo comercial com base em dados históricos, permitindo que passageiros e companhias aéreas se antecipem a imprevistos.

A solução consiste em um **Modelo de Machine Learning** integrado a uma **API REST**, capaz de receber dados de um voo e retornar a classificação (Pontual/Atrasado) e a probabilidade associada.

---

## 📂 Estrutura do Repositório
O projeto está organizado em um Monorepo para facilitar a integração contínua entre Ciência de Dados e Back-End:

```text
FlightOnTime/
├── backend/          # API REST em Java (Spring Boot)
├── datascience/      # Notebooks de Análise (EDA), Limpeza e Treinamento
├── models/           # Modelos serializados (.joblib) prontos para produção
└── README.md         # Documentação do Projeto
```

## 🧠 Ciência de Dados (Data Science)

A equipe realizou um ciclo completo de ciência de dados: Limpeza, Análise Exploratória (EDA), Feature Engineering e Modelagem.

🔍 Principais Insights da Análise Multivariada
Durante a etapa de análise, identificamos padrões críticos que guiaram a construção do modelo:

Tratamento de Viés Temporal (O caso das 04:00 AM):

Detectamos que horários da madrugada possuíam baixíssima amostragem (ex: apenas 1 voo às 04h), gerando ruído estatístico.

Solução: Substituímos a variável de hora exata por Turnos Operacionais (Manhã vs. Tarde/Noite), garantindo estabilidade ao modelo.

O "Efeito Bola de Neve":

Confirmamos estatisticamente que atrasos se acumulam ao longo do dia. Voos no 2º Turno (Tarde/Noite) têm probabilidade de atraso significativamente maior devido a atrasos reacionários.

Prevenção de Data Leakage (Vazamento de Dados):

Identificamos multicolinearidade perfeita entre distância e tempo de voo.

Decisão: Utilizamos apenas a Distância, pois o tempo real de voo só é conhecido após o pouso (o que seria um vazamento de dados futuros na predição).

Impacto da Companhia Aérea:

A variável op_unique_carrier provou ser um dos maiores discriminadores de atraso, refletindo a eficiência operacional de cada empresa.

🛠️ Tecnologias e Bibliotecas
Linguagem: Python 3.10+

Análise: Pandas, NumPy

Visualização: Seaborn, Matplotlib

Machine Learning: Scikit-Learn

Serialização: Joblib

📓 Como reproduzir a análise:
Acesse a pasta datascience/.

Instale as dependências: pip install -r requirements.txt

Execute os notebooks na ordem numérica.

## ☕ Back-End (API)
A API REST foi desenvolvida com o objetivo de **consumir o modelo de Machine Learning treinado** e **servir predições de atraso de voos** de forma simples e eficiente, permitindo a integração com aplicações externas, como front-end, dashboards ou outros serviços.

O serviço expõe um endpoint principal responsável por receber os dados do voo, processá-los e retornar a previsão de atraso.

---

### 📍 Endpoint Principal

**POST** `/predict`

---

### 📥 Entrada (Request)

A API recebe um objeto JSON contendo as principais informações do voo, como:

- Companhia aérea  
- Aeroporto de origem  
- Data do voo  
- Distância do trajeto  

Esses dados são utilizados como **variáveis de entrada para o modelo de predição**.

---

### 📤 Saída (Response)

A resposta da API é um objeto JSON contendo:

- **Status do voo:** classificação binária (*Pontual* ou *Atrasado*)  
- **Probabilidade de atraso:** valor percentual associado à predição (0 a 1)  

Essas informações permitem que usuários e sistemas consumidores **tomem decisões de forma antecipada**.

---

### 🛠️ Tecnologias Utilizadas

- Java  
- Spring Boot  
- API REST  

---

A arquitetura  foi pensada para ser **simples, escalável e de fácil manutenção**, facilitando futuras evoluções.
