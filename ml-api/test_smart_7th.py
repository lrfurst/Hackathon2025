import joblib
import numpy as np

print("🤔 TESTE INTELIGENTE PARA DESCOBRIR A 7ª FEATURE")
print("=" * 60)

model = joblib.load('model.joblib')
coefs = model.coef_[0]
print(f"Coeficiente da 7ª feature: {coefs[6]:.4f}")

# Sabemos que é POSITIVO (0.0830), então valores maiores = mais atraso
# Vamos testar valores que fazem sentido aumentarem atrasos:

print(f"\n🧪 Testando valores crescentes para a 7ª feature:")
print("(manter outras features constantes)")

# Base fixa
base = [1, 0, 0, 0.35, 2, 1]  # turno, LATAM, GRU-SCL, distância, quarta, janeiro

# Valores que FAZEM SENTE serem positivos para atrasos
test_values = [
    ("Hora tarde (18h)", 18),
    ("Hora noite (22h)", 22),
    ("Final de mês (28)", 28),
    ("Fim de semana (6)", 6),  # se for dia da semana, domingo=6
    ("Mês alto (12)", 12),  # dezembro
    ("Feriado (1)", 1),
    ("Alta temporada (1)", 1),
    ("Baixa temporada (0)", 0),
]

for name, val in test_values:
    features = base + [val]
    try:
        proba = model.predict_proba([features])[0]
        prob_atraso = proba[1]  # Probabilidade de atraso
        print(f"  {name:20} (valor={val:2d}) -> Prob atraso: {prob_atraso:.3f}")
    except:
        pass

# Agora vamos fazer uma análise mais científica
print(f"\n🔬 ANÁLISE CIENTÍFICA:")
print("Vamos ver como muda a probabilidade com diferentes valores:")

# Testar range 0-30 (cobre hora, dia, mês, etc.)
print(f"\n📈 Probabilidade de atraso vs valor da 7ª feature:")
for val in [0, 5, 10, 15, 20, 25, 30]:
    features = base + [val]
    proba = model.predict_proba([features])[0]
    prob_atraso = proba[1]
    print(f"  Valor {val:2d} -> Prob atraso: {prob_atraso:.3f}")

# Verificar se é normalizado (0-1) ou não
print(f"\n💡 TESTANDO SE É NORMALIZADO (0-1):")
for val in [0, 0.1, 0.5, 0.9, 1.0]:
    features = base + [val]
    proba = model.predict_proba([features])[0]
    prob_atraso = proba[1]
    print(f"  Valor {val:.1f} -> Prob atraso: {prob_atraso:.3f}")

# Baseado na análise do README original
print(f"\n📚 RELEMBRANDO O README:")
print("Das análises do projeto:")
print("1. 'Turnos Operacionais (Manhã vs. Tarde/Noite)' - JÁ TEMOS (feature 0)")
print("2. 'Voos no 2º Turno têm probabilidade maior'")
print("3. 'Impacto da Companhia Aérea' - JÁ TEMOS (feature 1)")
print("4. 'Distância' - JÁ TEMOS (feature 3)")
print("5. Que mais? Talvez HORA EXATA foi mantida?")
print("6. Ou TEMPERATURA? CONDIÇÕES CLIMÁTICAS?")

print(f"\n🎯 MINHA APOSTA:")
print("A 7ª feature provavelmente é HORA_DO_DIA (0-23)")
print("Porque:")
print("1. Faz sentido ter coeficiente positivo (horas mais tarde = mais atraso)")
print("2. É mencionado no README sobre análise temporal")
print("3. É uma feature natural que complementa o 'turno'")
print("4. Valores entre 0-23 fazem sentido")

print(f"\n" + "=" * 60)
print("✅ CONCLUSÃO: Vamos assumir que é HORA_DO_DIA")
print("   Feature 6 = hora_do_dia (0-23)")
