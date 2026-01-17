"""
Testes de Integração com Pytest - API Python de Previsão de Atrasos

Estes testes usam pytest para validar a integração de forma estruturada.
Focam em casos específicos e edge cases da API.

Execução:
    pytest tests/test_integration_pytest.py -v
    pytest tests/test_integration_pytest.py::TestContractValidation -v
"""

import pytest
import requests
import json
from typing import Dict, Any
from setup_integration_tests import IntegrationTestHelper, assert_valid_prediction_response, assert_validation_error


class TestContractValidation:
    """Testes de validação do contrato da API"""

    @pytest.mark.integration
    def test_api_contract_health_endpoint(self, api_client):
        """Valida contrato do endpoint /health"""
        result = api_client.session.get(f"{api_client.base_url}/health", timeout=api_client.timeout)

        # Deve retornar JSON
        assert result.status_code in [200, 503]
        if result.status_code == 200:
            response = result.json()
            assert isinstance(response, dict)
            assert "status" in response

    @pytest.mark.integration
    def test_api_contract_predict_endpoint(self, api_client, valid_payloads):
        """Valida contrato do endpoint /predict com payload válido"""
        payload = valid_payloads[0]

        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )

        assert result.status_code in [200, 503]
        if result.status_code == 200:
            response = result.json()
            assert_valid_prediction_response(response)

    @pytest.mark.integration
    def test_api_contract_error_responses(self, api_client, invalid_payloads):
        """Valida contrato de respostas de erro"""
        for payload in invalid_payloads[:3]:  # Testa primeiros 3 inválidos
            result = api_client.session.post(
                f"{api_client.base_url}/predict",
                json=payload,
                timeout=api_client.timeout
            )

            # Deve retornar erro de validação
            assert result.status_code in [400, 422, 503]
            if result.status_code in [400, 422]:
                try:
                    error_response = result.json()
                    assert_validation_error(error_response, result.status_code)
                except json.JSONDecodeError:
                    # Se não conseguir fazer parse do JSON, considera erro
                    pass


class TestPayloadValidation:
    """Testes específicos de validação de payload"""

    @pytest.mark.integration
    @pytest.mark.parametrize("missing_field", [
        "companhia_aerea",
        "aeroporto_origem",
        "aeroporto_destino",
        "data_hora_partida",
        "distancia_km"
    ])
    def test_missing_required_fields(self, api_client, missing_field):
        """Testa erro quando campo obrigatório está faltando"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        }

        # Remove campo obrigatório
        del payload[missing_field]

        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )

        assert result.status_code in [400, 422]

    @pytest.mark.integration
    @pytest.mark.parametrize("invalid_distance", [-100, 0, "invalid", None])
    def test_invalid_distance_values(self, api_client, invalid_distance):
        """Testa valores inválidos para distância"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": invalid_distance
        }

        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )

        assert result.status_code in [400, 422]

    @pytest.mark.integration
    @pytest.mark.parametrize("invalid_date", [
        "2024/01/15",  # Barra ao invés de hífen
        "15-01-2024",  # Formato brasileiro
        "2024-01-15",  # Sem hora
        "2024-13-15T14:30:00",  # Mês inválido
        "2024-01-32T14:30:00",  # Dia inválido
        "invalid-date"
    ])
    def test_invalid_date_formats(self, api_client, invalid_date):
        """Testa formatos inválidos de data"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": invalid_date,
            "distancia_km": 3980.0
        }

        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )

        assert result.status_code in [400, 422]


class TestPerformance:
    """Testes de performance da API"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_response_time_under_limit(self, api_client, valid_payloads):
        """Verifica se resposta está dentro do limite de tempo"""
        import time

        payload = valid_payloads[0]

        start_time = time.time()
        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )
        end_time = time.time()

        response_time = (end_time - start_time) * 1000  # ms

        # API deve responder em menos de 2 segundos
        assert response_time < 2000, f"Resposta muito lenta: {response_time:.1f}ms"

        # Se respondeu, deve ser sucesso
        if result.status_code == 200:
            assert_valid_prediction_response(result.json())

    @pytest.mark.integration
    def test_concurrent_requests(self, api_client, valid_payloads):
        """Testa múltiplas requisições simultâneas"""
        import concurrent.futures
        import time

        payload = valid_payloads[0]

        def make_request():
            return api_client.session.post(
                f"{api_client.base_url}/predict",
                json=payload,
                timeout=api_client.timeout
            )

        # Faz 5 requisições simultâneas
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(lambda _: make_request(), range(5)))
        end_time = time.time()

        total_time = (end_time - start_time) * 1000  # ms

        # Pelo menos uma deve ter sucesso
        success_count = sum(1 for r in results if r.status_code == 200)
        assert success_count > 0, "Nenhuma requisição teve sucesso"

        # Tempo total deve ser razoável (não sequencial)
        assert total_time < 5000, f"Requisições simultâneas muito lentas: {total_time:.1f}ms"


class TestConsistency:
    """Testes de consistência da API"""

    @pytest.mark.integration
    def test_deterministic_predictions(self, api_client, valid_payloads):
        """Verifica se previsões são determinísticas para mesmo input"""
        import time

        payload = valid_payloads[0]

        # Faz duas previsões idênticas com pequeno intervalo
        result1 = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )

        time.sleep(0.1)  # 100ms

        result2 = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )

        if result1.status_code == 200 and result2.status_code == 200:
            resp1 = result1.json()
            resp2 = result2.json()

            # Mesmo input deve dar mesma previsão
            assert resp1["atraso"] == resp2["atraso"], "Previsões não determinísticas"
            assert abs(resp1["probabilidade"] - resp2["probabilidade"]) < 0.001, "Probabilidades diferentes"


class TestErrorScenarios:
    """Testes de cenários de erro"""

    @pytest.mark.integration
    def test_malformed_json(self, api_client):
        """Testa envio de JSON malformado"""
        # Envia string ao invés de JSON
        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            data="not json",
            headers={"Content-Type": "application/json"},
            timeout=api_client.timeout
        )

        # Deve retornar bad request
        assert result.status_code in [400, 422]

    @pytest.mark.integration
    def test_wrong_content_type(self, api_client, valid_payloads):
        """Testa envio com Content-Type errado"""
        payload = valid_payloads[0]

        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            headers={"Content-Type": "text/plain"},
            timeout=api_client.timeout
        )

        # Deve retornar bad request ou aceitar mesmo assim
        assert result.status_code in [200, 400, 422]

    @pytest.mark.integration
    def test_very_large_payload(self, api_client):
        """Testa payload muito grande"""
        # Cria payload com dados enormes
        large_payload = {
            "companhia_aerea": "AA" * 1000,  # String muito longa
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        }

        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=large_payload,
            timeout=api_client.timeout
        )

        # Deve rejeitar ou aceitar (depende da implementação)
        assert result.status_code in [200, 400, 422, 413]  # 413 = Payload Too Large


class TestBoundaryConditions:
    """Testes de condições de borda"""

    @pytest.mark.integration
    @pytest.mark.parametrize("distance", [0.1, 0.01, 10000, 50000])
    def test_distance_boundaries(self, api_client, distance):
        """Testa valores limite de distância"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": distance
        }

        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )

        # Deve aceitar distâncias positivas
        if distance > 0:
            assert result.status_code in [200, 503]
        else:
            assert result.status_code in [400, 422]

    @pytest.mark.integration
    def test_future_dates(self, api_client):
        """Testa datas futuras"""
        from datetime import datetime, timedelta

        # Data 1 ano no futuro
        future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S")

        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": future_date,
            "distancia_km": 3980.0
        }

        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )

        # Deve aceitar datas futuras
        assert result.status_code in [200, 503]

    @pytest.mark.integration
    def test_past_dates(self, api_client):
        """Testa datas passadas"""
        payload = {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2020-01-15T14:30:00",  # Data passada
            "distancia_km": 3980.0
        }

        result = api_client.session.post(
            f"{api_client.base_url}/predict",
            json=payload,
            timeout=api_client.timeout
        )

        # Deve aceitar datas passadas (históricas)
        assert result.status_code in [200, 503]


# Testes que requerem configuração especial da API
class TestSpecialScenarios:
    """Testes que podem requerer configuração especial"""

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requer API configurada para simular timeout")
    def test_timeout_handling(self, api_client, valid_payloads):
        """Testa tratamento de timeout (requer configuração especial)"""
        # Este teste só funciona se a API estiver configurada para simular delay
        payload = valid_payloads[0]

        # Timeout muito curto para forçar timeout
        short_timeout_client = IntegrationTestHelper(timeout=0.001)

        result = short_timeout_client.session.post(
            f"{short_timeout_client.base_url}/predict",
            json=payload,
            timeout=short_timeout_client.timeout
        )

        # Deve dar timeout
        with pytest.raises(requests.exceptions.Timeout):
            result.raise_for_status()


if __name__ == "__main__":
    # Execução standalone
    print("Executando testes de integração com pytest...")

    # Executa apenas alguns testes básicos
    pytest.main([
        __file__,
        "-v",
        "-k", "test_api_contract",
        "--tb=short"
    ])
