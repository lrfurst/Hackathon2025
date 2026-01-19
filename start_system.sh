#!/bin/bash

echo "🚀 SISTEMA FLIGHTONTIME - INICIANDO TUDO"
echo "========================================"

# Função para verificar porta
check_port() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

# 1. Iniciar API Python
echo "1. Iniciando API Python (porta 8000)..."
cd ml-api
if check_port 8000; then
    echo "   ✅ API Python já está rodando"
else
    python -m uvicorn app_final:app --host 0.0.0.0 --port 8000 > python.log 2>&1 &
    echo $! > python.pid
    echo "   ✅ API Python iniciada (PID: $(cat python.pid))"
fi

# 2. Iniciar Backend Java
echo -e "\n2. Iniciando Backend Java (porta 8080)..."
cd ../backend
if check_port 8080; then
    echo "   ✅ Backend Java já está rodando"
else
    mvn spring-boot:run > java.log 2>&1 &
    echo $! > java.pid
    echo "   ✅ Backend Java iniciado (PID: $(cat java.pid))"
    echo "   Aguarde 10 segundos para inicialização completa..."
    sleep 10
fi

# 3. Mostrar status
echo -e "\n📊 STATUS DOS SERVIÇOS:"
echo "========================"
if check_port 8000; then
    echo "✅ API Python:  http://localhost:8000"
    echo "   Health:     http://localhost:8000/health"
else
    echo "❌ API Python:  OFFLINE"
fi

if check_port 8080; then
    echo "✅ Backend Java: http://localhost:8080"
    echo "   Health:      http://localhost:8080/actuator/health"
    echo "   H2 Console:  http://localhost:8080/h2-console"
else
    echo "❌ Backend Java: OFFLINE"
fi

echo -e "\n📝 ENDPOINTS DISPONÍVEIS:"
echo "Python:"
echo "  GET  /health         - Status da API"
echo "  POST /predict        - Predição de atrasos"
echo ""
echo "Java:"
echo "  GET  /api/flights    - Listar predições"
echo "  POST /api/flights    - Nova predição"
echo ""
echo "🛑 Para parar: ./stop_system.sh"
echo "📋 Logs: tail -f ml-api/python.log backend/java.log"
