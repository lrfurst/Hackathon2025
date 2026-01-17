#!/bin/bash
echo "🚀 Iniciando ambiente de predição FlightOnTime..."
pip install -r requirements.txt
uvicorn datascience.4_integration.code.main:app --host 0.0.0.0 --port 8000 --reload
