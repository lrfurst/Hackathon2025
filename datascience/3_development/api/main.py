# main.py - VERSÃO FUNCIONAL SIMPLES
import os
import joblib
import json
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

print("=" * 60)
print("🚀 INICIANDO FLIGHT ON TIME API")
print("=" * 60)

# 1. Configurar app FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Caminhos dos arquivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "logistic_regression_optimized_final.joblib")
COMPANHIA_ENC = os.path.join(BASE_DIR, "..", "models", "encoders", "companhia_encoder.json")
AIRPORT_ENC = os.path.join(BASE_DIR, "..", "models", "encoders", "airport_pair_encoder.json")

print(f"\n📂 Verificando arquivos...")
print(f"   Modelo: {'✅' if os.path.exists(MODEL_PATH) else '❌'} {MODEL_PATH}")
print(f"   Encoder companhia: {'✅' if os.path.exists(COMPANHIA_ENC) else '❌'} {COMPANHIA_ENC}")
print(f"   Encoder aeroportos: {'✅' if os.path.exists(AIRPORT_ENC) else '❌'} {AIRPORT_ENC}")

# 3. Carregar modelo
print(f"\n📦 Carregando modelo...")
try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modelo carregado com sucesso!")
    print(f"   Tipo: {type(model).__name__}")
    print(f"   Features esperadas: {model.n_features_in_}")
    print(f"   Classes: {model.classes_}")
    
    # Mostrar coeficientes
    if hasattr(model, 'coef_'):
        print(f"\n🔢 COEFICIENTES DO MODELO (ordem CORRETA):")
        for i, coef in enumerate(model.coef_[0]):
            significado = "🔴 REDUZ atraso" if coef < 0 else "🟢 AUMENTA atraso"
            print(f"   Feature [{i}]: {coef:+.6f} - {significado}")
            
except Exception as e:
    print(f"❌ ERRO ao carregar modelo: {e}")
    exit(1)

# 4. Carregar encoders
try:
    with open(COMPANHIA_ENC, 'r') as f:
        companhia_map = json.load(f)
    print(f"\n✅ Encoder de companhia: {len(companhia_map)} companhias")
    print(f"   Valores: {companhia_map}")
    
    with open(AIRPORT_ENC, 'r') as f:
        airport_map = json.load(f)
    print(f"\n✅ Encoder de aeroportos: {len(airport_map)} rotas")
    print(f"   Rotas: {airport_map}")
    
except Exception as e:
    print(f"❌ ERRO ao carregar encoders: {e}")
    companhia_map = {}
    airport_map = {}

# 5. Mapeamentos
hora_map = {"manha": 0, "tarde": 1, "noite": 2}

# 6. Modelo de dados para requisição
class FlightData(BaseModel):
    companhia: str
    aeroporto_origem: str
    aeroporto_destino: str
    distancia: float
    hora_partida: str
    dia_semana: int

# 7. Endpoints
@app.get("/")
def home():
    return {
        "api": "Flight On Time Prediction",
        "status": "online",
        "model": "logistic_regression_optimized_final",
        "features": model.n_features_in_,
        "endpoints": {
            "GET /": "Esta página",
            "GET /health": "Status da API",
            "GET /model": "Informações do modelo",
            "POST /predict": "Fazer predição"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "features_count": model.n_features_in_,
        "classes": model.classes_.tolist()
    }

@app.get("/model")
def model_info():
    """Informações detalhadas do modelo"""
    return {
        "model_info": {
            "type": str(type(model)),
            "n_features": model.n_features_in_,
            "classes": model.classes_.tolist(),
            "coefficients": [float(c) for c in model.coef_[0]],
            "intercept": float(model.intercept_[0]) if hasattr(model, 'intercept_') else None
        },
        "encoders": {
            "companhia": companhia_map,
            "aeroportos": airport_map,
            "hora": hora_map
        },
        "feature_order": [
            "[0] distancia_km_normalizada (distancia / 1000)",
            "[1] hora_partida (0=manhã, 1=tarde, 2=noite)",
            "[2] companhia_id",
            "[3] origem_id (sempre -1 no seu modelo)",
            "[4] destino_id (sempre -1 no seu modelo)",
            "[5] rota_id",
            "[6] dia_semana (0=domingo, 6=sábado)"
        ]
    }

@app.post("/predict")
def predict_flight(data: FlightData):
    """Prever se um voo terá atraso"""
    
    print(f"\n" + "=" * 50)
    print(f"📥 NOVA PREDIÇÃO:")
    print(f"   Companhia: {data.companhia}")
    print(f"   Rota: {data.aeroporto_origem} → {data.aeroporto_destino}")
    print(f"   Distância: {data.distancia} km")
    print(f"   Período: {data.hora_partida}")
    print(f"   Dia da semana: {data.dia_semana}")
    
    try:
        # Converter dados
        comp_id = companhia_map.get(data.companhia.upper(), -1)
        rota_key = f"{data.aeroporto_origem.upper()}-{data.aeroporto_destino.upper()}"
        rota_id = airport_map.get(rota_key, -1)
        hora_val = hora_map.get(data.hora_partida.lower(), 1)
        
        # Construir features na ORDEM CORRETA
        # Baseado nos seus testes: [distancia, hora, companhia, origem, destino, rota, dia]
        features = [
            float(data.distancia) / 1000.0,  # Feature 0: Distância normalizada
            float(hora_val),                  # Feature 1: Hora do dia
            float(comp_id),                   # Feature 2: ID da companhia
            -1.0,                             # Feature 3: Origem ID (fallback)
            -1.0,                             # Feature 4: Destino ID (fallback)
            float(rota_id),                   # Feature 5: ID da rota
            float(data.dia_semana)            # Feature 6: Dia da semana
        ]
        
        print(f"\n🔢 Features enviadas ao modelo:")
        feature_names = [
            "distancia_normalizada",
            "hora_partida",
            "companhia_id",
            "origem_id",
            "destino_id",
            "rota_id",
            "dia_semana"
        ]
        
        for i, (name, value) in enumerate(zip(feature_names, features)):
            print(f"   [{i}] {name}: {value}")
        
        # Fazer predição
        probs = model.predict_proba([features])[0]
        
        # Pela sua análise: classe 0 = ATRASO, classe 1 = PONTUAL
        prob_atraso = float(probs[0])   # Classe 0
        prob_pontual = float(probs[1])  # Classe 1
        
        print(f"\n📊 RESULTADO DA PREDIÇÃO:")
        print(f"   Probabilidade de ATRASO: {prob_atraso:.4f} ({prob_atraso*100:.1f}%)")
        print(f"   Probabilidade de PONTUAL: {prob_pontual:.4f} ({prob_pontual*100:.1f}%)")
        
        # Decisão (threshold 0.5)
        atraso = prob_atraso > 0.5
        
        # Explicação baseada nos coeficientes
        explanation = []
        coefs = model.coef_[0]
        
        # Analisar cada feature
        if coefs[0] > 0 and data.distancia > 1000:
            explanation.append("📏 Distância longa aumenta risco de atraso")
        elif coefs[0] < 0 and data.distancia > 1000:
            explanation.append("📏 Distância longa reduz risco de atraso")
            
        if coefs[1] > 0 and data.hora_partida == "noite":
            explanation.append("🌙 Período noturno aumenta risco")
        elif coefs[1] < 0 and data.hora_partida == "noite":
            explanation.append("🌙 Período noturno reduz risco")
            
        if coefs[2] < 0 and comp_id >= 0:
            explanation.append(f"✈️ Companhia {data.companhia} REDUZ risco (coef negativo)")
        elif coefs[2] > 0 and comp_id >= 0:
            explanation.append(f"✈️ Companhia {data.companhia} AUMENTA risco")
            
        if coefs[6] > 0 and data.dia_semana >= 5:
            explanation.append("📅 Final de semana aumenta risco")
        elif coefs[6] < 0 and data.dia_semana >= 5:
            explanation.append("📅 Final de semana reduz risco")
        
        # Calcular economia estimada
        avoided_cost = 0.0
        if atraso:
            avoided_cost = 100.0 + (prob_atraso * 50)
        
        # Preparar resposta
        result = {
            "voo": {
                "companhia": data.companhia,
                "rota": f"{data.aeroporto_origem} → {data.aeroporto_destino}",
                "distancia_km": data.distancia,
                "periodo": data.hora_partida,
                "dia_semana": data.dia_semana
            },
            "predicao": {
                "atraso": atraso,
                "probabilidade_atraso": round(prob_atraso, 4),
                "probabilidade_pontual": round(prob_pontual, 4),
                "confianca": round(max(prob_atraso, prob_pontual), 4)
            },
            "explicacao": explanation,
            "economia_estimada": round(avoided_cost, 2) if atraso else 0.0,
            "features_usadas": features,
            "metadata": {
                "modelo_hash": "d63f00c7",  # Do seu log
                "threshold": 0.5,
                "rota_encontrada": rota_id != -1,
                "companhia_encontrada": comp_id != -1
            }
        }
        
        print(f"   Decisão: {'⚠️  ATRASO' if atraso else '✅ PONTUAL'}")
        print(f"   Confiança: {max(prob_atraso, prob_pontual)*100:.1f}%")
        
        return result
        
    except Exception as e:
        print(f"❌ ERRO na predição: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "error": str(e),
            "atraso": False,
            "probabilidade_atraso": 0.0
        }

if __name__ == "__main__":
    import uvicorn
    
    print(f"\n" + "=" * 60)
    print(f"🌐 API PRONTA PARA USAR!")
    print("=" * 60)
    print(f"\n📡 Endpoints disponíveis:")
    print(f"   http://127.0.0.1:8000/")
    print(f"   http://127.0.0.1:8000/health")
    print(f"   http://127.0.0.1:8000/model")
    print(f"\n📤 Para testar uma predição:")
    print(f'   curl -X POST http://127.0.0.1:8000/predict \\')
    print(f'        -H "Content-Type: application/json" \\')
    print(f'        -d \'{{"companhia":"LATAM","aeroporto_origem":"GRU","aeroporto_destino":"CGH","distancia":50,"hora_partida":"manha","dia_semana":1}}\'')
    
    print(f"\n⚡ Iniciando servidor na porta 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)