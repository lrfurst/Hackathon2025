# 📊 Story 1.1: Análise Exploratória Estratégica

## 📋 Sobre
Análise exploratória inicial do dataset de voos para compreensão dos dados e identificação de problemas críticos.

## 🗓️ Data de Execução
2026-01-15 21:00:44

## 📈 Métricas Principais
- **Total de voos**: 10,000
- **Taxa de atrasos**: 21.19%
- **Balanceamento**: 0.269
- **Acurácia baseline**: 78.81%

## 📁 Estrutura de Arquivos

### 📓 Notebooks
- `story_1_1_analise_estrategica.ipynb` - Notebook Jupyter completo
- `story_1_1_analise_estrategica.py` - Código Python
- `story_1_1_analise_estrategica.html` - Versão HTML (se disponível)

### 📊 Dados
- `flight_data_with_target.csv` - Dataset com variável alvo
- `target_variable_analysis.csv` - Análise da variável alvo
- `quick_analysis_report.txt` - Resumo da análise

### 📄 Documentação
- `business_insights.md` - Insights de negócio
- `visualizations/` - Gráficos e dashboards

### 🔍 Features Promissoras (Top 5)
1. arr_delay
1. dep_delay
1. late_aircraft_delay
1. nas_delay
1. carrier_delay

## ⚠️ Problemas Identificados
- • 1 colunas com >50% de valores ausentes
- • 7 colunas suspeitas de vazamento de dados
- • Dataset desbalanceado (razão: 0.269)

## 🚀 Próximos Passos
1. Executar Story 1.2: Análise Univariada
2. Tratar valores missing identificados
3. Remover features com vazamento de dados
4. Balancear dataset se necessário

## 👤 Responsável
@ananda.matos

## 📊 Status
✅ COMPLETADA - 15/01/2026
