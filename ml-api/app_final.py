from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import joblib
import json
import numpy as np
from typing import Optional
import logging
import os
from contextlib import asynccontextmanager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
model = None
airline_encoder = {}
airport_pair_encoder = {}

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await load_model_and_encoders()
    yield

app = FastAPI(
    title="Flight Delay Prediction API",
    description="API para previsão de atrasos de voos - 7 FEATURES (hora_do_dia como 7ª)",
    version="1.0.0",
    lifespan=lifespan
)

# Modelo Pydantic para validação
class FlightRequest(BaseModel):
    companhia_aerea: str
    aeroporto_origem: str
    aeroporto_destino: str
    data_hora_partida: datetime
    distancia_km: float

class PredictionResponse(BaseModel):
    atraso: bool
    probabilidade: float
    status: str = "success"
    mensagem: Optional[str] = None
    features_explicadas: Optional[dict] = None

async def load_model_and_encoders():
    global model, airline_encoder, airport_pair_encoder
    
    try:
        # 1. Carregar o modelo
        model = joblib.load('model.joblib')
        logger.info(f"✅ Modelo carregado: {type(model)}")
        logger.info(f"📐 Features esperadas: {model.n_features_in_}")
        
        # 2. Carregar encoders
        with open('companhia_encoder.json', 'r') as f:
            airline_encoder = json.load(f)
        
        with open('airport_pair_encoder.json', 'r') as f:
            airport_pair_encoder = json.load(f)
        
        logger.info(f"📊 Encoders: {len(airline_encoder)} companhias, {len(airport_pair_encoder)} rotas")
        logger.info("🚀 API pronta para receber requisições!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar recursos: {e}", exc_info=True)
        raise

@app.get("/model")
def get_model_info():
    return {
        "name": "Flight Delay Predictor",
        "type": "Logistic Regression",
        "version": "1.0",
        "features_expected": 7,
        "status": "loaded",
        "available_endpoints": [
            {"path": "/predict", "method": "POST", "description": "Make predictions"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/docs", "method": "GET", "description": "Swagger UI"},
            {"path": "/model", "method": "GET", "description": "Model info"}
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if model else "unhealthy",
        "model_loaded": model is not None,
        "features_expected": model.n_features_in_ if model else 0,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model-info")
async def model_info():
    if not model:
        raise HTTPException(503, "Modelo não carregado")
    
    info = {
        "type": str(type(model)),
        "n_features_in": model.n_features_in_,
        "has_predict_proba": hasattr(model, 'predict_proba'),
        "classes": model.classes_.tolist(),
        "coeficientes": model.coef_[0].tolist() if hasattr(model, 'coef_') else None,
        "intercept": model.intercept_[0].tolist() if hasattr(model, 'intercept_') else None
    }
    
    return info

@app.post("/debug-features")
async def debug_features(flight: FlightRequest):
    """Endpoint para debug - mostra as features calculadas"""
    features = prepare_features(flight)
    
    return {
        "features": features,
        "features_named": {
            "turno_operacional": features[0],
            "companhia_aerea_encoded": features[1],
            "airport_pair_encoded": features[2],
            "distancia_normalizada": features[3],
            "dia_da_semana": features[4],
            "mes": features[5],
            "hora_do_dia": features[6]
        },
        "input_data": flight.dict(),
        "airline_encoded": airline_encoder.get(flight.companhia_aerea.upper(), "UNKNOWN"),
        "airport_pair": f"{flight.aeroporto_origem.upper()}-{flight.aeroporto_destino.upper()}"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(flight: FlightRequest):
    try:
        logger.info(f"📥 Recebida requisição: {flight.companhia_aerea} {flight.aeroporto_origem}->{flight.aeroporto_destino}")
        
        if not model:
            raise HTTPException(503, "Modelo não carregado")
        
        # Preparar features
        features = prepare_features(flight)
        
        # Verificar se temos o número correto
        if len(features) != model.n_features_in_:
            logger.error(f"❌ Features: {len(features)}, Esperado: {model.n_features_in_}")
            raise HTTPException(500, f"Número de features incorreto: {len(features)} != {model.n_features_in_}")
        
        logger.info(f"🔧 Features: {features}")
        
        # Fazer predição
        features_array = np.array([features], dtype=np.float32)
        
        try:
            prediction = model.predict(features_array)[0]
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features_array)[0]
                probability = float(proba[1])  # Probabilidade de atraso
            else:
                probability = 0.8 if prediction == 1 else 0.2
            
        except Exception as e:
            logger.error(f"❌ Erro no modelo: {e}")
            raise HTTPException(500, f"Erro no modelo: {str(e)}")
        
        atraso = bool(prediction)
        logger.info(f"📤 Resultado: Atraso={atraso}, Prob={probability:.1%}")
        
        # Explicação das features
        features_explained = {
            "turno_operacional": "Manhã" if features[0] == 0 else "Tarde/Noite",
            "companhia_aerea": f"{flight.companhia_aerea} (código: {features[1]})",
            "rota_aerea": f"{flight.aeroporto_origem}-{flight.aeroporto_destino} (código: {features[2]})",
            "distancia": f"{flight.distancia_km}km (normalizado: {features[3]:.3f})",
            "dia_da_semana": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"][features[4]],
            "mes": features[5],
            "hora_do_dia": f"{features[6]}h"
        }
        
        return PredictionResponse(
            atraso=atraso,
            probabilidade=probability,
            status="success",
            mensagem=f"Voo {'COM ATRASO' if atraso else 'PONTUAL'} ({probability:.1%} de probabilidade)",
            features_explicadas=features_explained
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro: {e}", exc_info=True)
        raise HTTPException(500, f"Erro interno: {str(e)}")

def prepare_features(flight: FlightRequest) -> list:
    """Preparar TODAS as 7 features na ordem correta"""
    features = []
    
    # 0. TURNO OPERACIONAL (0=Manhã, 1=Tarde/Noite)
    hora = flight.data_hora_partida.hour
    turno = 0 if hora < 12 else 1
    features.append(turno)
    
    # 1. COMPANHIA AÉREA CODIFICADA
    companhia = flight.companhia_aerea.upper()
    codigo_companhia = airline_encoder.get(companhia, airline_encoder.get("UNKNOWN", 0))
    features.append(codigo_companhia)
    
    # 2. PAR DE AEROPORTOS CODIFICADO
    rota = f"{flight.aeroporto_origem.upper()}-{flight.aeroporto_destino.upper()}"
    codigo_rota = airport_pair_encoder.get(rota, airport_pair_encoder.get("UNKNOWN", 0))
    features.append(codigo_rota)
    
    # 3. DISTÂNCIA NORMALIZADA (0-1)
    distancia = float(flight.distancia_km)
    distancia_norm = min(distancia / 10000.0, 1.0)  # Assume máximo 10,000km
    features.append(distancia_norm)
    
    # 4. DIA DA SEMANA (0=Segunda, 6=Domingo)
    dia_semana = flight.data_hora_partida.weekday()
    features.append(dia_semana)
    
    # 5. MÊS (1-12)
    mes = flight.data_hora_partida.month
    features.append(mes)
    
    # 6. HORA DO DIA (0-23) - NOSSA 7ª FEATURE!
    hora_do_dia = flight.data_hora_partida.hour
    features.append(hora_do_dia)
    
    return features

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
