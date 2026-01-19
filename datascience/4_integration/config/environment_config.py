# datascience/4_integration/config/environment_config.py
"""
Configurações de ambiente para integração Java-Python
Este arquivo deve ser ajustado para cada ambiente (dev, staging, prod)
"""

import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class APIConfig:
    """Configurações da API Python"""
    
    # URLs
    base_url: str = "http://localhost:8000"
    health_endpoint: str = "/health"
    predict_endpoint: str = "/predict"
    metrics_endpoint: str = "/metrics"
    
    # Timeouts (em segundos)
    connect_timeout: float = 1.0
    read_timeout: float = 2.0
    total_timeout: float = 2.5
    
    # Retry configuration
    max_retries: int = 2
    retry_backoff_factor: float = 0.5
    
    # Headers
    default_headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.default_headers is None:
            self.default_headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "FlightDelayJavaClient/1.0"
            }


@dataclass
class JavaClientConfig:
    """Configurações do cliente Java"""
    
    # Timeouts (em milissegundos)
    java_connect_timeout_ms: int = 3000
    java_read_timeout_ms: int = 3000
    java_write_timeout_ms: int = 3000
    
    # Pool configuration
    max_connections: int = 100
    max_connections_per_route: int = 20
    keep_alive_duration_ms: int = 30000
    
    # Retry policy
    enable_retry: bool = True
    max_retry_attempts: int = 3
    retry_initial_interval_ms: int = 500
    retry_max_interval_ms: int = 2000
    retry_multiplier: float = 1.5
    
    # Circuit breaker
    enable_circuit_breaker: bool = True
    failure_threshold_percentage: int = 50
    wait_duration_ms: int = 30000
    permitted_calls_half_open: int = 3
    sliding_window_size: int = 10


@dataclass
class EnvironmentConfig:
    """Configuração completa por ambiente"""
    
    name: str  # dev, staging, prod
    api_config: APIConfig
    java_config: JavaClientConfig
    
    # Feature flags
    enable_caching: bool = False
    enable_logging: bool = True
    enable_metrics: bool = True
    enable_tracing: bool = False
    
    # Monitoring
    prometheus_endpoint: str = ""
    grafana_dashboard: str = ""
    alert_webhook: str = ""
    
    @classmethod
    def get_development_config(cls) -> 'EnvironmentConfig':
        """Configuração para ambiente de desenvolvimento"""
        return cls(
            name="development",
            api_config=APIConfig(
                base_url="http://localhost:8000",
                connect_timeout=1.0,
                read_timeout=2.0
            ),
            java_config=JavaClientConfig(
                java_connect_timeout_ms=3000,
                enable_circuit_breaker=False  # Desabilitado em dev para debugging
            ),
            enable_caching=False,
            enable_logging=True
        )
    
    @classmethod
    def get_staging_config(cls) -> 'EnvironmentConfig':
        """Configuração para ambiente de staging"""
        return cls(
            name="staging",
            api_config=APIConfig(
                base_url="https://api.flight-delay.staging.com",
                connect_timeout=1.5,
                read_timeout=2.0
            ),
            java_config=JavaClientConfig(
                java_connect_timeout_ms=3000,
                enable_circuit_breaker=True
            ),
            enable_caching=True,
            enable_metrics=True,
            prometheus_endpoint="http://prometheus.staging.com:9090"
        )
    
    @classmethod
    def get_production_config(cls) -> 'EnvironmentConfig':
        """Configuração para ambiente de produção"""
        return cls(
            name="production",
            api_config=APIConfig(
                base_url="https://api.flight-delay.prod.com",
                connect_timeout=1.0,
                read_timeout=1.5,  # Mais agressivo em produção
                total_timeout=2.0
            ),
            java_config=JavaClientConfig(
                java_connect_timeout_ms=2500,  # Mais agressivo em produção
                java_read_timeout_ms=2500,
                max_connections=200,
                enable_circuit_breaker=True
            ),
            enable_caching=True,
            enable_metrics=True,
            enable_tracing=True,
            prometheus_endpoint="http://prometheus.prod.com:9090",
            grafana_dashboard="https://grafana.prod.com/d/api-metrics",
            alert_webhook="https://hooks.slack.com/services/..."
        )


def get_current_config() -> EnvironmentConfig:
    """Obtém configuração baseada na variável de ambiente"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    config_map = {
        "dev": EnvironmentConfig.get_development_config,
        "development": EnvironmentConfig.get_development_config,
        "staging": EnvironmentConfig.get_staging_config,
        "prod": EnvironmentConfig.get_production_config,
        "production": EnvironmentConfig.get_production_config
    }
    
    if env in config_map:
        return config_map[env]()
    else:
        print(f"⚠️ Ambiente '{env}' não reconhecido, usando desenvolvimento")
        return EnvironmentConfig.get_development_config()


# Configuração atual (para importação direta)
current_config = get_current_config()

# Exemplo de uso:
if __name__ == "__main__":
    config = get_current_config()
    print(f"🎯 Ambiente: {config.name}")
    print(f"📡 API URL: {config.api_config.base_url}")
    print(f"⏱️ Timeout Python: {config.api_config.total_timeout}s")
    print(f"⏱️ Timeout Java: {config.java_config.java_read_timeout_ms}ms")
    print(f"🔌 Circuit Breaker: {'✅' if config.java_config.enable_circuit_breaker else '❌'}")