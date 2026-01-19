# 🎬 **Roteiro: FlightOnTime - Inteligência Preditiva na Aviação**

## 📋 **Roteiro Estruturado para Vídeo Demo**

### **⏰ Duração Total: 5-10 minutos**
**Foco:** Clareza, critério técnico e valor de negócio (não edição visual)

---

## 📊 **Estrutura do Roteiro**

### **1. 🎯 Introdução e Problema (00:00 - 01:30)**
```markdown
📌 Abertura:
• Apresentação pessoal: "Olá, sou [Nome], da Equipe 22 do Hackathon ONE II"
• Contexto: "Desenvolvemos o FlightOnTime no programa Oracle/No Country"

💸 O "Gancho" Financeiro:
• Dado de impacto: "Atrasos de voos custam 100,76 USD por minuto para companhias aéreas"
• Escala do problema: "Multiplique isso por milhares de voos diários..."

⚠️ O Problema Identificado:
• "Efeito Dominó": 15 minutos de atraso desregulam:
  - Tripulações
  - Manutenções
  - Conexões de passageiros
  - Operações aeroportuárias

👤 Persona do Usuário:
• "Analista de Operações"
• Trabalha com silos de dados desconexos
• Precisa de previsões para agir proativamente
```

---

### **2. 🔬 Processo e Metodologia (01:30 - 03:00)**
```markdown
🔄 Double Diamond Aplicado:
• Fase 1: Descobrir (Discover)
• Fase 2: Definir (Define)
• Fase 3: Desenvolver (Develop)
• Resultado: Solução centrada no humano e viável tecnicamente

📈 Estratégia de Dados Crítica:
• Decisão: PRIORIZAR RECALL (Revocação)
• Justificativa: "Identificamos que um Falso Negativo é 10x mais caro que um Falso Positivo"

🎯 Métricas do Modelo:
• Recall (Revocação): > 85%
• Objetivo: Capturar a maioria dos atrasos reais
• Trade-off aceitável com Precisão

🤝 Ensemble de Modelos:
• "Consenso de especialistas" (Voting/Stacking)
• Random Forest + XGBoost
• Combinação para robustez e acurácia
```

---

### **3. 🖥️ Demonstração Funcional (Compartilhamento de Tela) (03:00 - 06:30)**
```markdown
🏗️ Arquitetura Técnica:
• FastAPI (Data Science/Microserviço ML)
• Spring Boot (Backend/API Principal)
• Integração: REST API com JSON

🔧 API em Ação (Live Demo):
1. POST /predict (Previsão individual)
   • JSON de entrada: {companhia, origem, destino, data, distância}
   • JSON de saída: {previsao: "Atrasado", probabilidade: 0.78, fatores: [...]}

2. GET /stats (Estatísticas)
   • Dashboard de métricas acumuladas
   • Banco de dados com histórico

☁️ Infraestrutura OCI (Oracle Cloud):
• Instâncias Always Free (ARM Ampere A1)
• Banco de dados Autonomous
• Custo: ZERO para MVP
• Escalabilidade: Pronto para produção
```

---

### **4. 🎨 UX e Explicabilidade (06:30 - 08:30)**
```markdown
✨ Princípios de Design:
• Ação sobre Informação
• "Não apenas dizer 'atrasou', mas ajudar na decisão"
• Interface minimalista e funcional

🔍 SHAP (XAI - Explainable AI):
• O modelo explica o "porquê" da previsão:
  - "Horário de pico aumenta risco em 35%"
  - "Distância longa contribui com 20%"
  - "Companhia X tem histórico positivo"
• Gera confiança para o operador humano

⚡ Validação de Sucesso:
• Objetivo UX: < 3 cliques para análise
• Objetivo Tempo: < 2 minutos para decisão
• KPIs de usabilidade mensurados
```

---

### **5. 🚀 Conclusão e Visão de Futuro (08:30 - 10:00)**
```markdown
💰 ROI e Impacto de Negócio:
• Projeção: Redução de 15% no tempo médio de atraso
• Tradução: Milhões de USD economizados anualmente
• ROI calculado: 4:1 (R$ 4 economizados para cada R$ 1 investido)

👥 Trabalho em Equipe Profissional:
• Colaboração assíncrona eficiente
• Ferramentas: Jira + Git + Inbox da plataforma
• Comunicação: Simulando ambiente corporativo real

🌐 Encerramento:
• Convite: "Conheça nosso projeto no Showcase da No Country"
• Agradecimento: "Obrigado pela atenção e oportunidade"
• Call-to-action: "Estamos abertos para feedback e colaborações"
```

---

## ⚠️ **Regras de Ouro para o Vídeo (No Country)**

### **1. 🛠️ Ferramentas e Técnica:**
```markdown
🎥 Gravação:
• Ferramenta principal: Loom (ou similar)
• Configuração: Tela + câmera em balãozinho
• Qualidade: Áudio claro é mais importante que vídeo 4K

📹 Envio:
• Plataforma: YouTube
• Visibilidade: Público
• Link: Postar na seção de Entregáveis da plataforma

🎬 Produção:
• Foco: Evidência do processo e resultado funcional
• ❌ NÃO precisa de: Efeitos especiais, música épica, edição complexa
• ✅ PRECISA ter: Clareza, objetividade, demonstração real
```

### **2. ⏰ Prazos Críticos:**
```markdown
📅 Prazo de Gravação: Até 17/01/2026
⏱️ Prazo de Upload: Até 18/01 às 23:59 (GMT-3)
🚀 Demo Day: 20/01/2026 (09:30 - sua apresentação)
```

### **3. ✅ Checklist de Qualidade:**
```markdown
[ ] Áudio claro e sem ruído de fundo
[ ] Tela nítida (1080p recomendado)
[ ] Demonstração REAL da aplicação funcionando
[ ] Todos os 5 pilares cobertos:
    • Negócio (ROI)
    • Ciência de Dados (Recall/SHAP)
    • Engenharia (Spring/FastAPI/OCI)
    • Produto (UX/Personas)
    • Processo (Metodologia)
[ ] Duração: 5-10 minutos (ideal: 7-8 minutos)
[ ] Link YouTube configurado como Público
[ ] Link postado na plataforma No Country
```

---

## 🎯 **Pilares do Roteiro - Resumo Visual**

### **📊 Matriz de Cobertura:**
| Pilar | Tempo | Elementos-Chave | Objetivo |
|-------|-------|-----------------|----------|
| **Negócio** | 01:30 | ROI, custos, impacto | Mostrar valor financeiro |
| **Dados** | 01:30 | Recall, estratégia, métricas | Demonstrar critério técnico |
| **Engenharia** | 03:30 | Demo API, arquitetura, OCI | Provar funcionalidade |
| **Produto** | 02:00 | UX, SHAP, personas | Validar usabilidade |
| **Processo** | 01:30 | Metodologia, equipe | Evidenciar profissionalismo |

### **⏱️ Timeline Visual:**
```
00:00-01:30 🎯 PROBLEMA (Financeiro + Persona)
01:30-03:00 🔬 METODOLOGIA (Recall + Ensemble)
03:00-06:30 🖥️ DEMO (API + OCI + Funcionalidades)
06:30-08:30 🎨 UX (SHAP + Design Thinking)
08:30-10:00 🚀 CONCLUSÃO (ROI + Equipe + Call-to-action)
```

---

## 💡 **Dicas de Apresentação**

### **1. 🎤 Performance Vocal:**
```markdown
🗣️ Tom de Voz:
• Claro e confiante
• Pausas estratégicas
• Ênfase nos números-chave

📝 Roteiro:
• Não leia palavra por palavra
• Use tópicos como guia
• Pratique 2-3 vezes antes
```

### **2. 🖥️ Demonstração Técnica:**
```markdown
🔧 Preparação:
• Tenha dados de teste prontos
• Prepare cenários diferentes
• Teste TUDO antes de gravar

🎯 Foco na Tela:
• Zoom em áreas importantes
• Mostre inputs e outputs claramente
• Evite transições muito rápidas
```

### **3. 🎨 Storytelling:**
```markdown
📖 Estrutura Narrativa:
1. "Era uma vez um problema gigante..."
2. "Nossa equipe descobriu que..."
3. "Construímos uma solução que..."
4. "E os resultados são..."
5. "Imagine o futuro onde..."

🎭 Elementos Emocionais:
• Conecte com experiência pessoal (já teve voo atrasado?)
• Mostre o "antes" caótico vs "depois" organizado
• Humanize a tecnologia
```

---

## 🚨 **PONTOS CRÍTICOS DE ATENÇÃO**

### **✅ O QUE FAZER:**
```markdown
• Mostrar a APLICAÇÃO REAL funcionando
• Falar sobre DECISÕES (não apenas resultados)
• Demonstrar COLABORAÇÃO da equipe
• Incluir NÚMEROS CONCRETOS (ROI, métricas)
• Manter PROFISSIONALISMO do início ao fim
```

### **❌ O QUE EVITAR:**
```markdown
• Efeitos visuais exagerados
• Jargões técnicos sem explicação
• Demonstrações "fake" ou pré-gravadas
• Exceder 10 minutos
• Esquecer de mencionar a plataforma No Country
```

---

## 📋 **Checklist Final de Gravação**

### **🎬 Pré-Gravação:**
```
[ ] Script revisado e aprovado pela equipe
[ ] Ambiente de gravação silencioso
[ ] Iluminação adequada (se usar câmera)
[ ] Mic testado (áudio claro)
[ ] Aplicação funcionando perfeitamente
[ ] Dados de teste preparados
[ ] Tela organizada (sem ícones desnecessários)
```

### **🎥 Durante a Gravação:**
```
[ ] Iniciar com cumprimento e contexto
[ ] Seguir timeline (monitorar relógio)
[ ] Demonstrar funcionalidades REAIS
[ ] Mostrar código/interface quando relevante
[ ] Encerrar com call-to-action claro
```

### **📤 Pós-Gravação:**
```
[ ] Upload no YouTube como Público
[ ] Título: "FlightOnTime - Hackathon ONE II - Demo"
[ ] Descrição com links importantes
[ ] Postar link na plataforma No Country
[ ] Compartilhar com a equipe para review
```

---

## 🌟 **Benefícios deste Roteiro**

### **Para as Empresas Observadoras:**
```markdown
✅ Demonstra pensamento estratégico
✅ Mostra competência técnica real
✅ Evidencia trabalho em equipe
✅ Apresenta solução escalável
✅ Conecta tecnologia a negócio
```

### **Para sua Carreira:**
```markdown
🚀 Portfólio profissional de alto impacto
📈 Visibilidade no Showcase da No Country
🤝 Networking com empresas parceiras
💼 Evidência concreta de habilidades
🎯 Diferencial competitivo real
```

---

**🎬 Agora é com você!** Este roteiro cobre todos os aspectos técnicos, de negócio e processuais que as empresas observadoras procuram. Grave com confiança, mostre o trabalho incrível que sua equipe realizou, e boa sorte no Demo Day! 🚀

*Lembre-se: O objetivo não é perfeição, é EVIDÊNCIA de capacidade profissional.*