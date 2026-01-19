✈️ Flight On Time — Predição de Atrasos de Voos

📋 Visão Geral

O Flight On Time é uma aplicação full-stack de Inteligência Artificial voltada para o setor aéreo. A solução utiliza um modelo de Machine Learning treinado com dados históricos para prever a probabilidade de atraso de voos, oferecendo suporte à tomada de decisão antecipada.

O sistema foi projetado para ser modular, escalável e desacoplado, separando claramente as responsabilidades entre predição e orquestração de dados.

🏗️ Arquitetura do Sistema

A aplicação é composta por dois serviços independentes, que se comunicam via HTTP/JSON:

☕ Back-end Java (Spring Boot)
Responsável por:

Gerenciar requisições externas
Validar os dados de entrada
Persistir o histórico de consultas em banco de dados
Consumir a API de Machine Learning de forma reativa
🧠 API de Machine Learning (Python / FastAPI)
Responsável por:

Carregar o modelo treinado (.joblib)
Processar predições em tempo real
Retornar classificação e probabilidade de atraso
Essa separação garante flexibilidade para evolução independente do modelo e da API principal.

🚀 Tecnologias Utilizadas

Back-end (Java)
Java 21
Spring Boot 3
WebClient (consumo reativo de APIs)
Spring Data JPA (persistência)
JUnit 5
MockWebServer (testes)
Machine Learning (Python)
Python 3.10+
FastAPI
Uvicorn (ASGI Server)
Scikit-Learn
Joblib
Pandas
🛠️ Como Executar o Projeto

1️⃣ Pré-requisitos
JDK 21
Python 3.10 ou superior
Maven
2️⃣ Configurando o Serviço de Machine Learning (Python)
Navegue até a pasta da API Python e instale as dependências:

cd api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
A API de Machine Learning estará disponível em:

http://localhost:8000
3️⃣ Configurando o Back-end Java (Spring Boot)
Verifique se o arquivo src/main/resources/application.properties está configurado corretamente:

ml.api.base-url=http://localhost:8000
ml.api.predict-path=/predict
Execute a aplicação:

mvn spring-boot:run
Por padrão, a API Java será iniciada na porta 8080.

📊 Endpoints Principais

POST /predict (API Java — Porta 8080)
Envia os dados do voo para análise de atraso.

📥 Corpo da Requisição (JSON)
{
  "companhia": "AZ",
  "origem": "GRU",
  "destino": "SDU",
  "distancia_km": 360,
  "hora_dia": "manha",
  "dia_semana": 3
}
📤 Resposta de Sucesso (200 OK)
{
  "prediction": 1,
  "probability": 0.82,
  "avoided_cost": 100.76
}
prediction = 1 indica alta probabilidade de atraso
probability representa a confiança do modelo
🧪 Testes Unitários

O projeto possui cobertura de testes para:

Serviço de predição
Cálculo de estatísticas
Utilizamos o MockWebServer para simular a API Python, permitindo que os testes sejam executados sem a necessidade do serviço de Machine Learning estar ativo durante o build.

▶️ Executar os testes
mvn test
📝 Mapeamento de Dados (DTO)

Para garantir compatibilidade com a API Python sem necessidade de alterar o código do modelo, utilizamos o @JsonProperty no Java para alinhar os nomes dos campos.

Exemplo de Mapeamento
| Java DTO | JSON Enviado | Python (Leitura) | | ------------- | ------------------ | ------------------------------ | | origem | aeroporto_origem | data.get("aeroporto_origem") | | distanciaKm | distancia_km | data.get("distancia_km") |

Essa abordagem reduz acoplamento e protege o contrato entre serviços.

📌 Considerações Finais

O Flight On Time demonstra uma arquitetura moderna de integração entre Machine Learning e APIs corporativas, com foco em confiabilidade, testabilidade e evolução contínua do modelo preditivo.