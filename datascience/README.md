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

## 🏗️ Arquitetura

A API segue o modelo de **arquitetura em camadas**, promovendo organização, desacoplamento e facilidade de manutenção.

### 📂 Estrutura de Pacotes
```text
br.com.flightOnTime
├── config
│   ├── PythonApiHealthIndicator
│   └── WebClientConfig
├── controller
│   └── PredictionController
├── dto
│   ├── ErroResponseDTO
│   ├── PredictionRequestDTO
│   ├── PredictionResponseDTO
│   ├── ValidandoCampos
│   └── ValidarCampos
├── entity
│   └── PredictionEntity
├── exception
│   └── PrevisaoNaoEncontrada
├── infra
│   └── ExcecoesGlobais
├── repository
│   └── PredictionRepository
└── service
    └── FlightOnTimeJavaApplication
```
---

## 📦 Descrição dos Pacotes

`controller`
- Contém os endpoints REST da aplicação.
- Responsável por receber requisições HTTP e retornar respostas.
  
`service`
- Camada de regras de negócio.
- Responsável pela integração com a API externa em Python que executa o modelo preditivo.
- Orquestra chamadas entre controller, repository e API externa.
  
`dto`
- Define os Data Transfer Objects (DTOs).
- Utilizados como entrada e saída da API, garantindo desacoplamento do modelo interno.
  
`entity`
- Representa as entidades do domínio.
- Mapeadas para o banco de dados utilizando JPA/Hibernate.
  
`repository`
- Camada de acesso a dados.
- Utiliza Spring Data JPA para persistência e consultas.

`config`
- Contém classes de configuração da aplicação.
- Inclui a configuração do WebClient, usado na comunicação com a API Python.
- Possui também um Health Check para verificar a disponibilidade da API Python.

`infra.exception`
- Camada responsável pelo tratamento global de erros.
- Possui um `@ControllerAdvice` para padronizar respostas de erro.
- Exemplo de exceção personalizada:
- `PredictionNotFound`: lançada quando uma previsão não é encontrada.
---

## 📍 Endpoint Principal

**POST** `/predict`

Envia os dados de um voo para o modelo preditivo e retorna a probabilidade de atraso.

#### 📥 Exemplo de Request
```json
{
  "companhia": "LATAM",
  "origem": "GRU",
  "destino": "SSA",
  "dataPartida": "10/01/2026",
  "distanciaKm": 1500
}
```
#### 📤 Exemplo de Response
```json
{
  "probabilidadeAtraso": 0.78,
  "previsao": "ATRASADO"
}
```
**GET**  `/stats`

Retorna estatísticas agregadas, com base exclusivamente nos dados armazenados no banco.

#### 📤 Exemplo de Response
```json
{
  "totalVoos": 120,
  "voosAtrasados": 45,
  "percentualAtraso": 37.5
}
```
---
## ✅ Validações de Entrada

A API utiliza Bean Validation (Jakarta Validation) para garantir a consistência dos dados recebidos, principalmente no endpoint /predict.

Campos validados no PredictionRequestDTO:
- `companhia`, `origem` e `destino`: Campos obrigatórios (`@NotBlank`).
- `data_partida`: Deve seguir o formato `yyyy-MM-dd` e não pode ser uma data retroativa.
- `distancia_km`: Deve ser obrigatoriamente um valor positivo (`@Positive`).
  
Em caso de dados inválidos, a API retorna um erro estruturado via `ErroResponseDTO`, facilitando a correção por parte do cliente.

---
## ⚠️ Tratamento de Erros
Erros de validação e exceções de negócio são tratados globalmente pelo  `GlobalExceptionHandler`.

As respostas de erro seguem um padrão unificado por meio do `ErroResponseDTO`, garantindo mensagens claras e consistentes para o consumidor da API.

---
## 🧪 Testes Automatizados

A aplicação conta com testes automatizados para garantir qualidade e confiabilidade.

### 📂 Estrutura de Testes
```text
src/test/java
└── br.com.flightOnTime
    ├── PredictionControllerTest
    └── PredictionServiceTest
```
- **PredictionControllerTest**: Valida o comportamento dos endpoints, códigos de status HTTP e o fluxo de validação de entrada.
- **PredictionServiceTest**: Foca nas regras de negócio e simula (mock) a integração com a API Python para garantir que o processamento interno esteja correto.
---
## 📘 Documentação com Swagger

A API utiliza Swagger (OpenAPI) para documentação e testes dos endpoints.

#### 📍 Acesso:

http://localhost:8080/swagger-ui/index.html

---

## 🛠️ Tecnologias Utilizadas

- Java 21
- Spring Boot  
- Spring Web
- Spring WebClient
- Spring Data JPA
- Swagger / OpenAPI
- Banco de Dados Relacional
- JUnit e Mockito

---

A arquitetura  foi pensada para ser **simples, escalável e de fácil manutenção**, facilitando futuras evoluções.
