# 🎬 **Roteiro Atualizado: FlightOnTime - Predição de Atrasos de Voos**

## 📋 **Roteiro para Vídeo Demo (5 Minutos)**

### **⏰ Duração Total: 5 minutos**
**Foco:** Clareza, propósito e impacto do projeto (conforme regras do Hackathon)

---

## 📊 **Estrutura do Roteiro**

### **1. 🎯 Introdução e Problema (00:00 - 01:00)**
```markdown
📌 Abertura:
• "Olá, sou Ananda Matos, da Equipe H12-25-B-Equipo 22"
• "Apresento o Flight On Time desenvolvido no Hackathon ONE II"

💡 O Problema:
• "15% dos voos no Brasil sofrem atrasos"
• "Impacto operacional e financeiro para companhias aéreas"

🎯 Nossa Solução:
• "Sistema de Machine Learning para previsão de atrasos"
• "Backend Java + API Python FastAPI integrados"
```

---

### **2. 🔬 Demonstração da Solução (01:00 - 03:30)**
```markdown
🖥️ Compartilhamento de Tela:
• Interface web GOV.BR (flight-on-time-frontend)
• Formulário de análise de voo

🎯 Funcionalidades Principais:
1. **Análise em tempo real**:
   - Preenchimento manual ou dados aleatórios
   - Probabilidade de atraso com indicador visual

2. **Testes da API**:
   - Endpoints testáveis: /health, /predict, /model
   - Logs em tempo real para debugging

3. **Status do Sistema**:
   - Monitoramento automático
   - Alertas apenas quando offline

📊 Exemplo de Previsão:
• "Companhia: GOL, Origem: CNF, Destino: BSB"
• "Resultado: 81.5% probabilidade de atraso"
• "Nível de risco: ALTO"
```

---

### **3. 🏗️ Arquitetura Técnica (03:30 - 04:30)**
```markdown
🔧 Stack Tecnológica:
• **Frontend**: HTML/CSS/JS com Design System GOV.BR
• **Backend Java**: Spring Boot (porta 8080)
• **ML API**: Python FastAPI (porta 8000)

🔄 Fluxo de Dados:
1. Interface coleta dados do voo
2. Java Spring Boot valida e processa
3. FastAPI executa predição com Random Forest
4. Resultados retornam em JSON

📈 Modelo de Machine Learning:
• Random Forest Classifier (200 árvores)
• 12 features selecionadas
• Acurácia: ~85%
• Tempo de resposta: <200ms
```

---

### **4. 🚀 Conclusão e Impacto (04:30 - 05:00)**
```markdown
✅ O que Entregamos:
• Solução funcional e integrada
• Documentação completa nas 4 fases
• Interface profissional com padrões GOV.BR

🌟 Diferenciais:
• Integração Java-Python eficiente
• Design acessível e responsivo
• Código aberto e replicável

🙌 Agradecimento:
• "Obrigada à No Country e Oracle pela oportunidade"
• "Confiamos no trabalho colaborativo da equipe"
• "Estamos disponíveis no Showcase para conexões"
```

---

## ⚠️ **Regras do Hackathon Aplicadas**

### **✅ Requisitos Obrigatórios:**
```markdown
🎥 Vídeo Demo: 5 minutos (dentro do limite)
📊 Solução Funcional: Sistema operacional completo
👥 Colaboração: Trabalho em equipe documentado
⏱️ Prazos: Entrega dentro do cronograma
```

### **🎯 Foco no Essencial:**
```markdown
• Problema que resolve: Previsão de atrasos de voos
• Solução desenvolvida: Sistema full-stack de ML
• Impacto: Otimização operacional para aviação
• Evite detalhes técnicos excessivos
```

---

## 📋 **Checklist para Demo Day (20/01/2026)**

### **Pré-Apresentação:**
```
[ ] Inscrição no formulário (até 09/01)
[ ] Apresentador: Ananda Matos confirmada
[ ] Horário: 09:30 GMT-3
[ ] Slides preparados (máx 2 slides)
```

### **Durante a Apresentação:**
```
[ ] 5 minutos cronometrados
[ ] 1 porta-voz apenas
[ ] Foco em: problema → solução → impacto
[ ] Destaque do trabalho em equipe
[ ] Storytelling claro
```

### **Slides (Máximo 2):**
```
Slide 1:
• Logo Flight On Time
• Estatística: "15% dos voos atrasam"
• Arquitetura simplificada

Slide 2:
• Print da interface funcionando
• Métricas do modelo (85% acurácia)
• Links: GitHub, Demo, Documentação
```

---

## 💡 **Dicas de Apresentação**

### **Storytelling:**
```markdown
1. "Imagine poder prever atrasos de voos..."
2. "Nossa equipe construiu uma solução que..."
3. "Veja como funciona na prática..."
4. "Os resultados mostram que..."
5. "Esta experiência nos mostrou que..."
```

### **O que os Jurados Avaliam:**
```markdown
• Clareza na comunicação
• Propósito do projeto
• Impacto da solução
• Trabalho colaborativo
• Profissionalismo
```

---

## 🎬 **Gravação do Vídeo Demo**

### **Configuração:**
```markdown
🛠️ Ferramenta: Loom (sugerida) ou similar
🎥 Formato: Tela + webcam (opcional)
⏱️ Duração: 5 minutos
📤 Upload: YouTube (público)
🔗 Postar: Link na plataforma do Hackathon
```

### **Estrutura do Vídeo:**
```
00:00-01:00: Introdução e problema
01:00-03:30: Demo da aplicação (tela)
03:30-04:30: Explicação técnica resumida
04:30-05:00: Conclusão e agradecimentos
```

---

## ✨ **Mensagem Final**

**"Nosso projeto Flight On Time demonstra como dados e colaboração podem transformar operações críticas. Mais do que código, entregamos uma solução com propósito, impacto real e trabalho em equipe - exatamente o que as empresas buscam no mercado atual."**
