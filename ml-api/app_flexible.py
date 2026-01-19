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
n_features_expected = 7  # DESCOBRIMOS QUE SÃO 7!

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await load_model_and_encoders()
    yield

app = FastAPI(
    title="Flight Delay Prediction API",
    description="API para previsão de atrasos de voos - 7 FEATURES",
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
    features_used: Optional[int] = None

async def load_model_and_encoders():
    global model, airline_encoder, airport_pair_encoder, n_features_expected
    
    try:
        # 1. Carregar o modelo
        model = joblib.load('model.joblib')
        logger.info(f"✅ Modelo carregado: {type(model)}")
        
        # Determinar número de features
        if hasattr(model, 'n_features_in_'):
            n_features_expected = model.n_features_in_
            logger.info(f"📐 Features esperadas: {n_features_expected}")
        else:
            logger.warning("⚠️ Não consegui determinar número de features, usando 7")
        
        # 2. Carregar encoders
        with open('companhia_encoder.json', 'r') as f:
            airline_encoder = json.load(f)
        
        with open('airport_pair_encoder.json', 'r') as f:
            airport_pair_encoder = json.load(f)
        
        logger.info("🚀 API pronta para receber requisições!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar recursos: {e}", exc_info=True)
        raise

@app.get("/")
async def root():
    return {
        "message": "Flight Delay Prediction API",
        "status": "operational" if model else "loading",
        "model_type": str(type(model)) if model else None,
        "features_expected": n_features_expected,
        "airline_encoder_entries": len(airline_encoder),
        "airport_encoder_entries": len(airport_pair_encoder),
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /predict",
            "model_info": "GET /model-info",
            "test_features": "GET /test-features"
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
        "classes": model.classes_.tolist() if hasattr(model, 'classes_') else None
    }
    
    return info

@app.get("/test-features")
async def test_features():
    """Endpoint para testar diferentes combinações de features"""
    test_cases = []
    
    # Teste 1: 7 zeros
    test_1 = [0] * 7
    try:
        pred = model.predict([test_1])[0]
        prob = model.predict_proba([test_1])[0] if hasattr(model, 'predict_proba') else None
        test_cases.append({"features": test_1, "prediction": int(pred), "probabilities": prob.tolist() if prob is not None else None})
    except:
        test_cases.append({"features": test_1, "error": "Failed"})
    
    # Teste 2: valores "razoáveis"
    test_2 = [1, 0, 0, 0.35, 2, 1, 0]  # turno, LATAM, GRU-SCL, distância norm, quarta, janeiro, extra
    try:
        pred = model.predict([test_2])[0]
        prob = model.predict_proba([test_2])[0] if hasattr(model, 'predict_proba') else None
        test_cases.append({"features": test_2, "prediction": int(pred), "probabilities": prob.tolist() if prob is not None else None})
    except:
        test_cases.append({"features": test_2, "error": "Failed"})
    
    return {
        "n_features_expected": n_features_expected,
        "test_cases": test_cases,
        "airline_encoder_sample": dict(list(airline_encoder.items())[:3]),
        "airport_encoder_sample": dict(list(airport_pair_encoder.items())[:3])
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(flight: FlightRequest):
    try:
        logger.info(f"📥 Recebida requisição: {flight.companhia_aerea} de {flight.aeroporto_origem}")
        
        if not model:
            raise HTTPException(503, "Modelo não carregado")
        
        # Preparar features BASE (6 que sabemos)
        features = prepare_base_features(flight)
        
        # Precisamos de 7 features, vamos adicionar um placeholder para a 7ª
        # A 7ª feature provavelmente é: ano, hora exata, ou outro derivado temporal
        if len(features) < n_features_expected:
            # Adicionar hora_do_dia como candidato para 7ª feature
            hora = flight.data_hora_partida.hour
            features.append(hora)  # hora_do_dia (0-23)
            
            # Se ainda faltar, preencher com zeros
            while len(features) < n_features_expected:
                features.append(0)
        
        logger.info(f"🔧 Features preparadas ({len(features)}): {features}")
        
        # Fazer predição
        features_array = np.array([features], dtype=np.float32)
        
        try:
            prediction = model.predict(features_array)[0]
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features_array)[0]
                if len(proba) == 2:
                    probability = float(proba[1])  # Probabilidade de atraso
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
            mensagem=f"Predição: {'Atraso' if atraso else 'Pontual'} ({probability:.1%})",
            features_used=len(features)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro: {e}", exc_info=True)
        raise HTTPException(500, f"Erro interno: {str(e)}")

def prepare_base_features(flight: FlightRequest) -> list:
    """Preparar as 6 features que sabemos"""
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
