import joblib
import json

print("🔍 DETALHES COMPLETOS DO MODELO")
print("=" * 60)

model = joblib.load('model.joblib')

print(f"\n📊 INFORMAÇÕES DO MODELO:")
print(f"Tipo: {type(model)}")
print(f"Classes: {model.classes_ if hasattr(model, 'classes_') else 'N/A'}")
print(f"Coeficientes shape: {model.coef_.shape if hasattr(model, 'coef_') else 'N/A'}")

# Listar todos os atributos
print(f"\n🔧 ATRIBUTOS DISPONÍVEIS:")
for attr in dir(model):
    if not attr.startswith('_'):
        try:
            value = getattr(model, attr)
            if not callable(value):
                print(f"  {attr}: {type(value).__name__}")
        except:
            pass

# Verificar se é um pipeline
if hasattr(model, 'named_steps'):
    print(f"\n🔧 É um PIPELINE com passos:")
    for name, step in model.named_steps.items():
        print(f"  {name}: {type(step)}")

print("\n" + "=" * 60)
