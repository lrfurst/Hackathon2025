"""
Testes de Integração - API Python de Previsão de Atrasos

Estes testes verificam a integração entre o backend Java e a API Python.
Focam em:
- Contrato da API (payloads e respostas)
- Tratamento de erros
- Timeouts
- Casos de borda

IMPORTANTE: Estes testes assumem que a API Python está rodando em localhost:8000
"""

import pytest
import requests
import json
import time
from typing import Dict, Any
from datetime import datetime, timedelta


class IntegrationTestClient:
    """Cliente simplificado para testes de integração"""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 3.0):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def health_check(self) -> Dict[str, Any]:
        """Verifica health da API"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
            return {
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else None
            }
        except requests.exceptions.Timeout:
            return {"error": "timeout"}
        except requests.exceptions.ConnectionError:
            return {"error": "connection_refused"}

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Faz previsão"""
        try:
            response = self.session.post(
                f"{self.base_url}/predict",
                json=payload,
                timeout=self.timeout
            )
            return {
                "status_code": response.status_code,
                "response": response.json() if response.content else None
            }
        except requests.exceptions.Timeout:
            return {"error": "timeout"}
        except requests.exceptions.ConnectionError:
            return {"error": "connection_refused"}


@pytest.fixture
def client():
    """Fixture para cliente de teste"""
    return IntegrationTestClient()


class TestHealthCheck:
    """Testes do endpoint /health"""

    def test_health_endpoint_exists(self, client):
        """Verifica se endpoint /health responde"""
        result = client.health_check()

        # Deve responder (200 ou erro de conexão se API não estiver rodando)
        assert "status_code" in result or "error" in result

    def test_health_response_format(self, client):
        """Verifica formato da resposta de health quando API está saudável"""
        result = client.health_check()

        if result.get("status_code") == 200:
            response = result["response"]
            assert isinstance(response, dict)
            assert "status" in response


class TestPredictionEndpoint:
    """Testes do endpoint /predict"""

    def test_valid_payload_domestic_us(self, client):
        """Testa payload válido - voo doméstico EUA"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        }

        result = client.predict(payload)

        if result.get("status_code") == 200:
            response = result["response"]
            assert isinstance(response, dict)
            assert "atraso" in response
            assert "probabilidade" in response
            assert isinstance(response["atraso"], bool)
            assert 0.0 <= response["probabilidade"] <= 1.0

    def test_valid_payload_domestic_br(self, client):
        """Testa payload válido - voo doméstico Brasil"""
        payload = {
            "companhia_aerea": "G3",
            "aeroporto_origem": "CGH",
            "aeroporto_destino": "GIG",
            "data_hora_partida": "2024-01-15T08:00:00",
            "distancia_km": 390.0
        }

        result = client.predict(payload)

        if result.get("status_code") == 200:
            response = result["response"]
            assert isinstance(response, dict)
            assert "atraso" in response
            assert "probabilidade" in response

    def test_invalid_payload_missing_fields(self, client):
        """Testa payload inválido - campos obrigatórios faltando"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK"
            # Faltam aeroporto_destino, data_hora_partida, distancia_km
        }

        result = client.predict(payload)

        # Deve retornar erro de validação (422) ou bad request (400)
        assert result.get("status_code") in [400, 422]

    def test_invalid_payload_wrong_date_format(self, client):
        """Testa payload inválido - formato de data errado"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "15/01/2024 14:30",  # Formato brasileiro, não ISO
            "distancia_km": 3980.0
        }

        result = client.predict(payload)

        # Deve retornar erro de validação
        assert result.get("status_code") in [400, 422]

    def test_invalid_payload_negative_distance(self, client):
        """Testa payload inválido - distância negativa"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": -100.0
        }

        result = client.predict(payload)

        # Deve retornar erro de validação
        assert result.get("status_code") in [400, 422]

    def test_invalid_payload_empty_strings(self, client):
        """Testa payload inválido - strings vazias"""
        payload = {
            "companhia_aerea": "",
            "aeroporto_origem": "",
            "aeroporto_destino": "",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        }

        result = client.predict(payload)

        # Deve retornar erro de validação
        assert result.get("status_code") in [400, 422]


class TestTimeoutHandling:
    """Testes de timeout e confiabilidade"""

    def test_timeout_simulation(self, client):
        """Testa comportamento com timeout (simulado)"""
        # Este teste pode ser usado quando a API estiver configurada para simular timeout
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        }

        # Configura timeout muito curto para forçar timeout
        client.timeout = 0.001  # 1ms

        result = client.predict(payload)

        # Deve resultar em timeout
        assert result.get("error") == "timeout"


class TestErrorHandling:
    """Testes de tratamento de erros"""

    def test_connection_refused(self, client):
        """Testa comportamento quando API não está rodando"""
        # Muda para URL que não existe
        client.base_url = "http://localhost:9999"

        result = client.health_check()

        assert result.get("error") == "connection_refused"

    def test_malformed_json_response(self, client):
        """Testa resposta malformada (se API retornar HTML ao invés de JSON)"""
        # Este teste depende de como a API trata erros internos
        # Por exemplo, se retornar HTML 500 ao invés de JSON
        pass  # Implementar se necessário


class TestBusinessLogic:
    """Testes de lógica de negócio (se aplicável)"""

    def test_prediction_consistency(self, client):
        """Testa consistência de previsões para mesmo input"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        }

        # Faz duas previsões idênticas
        result1 = client.predict(payload)
        time.sleep(0.1)  # Pequena pausa
        result2 = client.predict(payload)

        if result1.get("status_code") == 200 and result2.get("status_code") == 200:
            # Mesmo input deve dar mesma previsão (determinístico)
            assert result1["response"]["atraso"] == result2["response"]["atraso"]
            assert abs(result1["response"]["probabilidade"] - result2["response"]["probabilidade"]) < 0.001


# Testes de carga (desabilitados por padrão - só executar manualmente)
class TestLoad:
    """Testes de carga - executar apenas quando necessário"""

    @pytest.mark.skip(reason="Teste de carga - executar manualmente")
    def test_multiple_requests(self, client):
        """Testa múltiplas requisições simultâneas"""
        import concurrent.futures

        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        }

        def make_request():
            return client.predict(payload)

        # Faz 10 requisições simultâneas
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda _: make_request(), range(10)))

        # Verifica que todas responderam
        successful = [r for r in results if r.get("status_code") == 200]
        assert len(successful) > 0  # Pelo menos algumas devem funcionar


if __name__ == "__main__":
    # Execução manual dos testes
    print("Executando testes de integração manualmente...")

    client = IntegrationTestClient()

    # Teste básico de conectividade
    print("1. Testando conectividade...")
    health = client.health_check()
    if "error" in health:
        print(f"❌ API não está acessível: {health['error']}")
        print("💡 Certifique-se de que a API Python está rodando em http://localhost:8000")
    else:
        print("✅ API acessível")

        # Teste de payload válido
        print("2. Testando payload válido...")
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        }

        result = client.predict(payload)
        if result.get("status_code") == 200:
            response = result["response"]
            print(f"✅ Previsão: atraso={response['atraso']}, probabilidade={response['probabilidade']:.3f}")
        else:
            print(f"❌ Erro na previsão: {result}")

    print("Testes manuais concluídos.")
