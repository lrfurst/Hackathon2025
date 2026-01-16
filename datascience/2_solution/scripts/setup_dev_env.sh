#!/bin/bash
# Setup rápido para FlightOnTime Pro
echo "🚀 Iniciando setup do ambiente..."
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn scikit-learn pandas joblib
echo "✅ Ambiente pronto!"
