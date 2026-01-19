import joblib
import json
import os

print("🧪 TESTANDO CARREGAMENTO DO MODELO")
print("=" * 50)

# 1. Verificar se os arquivos existem
print("\n📁 Verificando arquivos...")
for f in ['model.joblib', 'companhia_encoder.json', 'airport_pair_encoder.json']:
    if os.path.exists(f):
        print(f"✅ {f} - {os.path.getsize(f):,} bytes")
    else:
        print(f"❌ {f} - NÃO ENCONTRADO!")

# 2. Carregar modelo
print("\n🤖 Carregando modelo...")
try:
    model = joblib.load('model.joblib')
    print(f"✅ Modelo carregado!")
    print(f"   Tipo: {type(model)}")
    
    # Verificar atributos importantes
    print("\n📊 Informações do modelo:")
    
    if hasattr(model, 'n_features_in_'):
        print(f"   n_features_in_: {model.n_features_in_}")
    
    if hasattr(model, 'feature_names_in_'):
        print(f"\n🔤 Features esperadas:")
        for i, feat in enumerate(model.feature_names_in_):
            print(f"   {i:2d}. {feat}")
    
    if hasattr(model, 'classes_'):
        print(f"\n🎯 Classes: {model.classes_}")
    
    # Testar predição
    print("\n🧪 Testando predição...")
    
    # Tentar determinar número de features
    if hasattr(model, 'n_features_in_'):
        n = model.n_features_in_
    else:
        n = 6  # Valor padrão baseado nos encoders
    
    print(f"   Usando {n} features para teste")
    
    # Criar dados de teste
    test_data = []
    for i in range(n):
        # Valores padrão baseados na análise
        if i == 0:  # turno
            test_data.append(1)
        elif i == 1:  # companhia
            test_data.append(0)
        elif i == 2:  # aeroportos
            test_data.append(0)
        elif i == 3:  # distância
            test_data.append(0.35)  # Normalizado
        elif i == 4:  # dia da semana
            test_data.append(2)
        elif i == 5:  # mês
            test_data.append(1)
        else:
            test_data.append(0)  # Padrão para features extras
    
    print(f"   Dados de teste: {test_data}")
    
    # Fazer predição
    try:
        prediction = model.predict([test_data])
        print(f"   ✅ Predição: {prediction[0]}")
        
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba([test_data])
            print(f"   📈 Probabilidades: {proba[0]}")
            
    except Exception as e:
        print(f"   ❌ Erro na predição: {e}")
        
except Exception as e:
    print(f"❌ Erro ao carregar modelo: {e}")

# 3. Carregar encoders
print("\n🔤 Carregando encoders...")
try:
    with open('companhia_encoder.json', 'r') as f:
        airline_encoder = json.load(f)
    print(f"✅ Companhia encoder: {len(airline_encoder)} entradas")
    print(f"   Exemplo: {dict(list(airline_encoder.items())[:3])}")
    
    with open('airport_pair_encoder.json', 'r') as f:
        airport_encoder = json.load(f)
    print(f"✅ Airport encoder: {len(airport_encoder)} pares")
    print(f"   Exemplo: {dict(list(airport_encoder.items())[:3])}")
    
except Exception as e:
    print(f"❌ Erro nos encoders: {e}")

print("\n" + "=" * 50)
print("✅ Teste completo!")
