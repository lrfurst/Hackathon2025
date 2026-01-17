# Usar uma imagem leve do Python
FROM python:3.9-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências de sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar o requirements.txt para o container
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do projeto para o container
COPY . .

# Expor a porta que o FastAPI usa
EXPOSE 8000

# Comando para rodar a API (usando o caminho modular que definimos)
CMD ["uvicorn", "datascience.4_integration.code.main:app", "--host", "0.0.0.0", "--port", "8000"]
