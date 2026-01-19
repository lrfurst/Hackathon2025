#!/usr/bin/env python3
print("🔍 Teste do ambiente Python Anaconda")

import sys
print(f"Python: {sys.version}")
print(f"Executável: {sys.executable}")

# Testar imports
try:
    import joblib
    print("✅ joblib OK")
except ImportError as e:
    print(f"❌ joblib: {e}")

try:
    import sklearn
    print("✅ sklearn OK")
except ImportError as e:
    print(f"❌ sklearn: {e}")

# Verificar arquivo model.joblib
import os
print(f"\n📁 Diretório: {os.getcwd()}")
print("Arquivos:")
for f in sorted(os.listdir('.')):
    if f.endswith('.joblib') or f.endswith('.json') or f.endswith('.py'):
        print(f"  {f}")
