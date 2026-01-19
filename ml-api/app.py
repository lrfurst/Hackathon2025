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
n_features_expected = 6

# Lifespan manager (substitui @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await load_model_and_encoders()
    yield
    # Shutdown (opcional)
    logger.info("Shutting down...")

app = FastAPI(
    title="Flight Delay Prediction API",
    description="API para previsão de atrasos de voos",
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

async def load_model_and_encoders():
    global model, airline_encoder, airport_pair_encoder, n_features_expected
    
    try:
        # 1. Carregar o modelo
        model_path = "model.joblib"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo não encontrado: {model_path}")
        
        model = joblib.load(model_path)
        logger.info(f"✅ Modelo carregado com sucesso!")
        
        # Determinar número de features
        if hasattr(model, 'n_features_in_'):
            n_features_expected = model.n_features_in_
        elif hasattr(model, 'feature_names_in_'):
            n_features_expected = len(model.feature_names_in_)
            
        logger.info(f"📐 Features esperadas: {n_features_expected}")
        
        # 2. Carregar encoders
        encoders = [
            ("companhia_encoder.json", "airline_encoder"),
            ("airport_pair_encoder.json", "airport_pair_encoder")
        ]
        
        for filename, var_name in encoders:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    if var_name == "airline_encoder":
                        airline_encoder = json.load(f)
                    else:
                        airport_pair_encoder = json.load(f)
                logger.info(f"✅ {filename}: {len(locals()[var_name])} entradas")
            else:
                logger.warning(f"⚠️ {filename} não encontrado")
        
        logger.info("🚀 API pronta para receber requisições!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar recursos: {e}", exc_info=True)
        raise

@app.get("/")
async def root():
    return {
        "message": "Flight Delay Prediction API",
        "status": "operational" if model else "loading",
        "model_loaded": model is not None,
        "features_expected": n_features_expected,
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /predict",
            "model_info": "GET /model-info",
            "encoders": "GET /encoders",
            "docs": "GET /docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if model else "unhealthy",
        "model_loaded": model is not None,
        "features_expected": n_features_expected,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model-info")
async def model_info():
    if not model:
        raise HTTPException(503, "Modelo não carregado")
    
    info = {
        "type": str(type(model)),
        "n_features_expected": n_features_expected,
        "has_predict_proba": hasattr(model, 'predict_proba'),
    }
    
    if hasattr(model, 'feature_names_in_'):
        info["feature_names"] = list(model.feature_names_in_)
    
    return info

@app.get("/encoders")
async def get_encoders():
    return {
        "airline_encoder": airline_encoder,
        "airport_pair_encoder": airport_pair_encoder
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(flight: FlightRequest):
    try:
        logger.info(f"📥 Recebida requisição: {flight.companhia_aerea} de {flight.aeroporto_origem}")
        
        if not model:
            raise HTTPException(503, "Modelo não carregado")
        
        # Preparar features
        features = prepare_features(flight)
        
        # Ajustar número de features se necessário
        if len(features) != n_features_expected:
            logger.warning(f"⚠️ Features: {len(features)}, Esperado: {n_features_expected}")
            if len(features) < n_features_expected:
                features.extend([0] * (n_features_expected - len(features)))
            else:
                features = features[:n_features_expected]
        
        # Fazer predição
        features_array = np.array([features], dtype=np.float32)
        
        try:
            prediction = model.predict(features_array)[0]
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features_array)[0]
                if len(proba) == 2:
                    probability = float(proba[1])
                else:
                    probability = 0.8 if prediction == 1 else 0.2
            else:
                probability = 0.8 if prediction == 1 else 0.2
            
        except Exception as e:
            logger.error(f"❌ Erro no modelo: {e}")
            # Fallback
            prediction = 0
            probability = 0.3
        
        atraso = bool(prediction)
        logger.info(f"📤 Resultado: Atraso={atraso}, Prob={probability:.1%}")
        
        return PredictionResponse(
            atraso=atraso,
            probabilidade=probability,
            status="success",
            mensagem=f"Predição: {'Atraso' if atraso else 'Pontual'} ({probability:.1%})"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro: {e}", exc_info=True)
        raise HTTPException(500, f"Erro interno: {str(e)}")

def prepare_features(flight: FlightRequest) -> list:
    """Preparar features baseado nos encoders"""
    features = []
    
    # 1. TURNO (0=Manhã, 1=Tarde/Noite)
    hora = flight.data_hora_partida.hour
    turno = 0 if hora < 12 else 1
    features.append(turno)
    
    # 2. COMPANHIA AÉREA
    companhia = flight.companhia_aerea.upper()
    codigo_companhia = airline_encoder.get(companhia, airline_encoder.get("UNKNOWN", 0))
    features.append(codigo_companhia)
    
    # 3. PAR DE AEROPORTOS
    rota = f"{flight.aeroporto_origem.upper()}-{flight.aeroporto_destino.upper()}"
    codigo_rota = airport_pair_encoder.get(rota, airport_pair_encoder.get("UNKNOWN", 0))
    features.append(codigo_rota)
    
    # 4. DISTÂNCIA (normalizada 0-1)
    distancia = float(flight.distancia_km)
    distancia_norm = min(distancia / 10000.0, 1.0)
    features.append(distancia_norm)
    
    # 5. DIA DA SEMANA (0-6)
    dia_semana = flight.data_hora_partida.weekday()
    features.append(dia_semana)
    
    # 6. MÊS (1-12)
    mes = flight.data_hora_partida.month
    features.append(mes)
    
    return features

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
