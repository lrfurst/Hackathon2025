import joblib
import json
import numpy as np

print("🔍 TESTANDO DIFERENTES HIPÓTESES PARA A 7ª FEATURE")
print("=" * 60)

# Carregar modelo e encoders
model = joblib.load('model.joblib')
with open('companhia_encoder.json', 'r') as f:
    airline_encoder = json.load(f)
with open('airport_pair_encoder.json', 'r') as f:
    airport_encoder = json.load(f)

print(f"Modelo: {type(model).__name__}")
print(f"Features esperadas: {model.n_features_in_}")
print(f"Coeficientes shape: {model.coef_.shape}")
print(f"Coeficientes: {model.coef_[0]}")
print(f"Intercept: {model.intercept_[0]}")

# Base das primeiras 6 features (que sabemos)
base_features = [1, 0, 0, 0.35, 2, 1]  # turno, LATAM, GRU-SCL, distância norm, quarta, janeiro

print(f"\n🧪 TESTANDO DIFERENTES VALORES PARA A 7ª FEATURE:")
print(f"Base (primeiras 6): {base_features}")

# Hipóteses para a 7ª feature
hypotheses = [
    ("hora_do_dia (14)", 14),
    ("dia_do_mes (15)", 15),
    ("ano (2024)", 2024),
    ("ano_normalizado (0.5)", 0.5),
    ("estação (2=verão)", 2),
    ("feriado (0)", 0),
    ("feriado (1)", 1),
    ("semana_do_ano (3)", 3),
    ("trimestre (1)", 1),
]

for name, value in hypotheses:
    test_features = base_features + [value]
    try:
        prediction = model.predict([test_features])[0]
        proba = model.predict_proba([test_features])[0]
        print(f"  {name:20} -> Predição: {prediction}, Prob: [{proba[0]:.3f}, {proba[1]:.3f}]")
    except Exception as e:
        print(f"  {name:20} -> ERRO: {e}")

# Testar importância dos coeficientes
print(f"\n📊 ANÁLISE DOS COEFICIENTES:")
coefs = model.coef_[0]
print(f"Coeficientes: {coefs}")
print(f"Intercept: {model.intercept_[0]}")

# Ordenar por importância absoluta
feature_importance = [(i, abs(coefs[i])) for i in range(len(coefs))]
feature_importance.sort(key=lambda x: x[1], reverse=True)

print(f"\n🎯 FEATURES POR IMPORTÂNCIA (absoluta):")
for i, importance in feature_importance:
    print(f"  Feature {i}: {coefs[i]:.4f} (importância: {importance:.4f})")

# Tentar inferir pela magnitude dos coeficientes
print(f"\n💡 INFERÊNCIAS:")
print(f"  - Feature mais importante: #{feature_importance[0][0]} ({coefs[feature_importance[0][0]]:.4f})")
print(f"  - Feature menos importante: #{feature_importance[-1][0]} ({coefs[feature_importance[-1][0]]:.4f})")

print(f"\n" + "=" * 60)
print(f"🎯 COM BASE NOS COEFICIENTES:")
print(f"  Feature 0: {coefs[0]:.4f} - provavelmente turno_operacional")
print(f"  Feature 1: {coefs[1]:.4f} - provavelmente companhia_aerea")
print(f"  Feature 2: {coefs[2]:.4f} - provavelmente airport_pair")
print(f"  Feature 3: {coefs[3]:.4f} - provavelmente distancia (normalizada)")
print(f"  Feature 4: {coefs[4]:.4f} - provavelmente dia_semana")
print(f"  Feature 5: {coefs[5]:.4f} - provavelmente mes")
print(f"  Feature 6: {coefs[6]:.4f} - A 7ª FEATURE (precisa descobrir)")
