#!/usr/bin/env python3
"""
Mock API para Flight On Time - Sistema de Backup
==========================================

Este arquivo serve como backup para a API principal em caso de falhas.
Contém respostas pré-calculadas para demonstração.

Uso:
    python mock_api.py

A API mockada será executada em http://localhost:8001
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json
from datetime import datetime
import random

app = FastAPI(
    title="Flight On Time - Mock API",
    description="API de backup com respostas pré-calculadas para demonstração",
    version="1.0.0"
)

class PredictionRequest(BaseModel):
    """Modelo de entrada para predição"""
    companhia: str
    aeroporto_origem: str
    aeroporto_destino: str
    hora_partida: str
    distancia: float

class PredictionResponse(BaseModel):
    """Modelo de saída da predição"""
    prediction: int
    probability: float
    timestamp: str

# Respostas pré-calculadas para diferentes cenários
MOCK_RESPONSES = {
    "default": {
        "prediction": 1,  # Atraso
        "probability": 0.75,
        "timestamp": datetime.now().isoformat()
    },
    "on_time": {
        "prediction": 0,  # No horário
        "probability": 0.85,
        "timestamp": datetime.now().isoformat()
    },
    "high_delay": {
        "prediction": 1,  # Atraso
        "probability": 0.92,
        "timestamp": datetime.now().isoformat()
    }
}

# Exemplos de requests válidos
VALID_REQUESTS = [
    {
        "companhia": "LATAM",
        "aeroporto_origem": "GRU",
        "aeroporto_destino": "CGH",
        "hora_partida": "14:30",
        "distancia": 100.0
    },
    {
        "companhia": "GOL",
        "aeroporto_origem": "SDU",
        "aeroporto_destino": "BSB",
        "hora_partida": "08:15",
        "distancia": 850.5
    },
    {
        "companhia": "AZUL",
        "aeroporto_origem": "VCP",
        "aeroporto_destino": "POA",
        "hora_partida": "16:45",
        "distancia": 650.2
    }
]

@app.get("/")
async def root():
    """Endpoint raiz - informações da API"""
    return {
        "message": "Flight On Time - Mock API (Backup)",
        "status": "online",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Verificação de saúde",
            "/predict": "Predição de atraso (POST)",
            "/examples": "Exemplos de requests válidos"
        },
        "note": "Esta é uma API de backup com respostas pré-calculadas"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "mock_api",
        "version": "1.0.0"
    }

@app.get("/examples")
async def get_examples():
    """Retorna exemplos de requests válidos"""
    return {
        "examples": VALID_REQUESTS,
        "note": "Use estes exemplos para testar a API mockada"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_delay(request: PredictionRequest):
    """
    Predição de atraso de voo - versão mockada

    Esta é uma versão de backup que retorna respostas pré-calculadas
    baseadas em regras simples para demonstração.
    """
    try:
        # Validação básica dos campos
        if not request.companhia or not request.aeroporto_origem or not request.aeroporto_destino:
            raise HTTPException(status_code=400, detail="Campos obrigatórios faltando")

        if request.distancia <= 0:
            raise HTTPException(status_code=400, detail="Distância deve ser positiva")

        # Lógica mockada simples para escolher resposta
        if request.companhia.upper() == "GOL":
            response_data = MOCK_RESPONSES["on_time"]
        elif request.distancia > 800:
            response_data = MOCK_RESPONSES["high_delay"]
        else:
            response_data = MOCK_RESPONSES["default"]

        # Adiciona um pouco de variação aleatória para parecer real
        variation = random.uniform(-0.05, 0.05)
        response_data["probability"] = max(0.1, min(0.95, response_data["probability"] + variation))

        return PredictionResponse(**response_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/backup/status")
async def backup_status():
    """Status específico do sistema de backup"""
    return {
        "backup_system": "active",
        "responses_available": len(MOCK_RESPONSES),
        "valid_examples": len(VALID_REQUESTS),
        "last_updated": datetime.now().isoformat(),
        "note": "Sistema de backup operacional - pronto para uso em caso de falha da API principal"
    }

if __name__ == "__main__":
    print("🚀 Iniciando Flight On Time - Mock API (Backup)")
    print("📍 URL: http://localhost:8001")
    print("📋 Documentação: http://localhost:8001/docs")
    print("⚠️  NOTA: Esta é uma API de backup com respostas pré-calculadas")
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )