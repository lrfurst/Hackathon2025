# datascience/4_integration/api_client_example.py
"""
📡 EXEMPLO DE CLIENTE PARA API PYTHON DE PREVISÃO DE ATRASOS

Este arquivo demonstra como integrar com a API Python a partir de:
1. Backend Java (como referência)
2. Outros serviços Python
3. Testes manuais

🎯 OBJETIVO: Servir como referência para o time de backend Java
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FlightDelayAPIClient:
    """
    Cliente para API de previsão de atrasos de voos
    
    ⚠️ IMPORTANTE PARA O TIME JAVA:
    - Timeout máximo da API: 2 segundos
    - Timeout recomendado Java: 3 segundos
    - Formato data: ISO 8601 (YYYY-MM-DDTHH:MM:SS)
    - CORS configurado para: http://localhost:8080
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 2.5):
        """
        Inicializa o cliente da API
        
        Args:
            base_url: URL base da API Python (default: http://localhost:8000)
            timeout: Timeout em segundos (recomendado: 2.5s)
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        
        # Headers importantes para compatibilidade
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "FlightDelayJavaClient/1.0"
        })
        
        logger.info(f"✅ Cliente API inicializado: {base_url} (timeout: {timeout}s)")
    
    def check_health(self) -> Dict[str, Any]:
        """
        Verifica se a API está saudável e respondendo
        
        Returns:
            Dict com status e informações da API
        """
        try:
            start_time = time.time()
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            response_time = (time.time() - start_time) * 1000
            
            result = {
                "healthy": response.status_code == 200,
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "timestamp": datetime.now().isoformat()
            }
            
            if response.status_code == 200:
                result.update(response.json())
                logger.info(f"✅ API saudável - {response_time:.1f}ms")
            else:
                logger.warning(f"⚠️ API não saudável - Status: {response.status_code}")
                
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"⏰ Timeout na verificação de health ({self.timeout}s)")
            return {
                "healthy": False,
                "error": f"Timeout após {self.timeout} segundos",
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.ConnectionError:
            logger.error("🔌 Erro de conexão - API não encontrada")
            return {
                "healthy": False,
                "error": "Conexão recusada - API não está rodando",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"💥 Erro inesperado: {str(e)}")
            return {
                "healthy": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Obtém métricas de performance da API
        
        Returns:
            Dict com métricas da API
        """
        try:
            response = self.session.get(
                f"{self.base_url}/metrics",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "status": "error",
                    "status_code": response.status_code,
                    "message": "Falha ao obter métricas"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def predict_delay(self, flight_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz previsão de atraso para um voo
        
        📋 FORMATO ESPERADO DO PAYLOAD:
        {
            "companhia_aerea": "AA",                    # Código IATA (2-3 letras)
            "aeroporto_origem": "JFK",                 # Código IATA (3 letras)
            "aeroporto_destino": "LAX",                # Código IATA (3 letras)
            "data_hora_partida": "2024-01-15T14:30:00", # ISO 8601
            "distancia_km": 3980.0                     # Float positivo
        }
        
        Args:
            flight_data: Dicionário com dados do voo (formato acima)
            
        Returns:
            Dict com previsão e métricas de negócio
        """
        # Validação básica do payload
        validation_error = self._validate_flight_data(flight_data)
        if validation_error:
            return validation_error
        
        start_time = time.time()
        
        try:
            logger.info(f"✈️  Enviando previsão: {flight_data['aeroporto_origem']} → {flight_data['aeroporto_destino']}")
            
            response = self.session.post(
                f"{self.base_url}/predict",
                json=flight_data,
                timeout=self.timeout
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            # Log do tempo de resposta
            time_color = "🟢" if processing_time < 1000 else "🟡" if processing_time < 2000 else "🔴"
            logger.info(f"{time_color} Resposta em {processing_time:.1f}ms - Status: {response.status_code}")
            
            # Processa resposta baseada no status code
            if response.status_code == 200:
                result = response.json()
                result["_metadata"] = {
                    "processing_time_ms": round(processing_time, 2),
                    "request_timestamp": datetime.now().isoformat(),
                    "api_version": result.get("metadata", {}).get("model_version", "1.0.0")
                }
                return result
                
            elif response.status_code == 422:  # Validation error
                error_data = response.json()
                return {
                    "status": "validation_error",
                    "error": "Dados inválidos",
                    "details": error_data.get("detail", "Erro de validação"),
                    "processing_time_ms": round(processing_time, 2)
                }
                
            elif response.status_code == 400:  # Bad request
                return {
                    "status": "bad_request",
                    "error": "Requisição inválida",
                    "response_text": response.text,
                    "processing_time_ms": round(processing_time, 2)
                }
                
            else:
                return {
                    "status": "api_error",
                    "status_code": response.status_code,
                    "error": f"Erro da API: {response.status_code}",
                    "processing_time_ms": round(processing_time, 2)
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"⏰ TIMEOUT: API não respondeu em {self.timeout}s")
            return {
                "status": "timeout",
                "error": f"API não respondeu em {self.timeout} segundos",
                "processing_time_ms": self.timeout * 1000,
                "recommendation": "Aumente timeout no Java para 3s ou verifique API Python"
            }
            
        except requests.exceptions.ConnectionError:
            logger.error("🔌 ERRO DE CONEXÃO: API não encontrada")
            return {
                "status": "connection_error",
                "error": "Não foi possível conectar à API Python",
                "recommendation": "Verifique se a API está rodando: uvicorn app.main:app --host 0.0.0.0 --port 8000"
            }
            
        except Exception as e:
            logger.error(f"💥 ERRO INESPERADO: {str(e)}")
            return {
                "status": "unexpected_error",
                "error": str(e),
                "processing_time_ms": round((time.time() - start_time) * 1000, 2)
            }
    
    def _validate_flight_data(self, flight_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Valida o formato dos dados do voo
        
        Returns:
            Dict com erro ou None se válido
        """
        required_fields = [
            "companhia_aerea",
            "aeroporto_origem", 
            "aeroporto_destino",
            "data_hora_partida",
            "distancia_km"
        ]
        
        # Verifica campos obrigatórios
        missing_fields = [field for field in required_fields if field not in flight_data]
        if missing_fields:
            return {
                "status": "validation_error",
                "error": f"Campos obrigatórios faltando: {', '.join(missing_fields)}",
                "required_fields": required_fields
            }
        
        # Valida formato da data
        try:
            datetime.fromisoformat(flight_data["data_hora_partida"].replace('Z', '+00:00'))
        except ValueError:
            return {
                "status": "validation_error",
                "error": f"Formato de data inválido: {flight_data['data_hora_partida']}",
                "expected_format": "YYYY-MM-DDTHH:MM:SS (ex: 2024-01-15T14:30:00)"
            }
        
        # Valida distância
        try:
            distancia = float(flight_data["distancia_km"])
            if distancia <= 0:
                return {
                    "status": "validation_error",
                    "error": f"Distância deve ser positiva: {distancia}",
                    "field": "distancia_km"
                }
        except (ValueError, TypeError):
            return {
                "status": "validation_error", 
                "error": f"Distância deve ser número: {flight_data['distancia_km']}",
                "field": "distancia_km"
            }
        
        return None
    
    def batch_predict(self, flights: list) -> list:
        """
        Faz previsões para múltiplos voos
        
        Args:
            flights: Lista de dicionários com dados de voo
            
        Returns:
            Lista de resultados
        """
        results = []
        
        for i, flight in enumerate(flights, 1):
            logger.info(f"📦 Processando voo {i}/{len(flights)}...")
            result = self.predict_delay(flight)
            results.append({
                "flight_data": flight,
                "prediction": result
            })
            
            # Pequena pausa para não sobrecarregar a API
            if i < len(flights):
                time.sleep(0.1)
        
        return results


# ============================================================================
# EXEMPLOS PRÁTICOS DE USO
# ============================================================================

def exemplo_uso_simples():
    """Exemplo mínimo para integração rápida"""
    print("🚀 EXEMPLO DE USO SIMPLES")
    print("=" * 50)
    
    # 1. Cria cliente
    client = FlightDelayAPIClient()
    
    # 2. Verifica saúde da API
    health = client.check_health()
    if not health["healthy"]:
        print(f"❌ API não está saudável: {health.get('error', 'Unknown error')}")
        return
    
    print("✅ API está respondendo")
    
    # 3. Dados do voo
    flight_data = {
        "companhia_aerea": "AA",
        "aeroporto_origem": "JFK",
        "aeroporto_destino": "LAX", 
        "data_hora_partida": "2024-01-15T14:30:00",
        "distancia_km": 3980.0
    }
    
    # 4. Faz previsão
    result = client.predict_delay(flight_data)
    
    # 5. Processa resultado
    if result.get("status") == "success":
        pred = result["prediction"]
        metrics = result["business_metrics"]
        
        print(f"\n🎯 RESULTADO DA PREVISÃO:")
        print(f"   Atraso previsto: {'SIM' if pred['atraso'] else 'NÃO'}")
        print(f"   Probabilidade: {pred['probabilidade']:.1%}")
        print(f"   Custo evitado: R${metrics.get('custo_evitado', 0):.2f}")
        print(f"   Nível confiança: {metrics.get('confiança', 'N/A')}")
        print(f"   Tempo processamento: {result.get('_metadata', {}).get('processing_time_ms', 0):.1f}ms")
    else:
        print(f"\n❌ ERRO: {result.get('error', 'Erro desconhecido')}")


def exemplo_uso_avancado():
    """Exemplo completo com múltiplos voos e tratamento de erros"""
    print("\n🚀 EXEMPLO DE USO AVANÇADO")
    print("=" * 50)
    
    # Cria cliente com timeout customizado
    client = FlightDelayAPIClient(timeout=3.0)
    
    # Lista de voos para previsão (incluindo alguns inválidos)
    voos = [
        {
            "companhia_aerea": "AA",
            "aeroporto_origem": "JFK",
            "aeroporto_destino": "LAX",
            "data_hora_partida": "2024-01-15T14:30:00",
            "distancia_km": 3980.0
        },
        {
            "companhia_aerea": "DL", 
            "aeroporto_origem": "ATL",
            "aeroporto_destino": "ORD",
            "data_hora_partida": "2024-01-16T09:15:00",
            "distancia_km": 946.0
        },
        {
            "companhia_aerea": "G3",
            "aeroporto_origem": "GRU",
            "aeroporto_destino": "GIG",
            "data_hora_partida": "2024-01-17T18:45:00", 
            "distancia_km": 350.0
        },
        # Voo inválido (data mal formatada)
        {
            "companhia_aerea": "UA",
            "aeroporto_origem": "SFO",
            "aeroporto_destino": "EWR",
            "data_hora_partida": "2024/01/18 10:30",  # Formato errado
            "distancia_km": 4150.0
        }
    ]
    
    print(f"📊 Processando {len(voos)} voos...\n")
    
    resultados = client.batch_predict(voos)
    
    # Análise dos resultados
    sucessos = 0
    erros = 0
    
    for i, resultado in enumerate(resultados, 1):
        voo = resultado["flight_data"]
        pred = resultado["prediction"]
        
        origem = voo["aeroporto_origem"]
        destino = voo["aeroporto_destino"]
        
        if pred.get("status") == "success":
            sucessos += 1
            atraso = pred["prediction"]["atraso"]
            probabilidade = pred["prediction"]["probabilidade"]
            
            print(f"{i}. ✈️  {origem}→{destino}: {'🔴 ATRASO' if atraso else '🟢 NO HORÁRIO'} ({probabilidade:.1%})")
        else:
            erros += 1
            print(f"{i}. ❌ {origem}→{destino}: ERRO - {pred.get('error', 'Desconhecido')}")
    
    print(f"\n📈 RESUMO: {sucessos} sucessos, {erros} erros")


def exemplo_para_time_java():
    """
    Exemplo específico para referência do time Java
    Mostra o fluxo completo que deve ser implementado em Java
    """
    print("\n👨‍💻 EXEMPLO PARA TIME JAVA (COMO REFERÊNCIA)")
    print("=" * 50)
    
    print("""
    📋 FLUXO QUE DEVE SER IMPLEMENTADO EM JAVA:
    
    1. ✅ Inicializar cliente HTTP com timeout de 3s
    2. ✅ Configurar headers:
       - Content-Type: application/json
       - Accept: application/json
    3. ✅ Preparar payload JSON:
       {
         "companhia_aerea": "String (2-3 letras)",
         "aeroporto_origem": "String (3 letras)", 
         "aeroporto_destino": "String (3 letras)",
         "data_hora_partida": "String (ISO 8601)",
         "distancia_km": "Float"
       }
    4. ✅ Fazer requisição POST para:
       http://localhost:8000/predict
    5. ✅ Tratar respostas:
       - 200: Processar JSON de resposta
       - 400/422: Tratar erro de validação
       - Timeout: Fallback para regras de negócio
       - Outros erros: Log e retry/fallback
    6. ✅ Processar resultado:
       - prediction.atraso (boolean)
       - prediction.probabilidade (float 0-1)
       - business_metrics.custo_evitado (float)
    """)
    
    print("\n⚙️ CONFIGURAÇÕES CRÍTICAS PARA JAVA:")
    print("""
    - Timeout Java: 3000ms (3 segundos)
    - Timeout Python: 2000ms (2 segundos)
    - Formato data: ISO 8601 (ex: 2024-01-15T14:30:00)
    - CORS: Configurado para http://localhost:8080
    - Fallback: Implementar regras simples se API falhar
    """)
    
    # Demonstra o payload/resposta esperado
    print("\n📤 PAYLOAD DE EXEMPLO:")
    exemplo_payload = {
        "companhia_aerea": "AA",
        "aeroporto_origem": "JFK",
        "aeroporto_destino": "LAX",
        "data_hora_partida": "2024-01-15T14:30:00",
        "distancia_km": 3980.0
    }
    print(json.dumps(exemplo_payload, indent=2))
    
    print("\n📥 RESPOSTA DE EXEMPLO:")
    exemplo_resposta = {
        "status": "success",
        "prediction": {
            "atraso": True,
            "probabilidade": 0.78
        },
        "business_metrics": {
            "custo_evitado": 1250.50,
            "confiança": "ALTA"
        },
        "metadata": {
            "model_version": "1.0.0",
            "processing_time_ms": 185.5
        }
    }
    print(json.dumps(exemplo_resposta, indent=2))


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    """
    Ponto de entrada principal
    Execute: python api_client_example.py
    """
    
    print("=" * 60)
    print("📡 CLIENTE DE EXEMPLO - API PYTHON DE PREVISÃO DE ATRASOS")
    print("=" * 60)
    
    try:
        # Exemplo 1: Uso simples
        exemplo_uso_simples()
        
        # Exemplo 2: Uso avançado (descomente para testar)
        # exemplo_uso_avancado()
        
        # Exemplo 3: Para time Java
        exemplo_para_time_java()
        
        print("\n" + "=" * 60)
        print("✅ EXEMPLOS COMPLETADOS COM SUCESSO")
        print("=" * 60)
        
        print("\n📌 PRÓXIMOS PASSOS PARA INTEGRAÇÃO:")
        print("1. Teste com: python api_client_example.py")
        print("2. Verifique se API está rodando na porta 8000")
        print("3. Passe este arquivo para o time Java como referência")
        print("4. Use os exemplos de payload/resposta acima")
        
    except KeyboardInterrupt:
        print("\n\n👋 Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro durante execução: {str(e)}")
        import traceback
        traceback.print_exc()