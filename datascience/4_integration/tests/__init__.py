"""
Pacote de testes de integração para a API Python de previsão de atrasos.

Este pacote contém testes que validam a integração entre:
- Backend Java (consumidor)
- API Python (provedora)

Estrutura:
- integration_tests.py: Testes básicos e manuais
- test_integration_pytest.py: Testes estruturados com pytest
- setup_integration_tests.py: Configurações e fixtures compartilhadas
"""

# Configurações globais do pacote de testes
__version__ = "1.0.0"

# Imports convenientes para testes
from .setup_integration_tests import (
    IntegrationTestHelper,
    assert_valid_prediction_response,
    assert_validation_error
)

# Configurações padrão
DEFAULT_API_URL = "http://localhost:8000"
DEFAULT_TIMEOUT = 3.0