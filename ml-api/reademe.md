# Flight On Time - Interface de Teste da API

## 📋 Sobre o Projeto

Interface web para teste e validação da API de previsão de atrasos de voos da ANAC (Agência Nacional de Aviação Civil), desenvolvida seguindo o **Design System GOV.BR**.

## 🎯 Funcionalidades Principais

### 1. **Análise de Previsão de Atrasos**
- Formulário para inserção de dados do voo
- Geração de dados aleatórios com um clique
- Visualização da probabilidade de atraso com indicador colorido
- Detalhes das features processadas pelo modelo

### 2. **Testes da API**
- Testes individuais para todos os endpoints:
  - `/health` - Status do sistema
  - `/model` - Informações do modelo
  - `/predict` - Previsão de atrasos
  - `/docs` - Documentação da API
- Visualização de logs em tempo real
- Respostas da API formatadas em JSON

### 3. **Monitoramento do Sistema**
- Status da API em tempo real
- Badge de alerta apenas quando offline
- Tempo médio de resposta
- Verificação automática a cada 30 segundos

## 🏗️ Arquitetura da Interface

### Estrutura de Cards
1. **Análise de Voo** (Não colapsável)
   - Formulário principal
   - Botão de dados aleatórios
   - Análise de probabilidade

2. **Resultados + Testes** (Não colapsável)
   - Visualização de resultados
   - Testes dos endpoints
   - Logs do sistema

3. **Status do Sistema** (Colapsável)
   - Endpoints disponíveis
   - Informações técnicas
   - Monitoramento

4. **Informações Técnicas** (Colapsável)
   - Código de integração
   - Checklist de funcionamento

## 🎨 Design System GOV.BR

### Cores Oficiais
- **Azul Principal**: `#1351B4`
- **Amarelo Destaque**: `#FFCD07`
- **Verde Sucesso**: `#168821`
- **Vermelho Erro**: `#DC3545`

### Componentes
- Cards com bordas e sombras padronizadas
- Botões com altura mínima de 48px (acessibilidade)
- Formulários com validação visual
- Status badges coloridos

## 🔧 Tecnologias Utilizadas

- **HTML5** com semântica apropriada
- **CSS3** com Design System GOV.BR
- **JavaScript Vanilla** para interatividade
- **Font Awesome** para ícones
- **Google Fonts** (Rawline)

## 📱 Responsividade

- Layout adaptativo para mobile e desktop
- Reorganização de colunas em telas menores
- Elementos touch-friendly
- Tamanhos de fonte adequados

## ♿ Acessibilidade

- Contrastes de cores WCAG AA
- Navegação por teclado
- Labels descritivos
- Focus states visíveis
- Textos alternativos

## 🚀 Como Usar

### 1. **Análise de Voo**
```javascript
1. Preencha os dados do voo manualmente
2. OU clique em "Gerar Dados Aleatórios"
3. Clique em "Analisar Probabilidade"
4. Veja os resultados na seção de resultados
```

### 2. **Testes da API**
```javascript
1. Use os botões na seção "Testes da API"
2. Verifique as respostas no painel de resultados
3. Acompanhe os logs para debug
```

### 3. **Monitoramento**
```javascript
- Status da API aparece apenas quando offline
- Use "Verificar Status" para testes manuais
- "Simular Falha" para testes de resiliência
```

## 🔍 Recursos Especiais

### Expansão Inteligente
- Seções técnicas começam colapsadas
- Expansão automática em caso de erro
- Controle total do usuário sobre o que ver

### Feedback em Tempo Real
- Probabilidades com cores indicativas
- Logs atualizados automaticamente
- Alertas contextuais

### Simulação Realista
- Modelo de previsão com 7 features
- Probabilidades baseadas em dados históricos
- Simulação de falhas para testes

## 📊 Exemplo de Resposta da API

```json
{
  "atraso": true,
  "probabilidade": 0.815,
  "nivel_risco": "ALTO",
  "features_processadas": {
    "companhia_aerea": "GOL",
    "aeroporto_origem": "CNF",
    "aeroporto_destino": "BSB",
    "distancia_km": 600,
    "dia_da_semana": 1,
    "hora_do_dia": 8,
    "mes": 1
  }
}
```

## 🛠️ Configuração para Desenvolvimento

### Estrutura de Arquivos
```
flight-on-time-frontend/
├── index.html          # Interface principal
├── README.md           # Este documento
└── assets/             # (Opcional) Imagens/ícones
```

### Requisitos
- Navegador moderno (Chrome 90+, Firefox 88+, Edge 90+)
- Servidor HTTP local (opcional)
- API backend rodando em `localhost:8000`

### Execução
1. Abra o arquivo `index.html` no navegador
2. Para testes com API real, atualize as URLs no código
3. Use um servidor local para evitar problemas CORS

## 📈 Status do Projeto

✅ **Concluído** - Interface pronta para produção  
✅ **Design GOV.BR** - Padrões oficiais aplicados  
✅ **Responsivo** - Funciona em mobile e desktop  
✅ **Acessível** - WCAG AA atendido  
✅ **Testável** - Todos endpoints cobertos  