"""
Setup para Testes de Integração

Este arquivo configura o ambiente para testes de integração entre
o backend Java e a API Python de previsão de atrasos.

Configurações:
- URLs da API
- Timeouts
- Fixtures compartilhadas
- Utilitários de teste
"""

import pytest
import requests
import json
import os
import time
from typing import Dict, Any, Generator
from pathlib import Path


# Configurações globais para testes
API_BASE_URL = os.getenv("FLIGHT_DELAY_API_URL", "http://localhost:8000")
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "3.0"))  # segundos
JAVA_BACKEND_URL = os.getenv("JAVA_BACKEND_URL", "http://localhost:8080")

# Caminhos para arquivos de exemplo
EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
PAYLOAD_EXAMPLES = EXAMPLES_DIR / "payload_examples.json"
RESPONSE_EXAMPLES = EXAMPLES_DIR / "response_examples.json"


class IntegrationTestHelper:
    """Helper para testes de integração"""

    def __init__(self, base_url: str = API_BASE_URL, timeout: float = API_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

        # Headers padrão
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "IntegrationTest/1.0"
        })

    def is_api_available(self) -> bool:
        """Verifica se a API está disponível"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5.0)
            return response.status_code == 200
        except:
            return False

    def wait_for_api(self, max_wait: int = 30) -> bool:
        """Aguarda API ficar disponível"""
        print(f"Aguardando API em {self.base_url} por até {max_wait}s...")

        for i in range(max_wait):
            if self.is_api_available():
                print("✅ API disponível!")
                return True
            time.sleep(1)

        print("❌ API não ficou disponível no tempo esperado")
        return False

    def load_payload_examples(self) -> Dict[str, Any]:
        """Carrega exemplos de payloads do arquivo JSON"""
        if PAYLOAD_EXAMPLES.exists():
            with open(PAYLOAD_EXAMPLES, 'r') as f:
                content = f.read()
                # Remove comentários do JSON (linhas começando com #)
                lines = [line for line in content.split('\n') if not line.strip().startswith('#')]
                clean_json = '\n'.join(lines)
                return json.loads(clean_json)
        return {}

    def get_valid_payloads(self) -> list:
        """Retorna lista de payloads válidos para teste"""
        examples = self.load_payload_examples()
        return examples.get("valid_payloads", [])

    def get_invalid_payloads(self) -> list:
        """Retorna lista de payloads inválidos para teste"""
        examples = self.load_payload_examples()
        return examples.get("invalid_payloads", [])


@pytest.fixture(scope="session")
def api_helper():
    """Fixture global para helper da API"""
    return IntegrationTestHelper()


@pytest.fixture(scope="session")
def api_available(api_helper):
    """Fixture que garante que a API está disponível antes dos testes"""
    if not api_helper.wait_for_api():
        pytest.skip("API não está disponível - pule testes de integração")
    return api_helper


@pytest.fixture
def api_client(api_available):
    """Fixture para cliente da API em cada teste"""
    return IntegrationTestHelper()


@pytest.fixture
def valid_payloads(api_helper):
    """Fixture com payloads válidos"""
    payloads = api_helper.get_valid_payloads()
    if not payloads:
        # Payload padrão se não conseguir carregar do arquivo
        payloads = [{
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        }]
    return payloads


@pytest.fixture
def invalid_payloads(api_helper):
    """Fixture com payloads inválidos"""
    payloads = api_helper.get_invalid_payloads()
    if not payloads:
        # Payloads inválidos padrão
        payloads = [
            {},  # Vazio
            {"companhia_aerea": "AA"},  # Campos faltando
            {
                "companhia_aerea": "AA",
                "aeroporto_origem": "JFK",
                "aeroporto_destino": "LAX",
                "data_hora_partida": "invalid-date",
                "distancia_km": 3980.0
            },  # Data inválida
            {
                "companhia_aerea": "AA",
                "aeroporto_origem": "JFK",
                "aeroporto_destino": "LAX",
                "data_hora_partida": "2024-01-15T14:30:00",
                "distancia_km": -100.0
            }  # Distância negativa
        ]
    return payloads


@pytest.fixture
def java_backend_available():
    """Fixture para verificar se backend Java está disponível (opcional)"""
    # Este fixture pode ser usado se quisermos testar integração end-to-end
    # com o backend Java também
    try:
        response = requests.get(f"{JAVA_BACKEND_URL}/health", timeout=5.0)
        return response.status_code == 200
    except:
        return False


# Configuração do pytest
def pytest_configure(config):
    """Configuração global do pytest"""
    # Marcadores customizados
    config.addinivalue_line("markers", "integration: marca testes de integração")
    config.addinivalue_line("markers", "slow: marca testes lentos")
    config.addinivalue_line("markers", "java: marca testes que requerem backend Java")


def pytest_collection_modifyitems(config, items):
    """Modifica itens de teste baseados em marcadores"""

    # Adiciona marcador 'integration' automaticamente para testes nesta pasta
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

    # Skip testes que requerem Java se não estiver disponível
    java_required = [item for item in items if item.get_closest_marker("java")]
    if java_required:
        # Verificar se Java backend está disponível
        try:
            response = requests.get(f"{JAVA_BACKEND_URL}/health", timeout=2.0)
            java_up = response.status_code == 200
        except:
            java_up = False

        if not java_up:
            for item in java_required:
                item.add_marker(pytest.mark.skip(reason="Backend Java não disponível"))


# Utilitários para testes
def assert_valid_prediction_response(response: Dict[str, Any]):
    """Valida estrutura de resposta de previsão"""
    assert isinstance(response, dict)
    assert "atraso" in response
    assert "probabilidade" in response
    assert isinstance(response["atraso"], bool)
    assert isinstance(response["probabilidade"], (int, float))
    assert 0.0 <= response["probabilidade"] <= 1.0


def assert_validation_error(response: Dict[str, Any], status_code: int):
    """Valida resposta de erro de validação"""
    assert status_code in [400, 422]
    if status_code == 422:
        assert "detail" in response or "errors" in response


def benchmark_api_call(func, *args, **kwargs) -> tuple:
    """Mede tempo de execução de chamada da API"""
    import time
    start = time.time()
    result = func(*args, **kwargs)
    duration = (time.time() - start) * 1000  # ms
    return result, duration


# Configurações de ambiente
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup global do ambiente de teste"""
    print(f"\n🧪 Configuração dos testes de integração:")
    print(f"   API URL: {API_BASE_URL}")
    print(f"   Timeout: {API_TIMEOUT}s")
    print(f"   Java Backend: {JAVA_BACKEND_URL}")
    print(f"   Examples dir: {EXAMPLES_DIR}")

    # Verificar se arquivos de exemplo existem
    if PAYLOAD_EXAMPLES.exists():
        print("   ✅ Arquivo de exemplos de payload encontrado")
    else:
        print("   ⚠️ Arquivo de exemplos de payload não encontrado")

    yield

    print("\n🏁 Testes de integração finalizados.")
