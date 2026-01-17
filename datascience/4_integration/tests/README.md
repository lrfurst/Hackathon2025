# Testes de Integração - API Python de Previsão de Atrasos

Esta pasta contém testes que validam a integração entre o backend Java e a API Python de previsão de atrasos.

## Estrutura dos Testes

```
tests/
├── __init__.py                 # Configurações do pacote de testes
├── conftest.py                 # Configurações globais do pytest
├── integration_tests.py        # Testes básicos e manuais
├── setup_integration_tests.py  # Fixtures e utilitários compartilhados
├── test_integration_pytest.py  # Testes estruturados com pytest
└── test_end_to_end.py          # Testes end-to-end simulados
```

## Pré-requisitos

1. **API Python rodando** em `http://localhost:8000`
2. **Python 3.8+** com dependências instaladas
3. **pytest** para execução dos testes

```bash
# Instalar dependências de teste
pip install pytest requests

# Ou se houver requirements
pip install -r ../requirements.integration.txt
```

## Como Executar

### Todos os Testes

```bash
# Executar todos os testes de integração
pytest -v

# Com relatório HTML
pytest --html=reports/integration_tests.html
```

### Testes Específicos

```bash
# Apenas testes de contrato da API
pytest test_integration_pytest.py::TestContractValidation -v

# Apenas testes de performance
pytest -m performance -v

# Pular testes lentos
pytest --skip-performance -v
```

### Testes Manuais

```bash
# Executar testes manuais (sem pytest)
python integration_tests.py
```

## Configuração de Ambiente

### Variáveis de Ambiente

```bash
# URL da API Python (padrão: http://localhost:8000)
export FLIGHT_DELAY_API_URL="http://localhost:8000"

# Timeout para chamadas da API (padrão: 3.0s)
export API_TIMEOUT="3.0"

# URL do backend Java para testes end-to-end (opcional)
export JAVA_BACKEND_URL="http://localhost:8080"
```

### Opções do Pytest

```bash
# Especificar URL da API
pytest --api-url="http://localhost:8000"

# Especificar URL do Java
pytest --java-url="http://localhost:8080"

# Pular testes de performance
pytest --skip-performance
```

## Tipos de Teste

### 🔗 Testes de Integração (`integration`)
- Validam comunicação entre Java e Python
- Verificam contrato da API
- Testam tratamento de erros

### 📋 Testes de Contrato (`contract`)
- Validam formato de payloads e respostas
- Verificam campos obrigatórios
- Testam validações

### ⚡ Testes de Performance (`performance`)
- Medem tempo de resposta
- Testam carga simultânea
- Verificam limites de timeout

### 🐌 Testes Lentos (`slow`)
- Testes que demoram mais para executar
- Geralmente de performance ou carga

### ☕ Testes Java (`java`)
- Testes que simulam comportamento do backend Java
- Requerem configuração especial

## Cenários de Teste

### ✅ Cenários de Sucesso
- Payload válido doméstico EUA
- Payload válido doméstico Brasil
- Resposta dentro do tempo limite
- Previsões determinísticas

### ❌ Cenários de Erro
- Campos obrigatórios faltando
- Formato de data inválido
- Distância negativa ou zero
- JSON malformado
- Timeout da API
- API offline

### 🔄 Cenários de Fallback
- API retorna erro 4xx/5xx
- Timeout na chamada
- Erro de conexão
- Resposta malformada

## Relatórios e Logs

### Relatório HTML
```bash
pytest --html=reports/integration_tests.html
```

### Logs Detalhados
```bash
pytest -v -s --log-cli-level=INFO
```

### Cobertura de Código
```bash
pytest --cov=integration_tests --cov-report=html
```

## Troubleshooting

### API não está rodando
```
❌ API não disponível: connection_refused
```
**Solução**: Inicie a API Python primeiro
```bash
cd ../api/
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Testes pulados
```
⚠️ API não disponível - pule testes de integração
```
**Solução**: Verifique se a API está saudável
```bash
curl http://localhost:8000/health
```

### Timeout nos testes
```
E           Failed: Timeout >3.0s
```
**Solução**: Aumente o timeout ou otimize a API
```bash
export API_TIMEOUT="5.0"
```

## Desenvolvimento

### Adicionar Novo Teste

1. **Escolher arquivo apropriado**:
   - `test_integration_pytest.py` para testes estruturados
   - `test_end_to_end.py` para fluxos completos
   - `integration_tests.py` para testes manuais

2. **Usar fixtures disponíveis**:
   - `api_client`: Cliente da API
   - `valid_payloads`: Payloads válidos
   - `invalid_payloads`: Payloads inválidos

3. **Adicionar marcadores**:
   ```python
   @pytest.mark.integration
   @pytest.mark.performance
   def test_novo_teste(self, api_client):
       pass
   ```

### Debug de Testes

```bash
# Executar apenas um teste específico
pytest test_integration_pytest.py::TestContractValidation::test_api_contract_health_endpoint -v -s

# Parar no primeiro erro
pytest -x

# Mostrar prints e logs
pytest -s
```

## Métricas de Qualidade

- **Cobertura**: >80% dos endpoints da API
- **Tempo médio**: <500ms por teste
- **Taxa de sucesso**: >95% quando API saudável
- **Fallback**: Sempre funciona quando API falha

## Integração com CI/CD

### GitHub Actions
```yaml
- name: Run Integration Tests
  run: |
    cd datascience/4_integration
    pytest --api-url="${{ secrets.API_URL }}"
```

### Docker
```bash
# Testar com API em container
docker run -d -p 8000:8000 my-api-image
pytest tests/
```