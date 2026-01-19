import joblib
import json
import os

print("🧪 TESTE SIMPLES DO MODELO")
print("=" * 50)

# Verificar arquivos
files = ['model.joblib', 'companhia_encoder.json', 'airport_pair_encoder.json']
for f in files:
    if os.path.exists(f):
        print(f"✅ {f} - {os.path.getsize(f)} bytes")
    else:
        print(f"❌ {f} - NÃO ENCONTRADO")

# Carregar modelo
try:
    model = joblib.load('model.joblib')
    print(f"\n✅ Modelo carregado!")
    print(f"   Tipo: {type(model)}")
    
    # Informações básicas
    if hasattr(model, 'n_features_in_'):
        print(f"   Features esperadas: {model.n_features_in_}")
    
    if hasattr(model, 'feature_names_in_'):
        print(f"\n🔤 Nomes das features:")
        for i, name in enumerate(model.feature_names_in_):
            print(f"   {i}: {name}")
    
    # Testar com 6 features (número provável)
    test_data = [[1, 0, 0, 0.35, 2, 1]]  # turno, companhia, aeroporto, distância, dia, mês
    
    try:
        prediction = model.predict(test_data)
        print(f"\n🧪 Predição teste: {prediction[0]}")
        
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(test_data)
            print(f"📈 Probabilidades: {proba[0]}")
    except Exception as e:
        print(f"\n⚠️ Erro na predição: {e}")
        
except Exception as e:
    print(f"\n❌ Erro ao carregar modelo: {e}")

# Carregar encoders
print("\n🔤 ENCODERS:")
try:
    with open('companhia_encoder.json', 'r') as f:
        airline = json.load(f)
    print(f"✅ Companhia: {len(airline)} entradas")
    
    with open('airport_pair_encoder.json', 'r') as f:
        airport = json.load(f)
    print(f"✅ Aeroportos: {len(airport)} pares")
    
except Exception as e:
    print(f"❌ Erro nos encoders: {e}")

print("\n" + "=" * 50)
