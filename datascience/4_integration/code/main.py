from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="FlightOnTime Integration")

# Configuração de CORS (Essencial para integração)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "online", "service": "prediction-api"}

class PredictionRequest(BaseModel):
    companhia: str
    origem: str
    destino: str
    data_partida: str
    distancia_km: int
    hora_dia: str
    dia_semana: int

@app.post("/predict")
async def predict(flight: PredictionRequest):
    # Lógica de integração (mock inicial para teste)
    return {"previsao": "PONTUAL", "probabilidade": 0.15}
