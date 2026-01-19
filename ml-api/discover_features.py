import joblib
import json
import numpy as np

print("🔍 DESCOBRINDO AS 7 FEATURES DO MODELO")
print("=" * 60)

# Carregar modelo
model = joblib.load('model.joblib')
print(f"✅ Modelo: {type(model).__name__}")
print(f"📐 Número de features esperadas: {model.n_features_in_}")

# Verificar se temos feature names
if hasattr(model, 'feature_names_in_'):
    print(f"\n🎯 FEATURES NOMEADAS ENCONTRADAS!")
    print("A ordem EXATA é:")
    for i, name in enumerate(model.feature_names_in_):
        print(f"  {i}: {name}")
else:
    print(f"\n⚠️ O modelo não tem nomes de features armazenados")
    print("\n💡 Precisamos descobrir a ordem das features:")
    print("1. Veja no notebook de treinamento")
    print("2. Ou teste diferentes combinações")

# Carregar encoders
with open('companhia_encoder.json', 'r') as f:
    airline_encoder = json.load(f)

with open('airport_pair_encoder.json', 'r') as f:
    airport_encoder = json.load(f)

print(f"\n🔤 ENCODERS DISPONÍVEIS:")
print(f"  Companhias aéreas: {list(airline_encoder.keys())}")
print(f"  Pares de aeroportos: {list(airport_encoder.keys())}")

# Tentativa educada - possíveis 7 features baseado na análise
print(f"\n🤔 POSSÍVEIS 7 FEATURES:")
print("1. turno_operacional (0=Manhã, 1=Tarde/Noite)")
print("2. companhia_aerea_encoded (0, 1, 2, ...)")
print("3. airport_pair_encoded (0, 1, ...)")
print("4. distancia_km (ou normalizada)")
print("5. dia_da_semana (0-6)")
print("6. mes (1-12)")
print("7. ??? (qual poderia ser a 7ª feature?)")

print(f"\n💡 SUGESTÕES para a 7ª feature:")
print("   - ano (ou ano_mes)")
print("   - hora_do_dia (0-23)")
print("   - estação do ano")
print("   - feriado (0/1)")
print("   - dia_do_mes (1-31)")

# Testar com 7 features
print(f"\n�� Testando com 7 features (todos zeros)...")
test_7_features = [[0, 0, 0, 0, 0, 0, 0]]

try:
    prediction = model.predict(test_7_features)
    print(f"✅ Funcionou! Predição: {prediction[0]}")
    
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(test_7_features)
        print(f"📈 Probabilidades: {proba[0]}")
        
except Exception as e:
    print(f"❌ Ainda não: {e}")

print("\n" + "=" * 60)
print("🎯 PRÓXIMOS PASSOS:")
print("1. Verifique no notebook quais features foram usadas")
print("2. Ou me mostre o código de treinamento")
