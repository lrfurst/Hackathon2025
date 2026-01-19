"""
Configurações globais do pytest para testes de integração.

Este arquivo é executado automaticamente pelo pytest e configura:
- Fixtures globais
- Configurações de relatório
- Hooks customizados
"""

import pytest
import requests
import os
from pathlib import Path


# Configurações de ambiente
API_BASE_URL = os.getenv("FLIGHT_DELAY_API_URL", "http://localhost:8000")
API_TIMEOUT = float(os.getenv("API_TIMEOUT", "3.0"))
JAVA_BACKEND_URL = os.getenv("JAVA_BACKEND_URL", "http://localhost:8080")

# Diretórios
PROJECT_ROOT = Path(__file__).parent.parent.parent
INTEGRATION_DIR = Path(__file__).parent.parent
EXAMPLES_DIR = INTEGRATION_DIR / "examples"


@pytest.fixture(scope="session", autouse=True)
def global_setup():
    """Setup global executado uma vez por sessão de teste"""
    print(f"\n🚀 Iniciando testes de integração")
    print(f"   API: {API_BASE_URL}")
    print(f"   Timeout: {API_TIMEOUT}s")
    print(f"   Java Backend: {JAVA_BACKEND_URL}")
    print(f"   Diretório: {INTEGRATION_DIR}")

    # Verificar se arquivos de exemplo existem
    payload_file = EXAMPLES_DIR / "payload_examples.json"
    response_file = EXAMPLES_DIR / "response_examples.json"

    if payload_file.exists():
        print("   ✅ Exemplos de payload disponíveis")
    else:
        print("   ⚠️ Exemplos de payload não encontrados")

    if response_file.exists():
        print("   ✅ Exemplos de resposta disponíveis")
    else:
        print("   ⚠️ Exemplos de resposta não encontrados")

    yield

    print("\n🏁 Sessão de testes finalizada")


@pytest.fixture(scope="session")
def api_status():
    """Verifica status da API no início da sessão"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5.0)
        return {
            "available": response.status_code == 200,
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else None
        }
    except requests.exceptions.ConnectionError:
        return {"available": False, "error": "connection_refused"}
    except requests.exceptions.Timeout:
        return {"available": False, "error": "timeout"}
    except Exception as e:
        return {"available": False, "error": str(e)}


@pytest.fixture(autouse=True)
def skip_if_api_unavailable(api_status):
    """Pula testes se API não estiver disponível"""
    if not api_status["available"]:
        pytest.skip(f"API não disponível: {api_status.get('error', 'desconhecido')}")


# Configuração de relatórios HTML (opcional)
def pytest_configure(config):
    """Configuração do pytest"""
    # Adicionar marcadores customizados
    config.addinivalue_line("markers", "integration: testes de integração")
    config.addinivalue_line("markers", "contract: testes de contrato da API")
    config.addinivalue_line("markers", "performance: testes de performance")
    config.addinivalue_line("markers", "slow: testes que demoram mais")
    config.addinivalue_line("markers", "java: testes que requerem backend Java")

    # Configurar relatório HTML se solicitado
    if config.getoption("--html"):
        config.option.htmlpath = INTEGRATION_DIR / "reports" / "integration_tests.html"


def pytest_collection_modifyitems(config, items):
    """Modificar itens coletados"""

    # Adicionar marcador 'integration' automaticamente
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

    # Contar testes por marcador
    integration_tests = [item for item in items if item.get_closest_marker("integration")]
    performance_tests = [item for item in items if item.get_closest_marker("performance")]
    slow_tests = [item for item in items if item.get_closest_marker("slow")]

    if integration_tests:
        print(f"📊 Coletados {len(integration_tests)} testes de integração")
    if performance_tests:
        print(f"📊 Coletados {len(performance_tests)} testes de performance")
    if slow_tests:
        print(f"📊 Coletados {len(slow_tests)} testes lentos")


def pytest_runtest_makereport(item, call):
    """Hook para modificar relatórios de teste"""
    if call.excinfo is not None:
        # Adicionar informações extras em caso de falha
        if "api" in item.fixturenames:
            # Se teste usa fixture da API, adicionar info de conectividade
            pass


# Utilitários para hooks
def pytest_addoption(parser):
    """Adicionar opções customizadas ao pytest"""
    parser.addoption(
        "--api-url",
        action="store",
        default=API_BASE_URL,
        help="URL base da API para testes"
    )

    parser.addoption(
        "--java-url",
        action="store",
        default=JAVA_BACKEND_URL,
        help="URL do backend Java para testes end-to-end"
    )

    parser.addoption(
        "--skip-performance",
        action="store_true",
        help="Pular testes de performance"
    )


def pytest_configure(config):
    """Configuração adicional baseada em opções"""
    # Configurar URLs baseadas em opções
    global API_BASE_URL, JAVA_BACKEND_URL
    API_BASE_URL = config.getoption("--api-url")
    JAVA_BACKEND_URL = config.getoption("--java-url")

    # Pular testes de performance se solicitado
    if config.getoption("--skip-performance"):
        # Isso será usado no collection_modifyitems
        pass


# Fixture para configuração customizada
@pytest.fixture
def test_config(request):
    """Fornece configuração de teste baseada em opções do pytest"""
    return {
        "api_url": request.config.getoption("--api-url"),
        "java_url": request.config.getoption("--java-url"),
        "skip_performance": request.config.getoption("--skip-performance")
    }