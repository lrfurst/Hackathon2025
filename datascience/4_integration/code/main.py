from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import time
import pandas as pd
import numpy as np

app = FastAPI(title="FlightOnTime Optimized API")

# 1. CARREGAMENTO GLOBAL (Singleton)
try:
    # O modelo é carregado aqui para que o /predict seja ultrarrápido (Task T4.1.4)
    MODEL_KIT = joblib.load('models/model_kit_final.joblib')
except:
    MODEL_KIT = None
    print("⚠️ ERRO: Arquivo 'models/model_kit_final.joblib' não encontrado!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    companhia: str
    origem: str
    destino: str
    data_partida: str
    distancia_km: int
    hora_dia: str
    dia_semana: int

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": MODEL_KIT is not None}

@app.post("/predict")
async def predict(flight: PredictionRequest):
    # --- INÍCIO DA LÓGICA DE PERFORMANCE ---
    start_time = time.perf_counter() 
    
    if not MODEL_KIT:
        raise HTTPException(status_code=503, detail="Modelo não disponível no servidor")

    try:
        # AQUI É ONDE A MÁGICA ACONTECE (Substituindo o Mock anterior):
        
        # 1. Tradução: Texto do Java -> Números do Modelo (Encoders)
        h_dia = MODEL_KIT['encoders']['hora_dia'].get(flight.hora_dia, 0)
        cia = MODEL_KIT['encoders']['companhia'].get(flight.companhia, 0)
        orig = MODEL_KIT['encoders']['origem'].get(flight.origem, 0)
        dest = MODEL_KIT['encoders']['destino'].get(flight.destino, 0)
        
        # 2. Organização dos dados para o Scikit-Learn
        input_df = pd.DataFrame([{
            'hora_dia': h_dia,
            'dia_semana': flight.dia_semana,
            'companhia': cia,
            'origem': orig,
            'destino': dest,
            'distancia_km': flight.distancia_km
        }])
        
        # 3. Execução da Predição (Usa o Scaler e o Modelo carregados no MODEL_KIT)
        input_scaled = MODEL_KIT['scaler'].transform(input_df)
        prob = MODEL_KIT['model'].predict_proba(input_scaled)[0, 1]
        
        # 4. Resultado final baseado no Threshold de lucro/recall
        veredito = "ATRASADO" if prob >= MODEL_KIT['threshold'] else "PONTUAL"
        
        # --- FIM DA LÓGICA DE PERFORMANCE ---
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        
        return {
            "previsao": veredito,
            "probabilidade": round(float(prob), 2),
            "performance": {
                "latency_ms": round(latency_ms, 2),
                "status": "p95_compliant" if latency_ms < 2000 else "slow"
            }
        }
    except Exception as e:
        # Se algo der errado no processamento, retornamos erro 500
        raise HTTPException(status_code=500, detail=str(e))
