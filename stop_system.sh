#!/bin/bash

echo "🛑 PARANDO SISTEMA FLIGHTONTIME"
echo "================================"

# Parar Python
if [ -f "ml-api/python.pid" ]; then
    kill $(cat ml-api/python.pid) 2>/dev/null
    echo "✅ API Python parada"
    rm -f ml-api/python.pid
fi

# Parar Java
if [ -f "backend/java.pid" ]; then
    kill $(cat backend/java.pid) 2>/dev/null
    echo "✅ Backend Java parado"
    rm -f backend/java.pid
fi

# Matar por porta também
kill $(lsof -ti:8000) 2>/dev/null && echo "✅ Processos porta 8000 finalizados"
kill $(lsof -ti:8080) 2>/dev/null && echo "✅ Processos porta 8080 finalizados"

echo "✅ Sistema parado com sucesso!"
