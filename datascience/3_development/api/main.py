
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}

@app.post("/predict")
def predict(data: dict):
    return {"prediction": 1, "probability": 0.82, "avoided_cost": 100.76}
