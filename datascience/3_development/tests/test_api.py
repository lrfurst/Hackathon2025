# -*- coding: utf-8 -*-
"""Testes para FlightOnTime Pro API"""

import pytest
from fastapi.testclient import TestClient

try:
    import sys
    sys.path.insert(0, 'datascience/3_development')
    from api.main import app
    client = TestClient(app)
    API_AVAILABLE = True
except:
    API_AVAILABLE = False

@pytest.mark.skipif(not API_AVAILABLE, reason="API não disponível")
def test_health_check():
    """Testa health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

@pytest.mark.skipif(not API_AVAILABLE, reason="API não disponível")
def test_root():
    """Testa endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "api" in data

@pytest.mark.skipif(not API_AVAILABLE, reason="API não disponível")
def test_predict_valid():
    """Testa predição válida"""
    payload = {
        "companhia_aerea": "AA",
        "aeroporto_origem": "JFK",
        "aeroporto_destino": "LAX",
        "data_hora_partida": "2024-01-15T14:30:00",
        "distancia_km": 3980.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] in [0, 1]

@pytest.mark.skipif(not API_AVAILABLE, reason="API não disponível")
def test_predict_invalid_airline():
    """Testa airline inválida"""
    payload = {
        "companhia_aerea": "A",
        "aeroporto_origem": "JFK",
        "aeroporto_destino": "LAX",
        "data_hora_partida": "2024-01-15T14:30:00",
        "distancia_km": 3980.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400

@pytest.mark.skipif(not API_AVAILABLE, reason="API não disponível")
def test_metrics():
    """Testa métricas"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_predictions" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
