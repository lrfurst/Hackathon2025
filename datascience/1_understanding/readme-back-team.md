# README - Documentação Técnica do Projeto FlightOnTime

## ✈️ FlightOnTime: Predição de Atrasos Aéreos
**Status:** MVP Entregue 🚀

## 📋 Sobre o Projeto
O FlightOnTime é uma solução de Data Science e Engenharia de Software desenvolvida durante o Hackathon. O objetivo é prever a probabilidade de atraso de um voo comercial com base em dados históricos, permitindo que passageiros e companhias aéreas se antecipem a imprevistos.

A solução consiste em um **Modelo de Machine Learning** integrado a uma **API REST**, capaz de receber dados de um voo e retornar a classificação (Pontual/Atrasado) e a probabilidade associada.

## 📂 Estrutura do Repositório
O projeto está organizado em um **Monorepo** para facilitar a integração contínua entre Ciência de Dados e Back-End:

```
FlightOnTime/
├── backend/           # API REST em Java (Spring Boot)
├── datascience/       # Notebooks de Análise (EDA), Limpeza e Treinamento
├── models/            # Modelos serializados (.joblib) prontos para produção
└── README.md          # Documentação do Projeto
```

## 🧠 Ciência de Dados (Data Science)
A equipe realizou um ciclo completo de ciência de dados: Limpeza, Análise Exploratória (EDA), Feature Engineering e Modelagem.

### 🔍 Principais Insights da Análise Multivariada
Durante a etapa de análise, identificamos padrões críticos que guiaram a construção do modelo:

1. **Tratamento de Viés Temporal (O caso das 04:00 AM):**
   - Detectamos que horários da madrugada possuíam baixíssima amostragem (ex: apenas 1 voo às 04h), gerando ruído estatístico.
   - **Solução:** Substituímos a variável de hora exata por **Turnos Operacionais** (Manhã vs. Tarde/Noite), garantindo estabilidade ao modelo.

2. **O "Efeito Bola de Neve":**
   - Confirmamos estatisticamente que atrasos se acumulam ao longo do dia. Voos no **2º Turno (Tarde/Noite)** têm probabilidade de atraso significativamente maior devido a atrasos reacionários.

3. **Prevenção de Data Leakage (Vazamento de Dados):**
   - Identificamos multicolinearidade perfeita entre **distância** e **tempo de voo**.
   - **Decisão:** Utilizamos apenas a **Distância**, pois o tempo real de voo só é conhecido após o pouso (o que seria um vazamento de dados futuros na predição).

4. **Impacto da Companhia Aérea:**
   - A variável `op_unique_carrier` provou ser um dos maiores discriminadores de atraso, refletindo a eficiência operacional de cada empresa.

### 🛠️ Tecnologias e Bibliotecas
- **Linguagem:** Python 3.10+
- **Análise:** Pandas, NumPy
- **Visualização:** Seaborn, Matplotlib
- **Machine Learning:** Scikit-Learn
- **Serialização:** Joblib

### 📓 Como reproduzir a análise:
1. Acesse a pasta `datascience/`.
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute os notebooks na ordem numérica.

## ☕ Back-End (API)
A API REST foi desenvolvida com o objetivo de consumir o modelo de Machine Learning treinado e servir predições de atraso de voos de forma simples e eficiente, permitindo a integração com aplicações externas, como front-end, dashboards ou outros serviços.

O serviço expõe um endpoint principal responsável por receber os dados do voo, processá-los e retornar a previsão de atraso.

### 📍 Endpoint Principal
**POST** `/predict`

### 📥 Entrada (Request)
A API recebe um objeto JSON contendo as principais informações do voo, como:
- Companhia aérea
- Aeroporto de origem
- Data do voo
- Distância do trajeto

Esses dados são utilizados como variáveis de entrada para o modelo de predição.

### 📤 Saída (Response)
A resposta da API é um objeto JSON contendo:
- **Status do voo:** classificação binária (Pontual ou Atrasado)
- **Probabilidade de atraso:** valor percentual associado à predição (0 a 1)

Essas informações permitem que usuários e sistemas consumidores tomem decisões de forma antecipada.

### 🛠️ Tecnologias Utilizadas
- Java
- Spring Boot
- API REST

A arquitetura foi pensada para ser simples, escalável e de fácil manutenção, facilitando futuras evoluções.

## 🔗 Links Importantes
- **Repositório:** [https://github.com/lrfurst/Hackathon2025.git](https://github.com/lrfurst/Hackathon2025.git)

---

# ANEXO I: QUESTIONÁRIO DE ENTENDIMENTO TÉCNICO

## Levantamento – Estrutura da Solução Back-End (Hackathon)

### Entendimento Geral da Solução

1. **Qual problema principal a solução resolve e para quem ela foi pensada?**  
   (em termos simples, sem foco técnico):  
   A solução resolve o problema de antecipar o risco de atraso de voos. Ela foi pensada para **clientes finais** (passageiros) que precisam consultar rapidamente a probabilidade de atraso com base em dados do voo e para **companhias aéreas** que podem usar essas previsões para otimizar operações.

2. **Quais são as principais funcionalidades entregues pelo back-end para que a solução funcione?**  
   (ex.: salvar dados, integrar sistemas, processar informações):
   - Receber os dados do voo enviados pelo usuário
   - Validar informações e aplicar regras de negócio
   - Integrar com o modelo preditivo desenvolvido em Python
   - Retornar a probabilidade de atraso ao cliente
   - Persistir os dados da previsão no banco
   - Disponibilizar estatísticas agregadas dos voos já processados

3. **Como o back-end se conecta com o restante da solução (front-end, apps, integrações externas)?**  
   A API back-end se integra com a API Python (ML) via **WebClient**, seguindo um contrato definido pelo DTO de entrada. Resumindo: é enviada uma requisição com os dados e espera-se o retorno da previsão de atraso.

### Decisões e Organização da Solução

4. **Quais foram os principais critérios usados para definir a solução escolhida?**  
   (ex.: tempo disponível, simplicidade, facilidade de implementação, escalabilidade básica)
   - Separação de responsabilidades entre back-end e ML
   - Facilidade de evolução futura
   - Uso de tecnologias conhecidas pelo time
   - Manutenibilidade e testabilidade

5. **Quais decisões importantes precisaram ser tomadas durante o desenvolvimento da solução?**  
   (mesmo que não técnicas, como priorização ou simplificação):
   - Priorizar o fluxo principal (`/predict`) para garantir entrega do MVP
   - Validar os dados antes de chegar no ML
   - Implementar tratamento global de erros para padronização
   - Persistir dados para permitir métricas e estatísticas futuras

6. **Houve alguma alternativa considerada que acabou não sendo escolhida? Por quê?**  
   **Sim.** Inicialmente consideramos que as estatísticas agregadas fossem calculadas e retornadas diretamente pela API de ML. No entanto, optamos por gerar essas estatísticas a partir dos dados persistidos no banco de dados do back-end por três razões principais:
   - **Desacoplamento:** Separação clara de responsabilidades entre ML (previsões) e Back-End (dados operacionais)
   - **Performance:** Evitar sobrecarregar o serviço de ML com consultas analíticas
   - **Flexibilidade:** Permitir diferentes tipos de análises sem modificar a API de ML

### Funcionamento e Fluxos

7. **Como funciona o fluxo principal da solução do início ao fim?**  
   (o que acontece quando um usuário usa a aplicação):
   ```
   1. O usuário envia os dados do voo para o endpoint /predict
   2. A API valida os dados e aplica regras de negócio
   3. O service consome a API Python de forma reativa
   4. A previsão é retornada pelo modelo
   5. O back-end persiste o resultado no banco
   6. A resposta é enviada ao usuário
   ```
   Caso o usuário queira ver todas as previsões que já foram pesquisadas de forma agregada e com a porcentagem de atraso, basta acessar `/status`.

8. **O que acontece se algo der errado nesse fluxo?**  
   (ex.: erro de envio, dado inválido, falha de integração):
   - **Dados inválidos** → erro de validação com mensagem clara
   - **API Python indisponível** → erro tratado e resposta padronizada
   - **Erros inesperados** → capturados pelo GlobalExceptionHandler
   - Em todos os casos, a aplicação retorna respostas consistentes.

### Qualidade e Limitações

9. **Quais foram as principais limitações encontradas durante o hackathon?**  
   (tempo, escopo, conhecimento, ferramentas):
   - **Comunicação:** Alguns membros esperavam outros delegarem suas tarefas, resultando em momentos de baixa produtividade
   - **Tempo:** Janela de desenvolvimento limitada a 48 horas
   - **Recursos:** Limitação de infraestrutura para testes em larga escala
   - **Integração:** Sincronização entre times de Data Science e Back-End

10. **Quais pontos da solução vocês consideram mais frágeis ou que precisariam evoluir após o hackathon?**
    - Levar em consideração outros fatores para o retorno da probabilidade de atraso (condições climáticas, tráfego aéreo, etc.)
    - Implementar cache para previsões frequentes
    - Melhorar tratamento de falhas na integração com API de ML
    - Adicionar monitoramento e métricas operacionais

### Comunicação e Organização do Time

11. **Como o time se organizou para alinhar decisões e dividir responsabilidades durante o hackathon?**  
    A liderança utilizou **metodologia ágil** para organizar como seria feito o projeto, com reuniões diárias (dailies) e divisão clara de tarefas baseadas em skills específicos.

12. **Como as informações importantes sobre a solução foram compartilhadas entre os membros do time?**  
    Uso da plataforma de versionamento (GitHub) com branch strategy definida, documentação em READMEs, e reuniões frequentes para alinhamento técnico e de progresso.

### Perguntas Típicas de Banca (Encerramento)

13. **Por que essa solução é relevante em comparação com outras possíveis abordagens?**  
    Porque **separa claramente modelo, negócio e integração**, permitindo evolução independente, melhor manutenção e maior confiabilidade. Permite também a possibilidade de evolução sem muitas mudanças impactantes.

14. **Se vocês tivessem mais tempo, o que melhorariam ou expandiriam na solução?**:
    - Testes automatizados mais completos (unitários, integração, carga)
    - Novos endpoints analíticos para diferentes stakeholders
    - Mais features que impactam na possibilidade de atraso
    - Dashboard em tempo real com métricas operacionais
    - Sistema de alertas para atrasos críticos

15. **Quais aspectos dessa solução demonstram maior potencial de escala ou uso no mundo real?**
    - **Arquitetura desacoplada:** Permite escalar componentes independentemente
    - **Integração simples via API:** Fácil adoção por diferentes sistemas
    - **Persistência de dados:** Base para análises históricas e melhoria contínua
    - **Regras de negócio claras:** Manutenível e extensível
    - **Possibilidade de escalar o modelo de ML independentemente:** Pode evoluir sem impactar o back-end

---