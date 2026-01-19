import joblib
import json
import numpy as np
import os

print("🔍 Testando carregamento do modelo...")

# Tentar carregar o modelo
model_path = "model.joblib"
if os.path.exists(model_path):
    print(f"✅ Encontrado: {model_path}")
    try:
        model = joblib.load(model_path)
        print(f"✅ Modelo carregado com sucesso!")
        print(f"📊 Tipo: {type(model)}")
        
        # Mostrar atributos do modelo
        print(f"\n🔧 Atributos disponíveis:")
        for attr in dir(model):
            if not attr.startswith('_'):
                print(f"  - {attr}")
        
        # Verificar se é pipeline
        if hasattr(model, 'named_steps'):
            print(f"\n🔧 Passos do pipeline:")
            for name, step in model.named_steps.items():
                print(f"  - {name}: {type(step)}")
        
        # Verificar features
        if hasattr(model, 'feature_names_in_'):
            print(f"\n🔤 Features esperadas (em ordem):")
            for i, name in enumerate(model.feature_names_in_):
                print(f"  {i}: {name}")
        
        # Verificar número de features
        if hasattr(model, 'n_features_in_'):
            print(f"\n📐 Número de features esperadas: {model.n_features_in_}")
        
        # Testar predição simples
        print(f"\n🧪 Testando predição...")
        
        # Criar array de teste com número correto de features
        n_features = 6  # Ajuste conforme necessário
        
        # Array de exemplo (6 features como discutido)
        test_array = [[1, 0, 0, 3500.0, 2, 1]]  # Tarde, LATAM, GRU-SCL, 3500km, Quarta, Janeiro
        
        try:
            if hasattr(model, 'predict'):
                prediction = model.predict(test_array)
                print(f"✅ Predição: {prediction[0]}")
                
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(test_array)
                    print(f"✅ Probabilidades: {proba[0]}")
                    print(f"   Classe 0 (pontual): {proba[0][0]:.3f}")
                    print(f"   Classe 1 (atrasado): {proba[0][1]:.3f}")
                    
        except Exception as e:
            print(f"❌ Erro na predição: {e}")
            print("\n💡 Tentando com diferentes números de features...")
            
            # Tentar com diferentes tamanhos
            for n in [4, 5, 6, 7, 8]:
                try:
                    test_features = [[1] * n]
                    prediction = model.predict(test_features)
                    print(f"  Com {n} features: {prediction[0]}")
                except:
                    pass
        
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
else:
    print(f"❌ Arquivo {model_path} não encontrado")
    print(f"\n📁 Arquivos na pasta atual:")
    for f in os.listdir('.'):
        print(f"  {f}")