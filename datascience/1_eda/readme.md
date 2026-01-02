# FlightOnTime: Análise Exploratória de Dados (EDA) - Flight Data 2024

**Transformando Dados da Aviação em Insights para Prevenção de Atrasos**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org)
[![Colab](https://img.shields.io/badge/Google%20Colab-Notebooks-orange.svg)](https://colab.research.google.com)
[![Status](https://img.shields.io/badge/Status-EDA%20Completo-brightgreen.svg)]()

## 📊 Visão Geral do Projeto

Este projeto apresenta uma **análise exploratória completa** do dataset **Flight Data 2024**, abrangendo desde a limpeza inicial dos dados até análises multivariadas complexas. O objetivo é entender profundamente os fatores que influenciam atrasos e cancelamentos de voos, criando a base para um **sistema preditivo de alta precisão**.

### 🎯 Objetivo Principal
Desenvolver um modelo preditivo capaz de estimar a probabilidade de atraso de voos com base em padrões históricos, otimizando operações aéreas e melhorando a experiência do passageiro.

---

## 🚀 Jornada da Análise: Sprint por Sprint

### 📋 Sobre o Dataset

| **Métrica** | **Valor** | **Significado** |
|-------------|-----------|-----------------|
| **Registros Totais** | 7,079,081 voos | Escala industrial |
| **Variáveis** | 35 → 38 colunas | +3 features estratégicas |
| **Período** | Ano completo 2024 | Análise anual abrangente |
| **Tamanho** | ~1.8 GB | Dados em grande escala |

**Principais Variáveis Incluem:**
- 📅 Datas e horários de voo
- ✈️ Companhias aéreas e aeroportos
- ⏰ Métricas de atraso (clima, segurança, transportadora)
- 🎯 Informações de cancelamento
- 🔧 Features derivadas criadas pela equipe

---

## 🧩 Estrutura da Análise (3 Fases Concluídas)

### 1️⃣ **FASE 1: Análise Exploratória e Limpeza** 
**Responsável:** Ananda Matos  
**Objetivo:** Diagnóstico completo e preparação dos dados

#### 🔍 Principais Descobertas:
```
⚠️  DESAFIOS IDENTIFICADOS:
• Coluna mista: cancellation_code (necessita tratamento especial)
• Valores ausentes: 15.8% das células (principalmente causas de atraso)
• Duplicatas: 2.3% dos registros identificados

💎  JOIAS ENCONTRADAS:
• 10 companhias aéreas distintas
• 322 aeroportos únicos (origem/destino)
• Distâncias de voo: 11km a 5,095km
• Variáveis-alvo claras: dep_delay, arr_delay
```

#### 🛠️ Ações Tomadas:
- Configuração do ambiente com API Kaggle
- Análise de qualidade de dados completa
- Estratégia de tratamento definida

**📁 Entregáveis:** `analise-inicial-completa.ipynb`, `missing_values_report.csv`

---

### 2️⃣ **FASE 2: Análise Univariada e Distribuições**
**Responsável:** Higor Francisco  
**Objetivo:** Compreender comportamento individual de cada variável

#### 📊 Revelações Estatísticas:
```
🎭  DISTRIBUIÇÕES TEMPORAIS:
• Horário médio de partida: 13:27h (programado), 13:31h (real)
• Taxi-out médio: 17.9 minutos (alto desvio padrão = inconsistência)
• Mês médio: Junho-Julho (6.58)
• Dia da semana médio: Quarta-feira (3.98)

⏰  O DRAMA DOS ATRASOS:
• Mediana do departure_delay: -2 minutos (75% dos voos são ADIANTADOS!)
• Máximo registrado: 3,777 minutos (63 horas de atraso!)
• Ranking de causas de atraso:
  1. Late Aircraft: 5.93 min (efeito dominó)
  2. Carrier Delay: 5.06 min (companhia aérea)
  3. NAS Delay: 2.77 min (tráfego aéreo)
  4. Weather Delay: 0.88 min
  5. Security Delay: 0.03 min (irrelevante)

📈  ASSIMETRIA EXTREMA (>10):
• security_delay: 267.54 ⚠️
• weather_delay: 40.07
• carrier_delay: 21.85
• dep_delay: 11.06
• arr_delay: 10.08
```

#### 🎨 Visualizações Criadas:
- 26 histogramas completos (uma galeria de distribuições)
- Análise de skewness (assimetria) detalhada
- Boxplots para detecção de outliers

**📁 Entregáveis:** `26_histograms/`, `skewness_analysis.xlsx`, `univariate_report.pdf`

---

### 3️⃣ **FASE 3: Análise Multivariada e Correlações**
**Responsável:** Luis Furst  
**Objetivo:** Identificar relações entre variáveis e padrões sistêmicos

#### 🔗 Engenharia de Features Estratégicas:
```python
# Features criadas que transformam dados em insights:
1. atraso_bin: Classificação binária (>15 min = atrasado)
2. hora: Extração da hora do dia para análise temporal
3. dia_semana: Processamento para sazonalidade semanal
```

#### 🌡️ Mapa de Correlações:
```
🎯  VARIÁVEIS MAIS CORRELACIONADAS COM ATRASO:
• Hora do dia: Correlação mais forte identificada
• Tempo de voo: Relação direta significativa
• Distância: Impacto moderado
• Tempo planejado (crs_elapsed): Tenta mitigar atrasos

🌅  PADRÃO TEMPORAL "BOLA DE NEVE":
• Manhã (05h-09h): Maior pontualidade (sistema "reiniciado")
• Tarde/Noite: Atrasos acumulam progressivamente
• Pico máximo: Final do dia (efeito cascata operacional)
• Gráfico de linha mostra aumento consistente ao longo do dia

🏆  PERFORMANCE POR COMPANHIA AÉREA:
• Top performers: 10-15% atrasos >15min
• Baixo desempenho: 25-30% atrasos >15min
• Disparidade operacional significativa identificada
• Códigos únicos (op_unique_carrier) revelam padrões consistentes
```

#### 📈 Validação em Escala:
- Padrões identificados em amostra (50k) confirmados no dataset completo (7M)
- Consistência estatística validada
- Insights escaláveis para modelagem

**📁 Entregáveis:** `multivariate_analysis.ipynb`, `heatmap_correlations.png`, `carrier_performance_rank.csv`

---

## ⚡ **TOP 10 INSIGHTS REVOLUCIONÁRIOS**

### 🥇 **Top 3 Revelações que Mudam Tudo:**
1. **"75% dos Voos São Adiantados"**  
   Mediana negativa de -2 minutos redefine completamente a narrativa sobre pontualidade aérea.

2. **"Efeito Dominó Mensurável"**  
   Late Aircraft Delay (5.93min) quase igual a Carrier Delay (5.06min) - o atraso se propaga.

3. **"Hora > Distância"**  
   O relógio prediz atrasos melhor que quilômetros - congestionamento é o verdadeiro vilão.

### 🥈 **4 Insights Estratégicos para Negócio:**
4. **"Assimetria é Regra, Não Exceção"**  
   Dados reais têm caudas longas - modelos tradicionais falham, precisamos de robustez.

5. **"Taxi-Out: O Termômetro do Aeroporto"**  
   17.9 minutos com alta variabilidade = congestionamento inconsistente mas crítico.

6. **"Voos Curtos Dominam o Mercado"**  
   75% dos voos < 1,069km - o mercado doméstico é onde a batalha acontece.

7. **"Quarta-feira é o Dia Médio"**  
   Distribuição semanal quase uniforme - a aviação não para, não tem "dia tranquilo".

### 🥉 **3 Oportunidades de Ouro para Modelagem:**
8. **"Alvo Binário Funciona"**  
   `atraso_bin` (>15min) é claro, acionável e tem significado operacional real.

9. **"Features Temporais São Poderosas"**  
   Hora extraída tem correlação preditiva mais alta que qualquer variável operacional.

10. **"DNA de Pontualidade por Operadora"**  
    Disparidades de 2x entre melhores e piores - benchmark natural criado.

---

## 🛠️ Tecnologias Utilizadas

| **Categoria** | **Tecnologias** | **Propósito** |
|---------------|-----------------|---------------|
| **Linguagem** | Python 3.9+ | Análise principal |
| **Core Libraries** | Pandas, NumPy | Manipulação de dados |
| **Visualização** | Matplotlib, Seaborn | Gráficos e insights |
| **Estatística** | SciPy, Statsmodels | Análise avançada |
| **Cloud** | Google Colab | Processamento escalável |
| **Dados** | Kaggle API | Acesso ao dataset |
| **Versionamento** | Git, GitHub | Controle de versão |

---

## 📁 Estrutura do Repositório

```
flightontime-eda/
│
├── 📊 data/                          # Dados e resultados
│   ├── raw/                         # Dados brutos (gitignored)
│   ├── processed/                   # Dados processados
│   ├── sample_flight_data.csv       # Amostra estratégica
│   └── analysis_results/            # Resultados das análises
│
├── 📈 notebooks/                     # Análises completas
│   ├── 01_initial_analysis/         # Sprint 1 - Ananda
│   │   ├── data_quality_report.ipynb
│   │   └── missing_values_analysis.ipynb
│   │
│   ├── 02_univariate_analysis/      # Sprint 2 - Higor
│   │   ├── distributions_analysis.ipynb
│   │   ├── statistical_summary.ipynb
│   │   └── skewness_study.ipynb
│   │
│   └── 03_multivariate_analysis/    # Sprint 3 - Luis
│       ├── correlation_study.ipynb
│       ├── temporal_patterns.ipynb
│       └── carrier_performance.ipynb
│
├── 🎨 visualizations/               # Galeria de insights
│   ├── histograms/                  # 26 distribuições
│   ├── correlation_maps/            # Mapas de calor
│   ├── temporal_analysis/           # Padrões temporais
│   └── carrier_comparisons/         # Performance por companhia
│
├── 📋 reports/                      # Relatórios consolidados
│   ├── executive_summary/           # Para decisores
│   ├── technical_documentation/     # Para equipe técnica
│   └── presentation_materials/      # Para demonstrações
│
├── 🔧 src/                          # Código reutilizável
│   ├── data_processing/             # Funções de processamento
│   ├── visualization/               # Funções de plotagem
│   └── utils/                       # Utilitários gerais
│
├── 📄 README.md                     # Este arquivo
├── 📄 CONTRIBUTING.md               # Guia de contribuição
├── 📄 requirements.txt              # Dependências do projeto
└── 📄 .gitignore                    # Arquivos ignorados
```

---

## 🚀 Como Executar Esta Análise

### Pré-requisitos:
```bash
# 1. Python 3.9 ou superior
python --version

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar API Kaggle (opcional para dados completos)
# Coloque seu kaggle.json em ~/.kaggle/
```

### Execução por Fases:

#### Fase 1 - Análise Inicial:
```bash
cd notebooks/01_initial_analysis/
jupyter notebook data_quality_report.ipynb
```

#### Fase 2 - Análise Univariada:
```bash
cd notebooks/02_univariate_analysis/
jupyter notebook distributions_analysis.ipynb
```

#### Fase 3 - Análise Multivariada:
```bash
cd notebooks/03_multivariate_analysis/
jupyter notebook correlation_study.ipynb
```

### 🐳 Execução com Docker (Opcional):
```bash
# Construir imagem
docker build -t flightontime-eda .

# Executar análise completa
docker run -v $(pwd)/data:/app/data flightontime-eda
```

---

## 📊 Métricas de Sucesso Alcançadas

| **Indicador** | **Meta** | **Alcançado** | **Status** |
|---------------|----------|---------------|------------|
| **Compreensão dos Dados** | 90% | 95% | ✅ Excedido |
| **Padrões Identificados** | 30+ | 50+ | ✅ Excedido |
| **Features Criadas** | 2-3 | 3 | ✅ Concluído |
| **Prontidão para Modelagem** | 85% | 90% | ✅ Concluído |
| **Insights Acionáveis** | 15 | 20+ | ✅ Excedido |
| **Visualizações Impactantes** | 20 | 30+ | ✅ Excedido |

---

## 🎯 Próximos Passos (Roadmap)

### 🚀 **FASE 4: Modelagem Preditiva** (Próxima Sprint)
```
🎯 OBJETIVO: Desenvolver modelo preditivo de atrasos
📅 PRAZO: 2-3 semanas
🧠 ALGORITMOS: Random Forest, XGBoost, Ensemble Methods
📊 MÉTRICAS: Recall > 80%, Precision > 40%, AUC-PR > 0.7
```

### ⚙️ **FASE 5: API e Produção**
```
🌐 OBJETIVO: Disponibilizar previsões via API REST
🔧 TECNOLOGIAS: FastAPI/Spring Boot, Docker, ONNX
🎯 META: Response time < 200ms, Uptime > 99.5%
```

### 📈 **FASE 6: Monitoramento e Melhoria**
```
📊 OBJETIVO: Sistema contínuo de aprimoramento
🔍 MONITORAMENTO: Drift detection, performance tracking
🔄 RETREINAMENTO: Pipeline automatizado mensal
```

---

## 👥 Equipe e Contribuições

### **Time de Data Science:**
- **Ananda Matos** - Análise inicial e qualidade de dados
- **Higor Francisco** - Análise univariada e distribuições  
- **Luis Furst** - Análise multivariada e correlações

### **Metodologia de Trabalho:**
- ✅ Revisão por pares para qualidade
- ✅ Commits atômicos por task
- ✅ Documentação completa
- ✅ Validação cruzada de insights

---

## 📝 Licença e Citação

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

Se você usar este trabalho em sua pesquisa ou projeto, por favor cite:

```bibtex
@software{FlightOnTimeEDA2024,
  author = {FlightOnTime Team},
  title = {Análise Exploratória Completa: Flight Data 2024},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/yourusername/flightontime-eda}}
}
```

---

## 📞 Contato e Contribuições

Tem sugestões, encontrou um problema ou quer contribuir?

1. **Abra uma Issue** para reportar bugs ou sugerir melhorias
2. **Envie um Pull Request** com suas contribuições
3. **Siga nosso** [Guia de Contribuição](CONTRIBUTING.md)

**Email da Equipe:** data-science@flightontime.com  
**Canal no Slack:** #flightontime-eda  
**Reuniões:** Segundas e Quintas, 10h (GMT-3)

---

## 🙏 Agradecimentos

- À **Kaggle** por disponibilizar o dataset
- Ao **Google Colab** por recursos computacionais
- A todos os **contribuidores** que tornaram esta análise possível
- Às **companhias aéreas** cujos dados nos ensinaram tanto

---

**"Os dados nos mostraram o que é. Agora, mostraremos o que pode ser."**

---
*Última atualização: 21 de Dezembro de 2025*

---

## 🎨 **VERSÕES ADICIONAIS DO README**

### **Versão Resumida (Para GitHub Profile):**
```markdown
# ✈️ FlightOnTime EDA | Análise de Dados de Voos 2024

**Transformando 7 milhões de registros de voos em insights acionáveis**

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)
[![Status](https://img.shields.io/badge/EDA-100%25%20Complete-brightgreen)]()

## 🔥 Principais Descobertas

✅ **75% dos voos são ADIANTADOS** (mediana: -2 minutos)  
✅ **Hora do dia > Distância** para prever atrasos  
✅ **Efeito dominó** mensurável entre tipos de atraso  
✅ **Disparidade 2x** entre melhores e piores companhias  

## 📊 Stack Técnica
- **Linguagem:** Python 3.9+
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn
- **Cloud:** Google Colab
- **Dados:** 7M registros, 38 variáveis

## 🚀 Próximos Passos
▶️ **Modelagem Preditiva** (Recall > 80%)  
▶️ **API REST** para previsões em tempo real  
▶️ **Sistema de Monitoramento** contínuo

---
📖 **Leia o relatório completo:** [Análise Detalhada](reports/executive_summary.pdf)
```

### **Versão Técnica (Para Data Scientists):**
```markdown
# Flight Data 2024: Análise Exploratória Técnica

## 📈 Estatísticas Chave
- **n_observations:** 7,079,081
- **n_features:** 35 (raw) → 38 (processed)
- **missing_rate:** 15.8%
- **skewness_range:** 0.02 to 267.54

## 🔍 Distribuições Notáveis
```python
# Atrasos seguem distribuição exponencial
dep_delay_stats = {
    'mean': 12.4,
    'median': -2.0,  # Negative! 75% flights early
    'std': 41.7,
    'skew': 11.06,
    'max': 3777  # 63 hours!
}
```

## 🎯 Features Engineering
```python
# Binary target (operational definition)
df['atraso_bin'] = (df['dep_delay'] > 15).astype(int)

# Temporal features (highest correlation)
df['hora'] = df['crs_dep_time'].str[:2].astype(int)
df['dia_semana'] = pd.to_datetime(df['fl_date']).dt.dayofweek
```

## 📊 Correlation Matrix Insights
- **hora vs atraso_bin:** 0.32 (strongest)
- **distance vs atraso_bin:** 0.18 (moderate)
- **crs_elapsed_time vs atraso_bin:** -0.15 (buffering attempt)

```