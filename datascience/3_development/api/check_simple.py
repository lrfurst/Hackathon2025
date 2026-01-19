# check_simple.py
import joblib
import json
import os

print("🔍 VERIFICANDO MODELO DE TREINAMENTO")
print("="*60)

# Caminhos (ajuste se necessário)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "logistic_regression_optimized_final.joblib")
ENCODERS_DIR = os.path.join(BASE_DIR, "..", "models", "encoders")

print(f"Procurando modelo em: {MODEL_PATH}")

if not os.path.exists(MODEL_PATH):
    print(f"❌ Modelo não encontrado!")
    print(f"   Caminho procurado: {MODEL_PATH}")
    exit(1)

try:
    # 1. Carregar modelo
    print("\n📦 CARREGANDO MODELO...")
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modelo carregado com sucesso!")
    
    # 2. Informações básicas
    print(f"\n📊 INFORMAÇÕES DO MODELO:")
    print(f"   Tipo: {type(model)}")
    
    if hasattr(model, 'n_features_in_'):
        print(f"   Número de features: {model.n_features_in_}")
    else:
        print(f"   ❌ Modelo não tem atributo 'n_features_in_'")
        print(f"   Isso pode ser um problema!")
    
    if hasattr(model, 'classes_'):
        print(f"   Classes: {model.classes_}")
    
    # 3. Verificar encoders
    print(f"\n🔤 VERIFICANDO ENCODERS...")
    
    companhia_path = os.path.join(ENCODERS_DIR, "companhia_encoder.json")
    airport_path = os.path.join(ENCODERS_DIR, "airport_pair_encoder.json")
    
    if os.path.exists(companhia_path):
        with open(companhia_path, 'r') as f:
            companhia_map = json.load(f)
        print(f"✅ Encoder de companhia: {len(companhia_map)} itens")
        print(f"   Exemplo: {list(companhia_map.items())[:3]}")
    else:
        print(f"❌ Encoder de companhia não encontrado: {companhia_path}")
    
    if os.path.exists(airport_path):
        with open(airport_path, 'r') as f:
            airport_map = json.load(f)
        print(f"✅ Encoder de aeroportos: {len(airport_map)} itens")
        print(f"   Exemplo: {list(airport_map.items())[:3]}")
    else:
        print(f"❌ Encoder de aeroportos não encontrado: {airport_path}")
    
    # 4. Testar predições básicas
    print(f"\n🧪 TESTANDO PREDIÇÕES...")
    
    # Primeiro, descubra quantas features o modelo espera
    if hasattr(model, 'n_features_in_'):
        n_features = model.n_features_in_
        
        print(f"   O modelo espera {n_features} features")
        
        # Teste 1: Todas zero
        test1 = [[0] * n_features]
        try:
            prob1 = model.predict_proba(test1)[0]
            print(f"\n   Teste 1 - Todas features = 0:")
            print(f"      Probabilidade classe 0: {prob1[0]:.4f}")
            print(f"      Probabilidade classe 1: {prob1[1]:.4f}")
            
            # Adivinhar qual classe é qual
            if prob1[0] > prob1[1]:
                print(f"      ↳ Classe 0 parece ser PONTUAL")
                print(f"      ↳ Classe 1 parece ser ATRASO")
            else:
                print(f"      ↳ Classe 0 parece ser ATRASO")
                print(f"      ↳ Classe 1 parece ser PONTUAL")
                
        except Exception as e:
            print(f"   ❌ Erro no teste 1: {e}")
        
        # Teste 2: Valores diferentes para ver padrão
        if n_features == 7:
            # Se for 7 features, testar com valores diferentes
            print(f"\n   ⚠️  SEU MODELO TEM 7 FEATURES - Vamos testar diferentes combinações:")
            
            tests = [
                ("Distância alta (5.0)", [5.0, 0, 0, 0, 0, 0, 0]),
                ("Noite (2)", [1.5, 2, 0, 0, 0, 0, 0]),
                ("Sexta-feira (5)", [1.5, 0, 0, 0, 0, 0, 5]),
                ("Companhia diferente (1)", [1.5, 0, 1, 0, 0, 0, 0]),
                ("Rota conhecida (se tiver)", [1.5, 0, 0, 0, 0, 10, 0]),
            ]
            
            for test_name, test_features in tests:
                try:
                    if len(test_features) == n_features:
                        prob = model.predict_proba([test_features])[0]
                        print(f"\n   {test_name}:")
                        print(f"      Features: {test_features}")
                        print(f"      Prob: [Classe0={prob[0]:.4f}, Classe1={prob[1]:.4f}]")
                except Exception as e:
                    print(f"   ❌ Erro em {test_name}: {e}")
    
    # 5. Verificar se tem coeficientes
    print(f"\n🔢 VERIFICANDO COEFICIENTES...")
    
    if hasattr(model, 'coef_'):
        coefs = model.coef_[0]
        print(f"   Número de coeficientes: {len(coefs)}")
        
        print(f"\n   Os 5 coeficientes mais importantes (absoluto):")
        sorted_idx = sorted(range(len(coefs)), key=lambda i: abs(coefs[i]), reverse=True)
        
        for i in range(min(5, len(coefs))):
            idx = sorted_idx[i]
            print(f"      Feature {idx}: {coefs[idx]:.6f}")
        
        print(f"\n   TODOS os coeficientes:")
        for i, coef in enumerate(coefs):
            print(f"      [{i}] {coef:.6f}")
    else:
        print(f"   Modelo não tem coeficientes visíveis")
    
    # 6. CRIAR ARQUIVO DE CONFIGURAÇÃO
    print(f"\n💾 CRIANDO ARQUIVO DE CONFIGURAÇÃO...")
    
    config = {
        "model_info": {
            "path": MODEL_PATH,
            "type": str(type(model)),
            "n_features": n_features if hasattr(model, 'n_features_in_') else "unknown",
            "has_coefficients": hasattr(model, 'coef_')
        },
        "important_note": "A ORDEM DAS FEATURES NO SEU main.py DEVE SER EXATAMENTE A MESMA QUE O MODELO ESPERA!"
    }
    
    with open("model_info.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuração salva em: model_info.json")
    
    # 7. VERIFICAR SEU main.py ATUAL
    print(f"\n🔍 ANALISANDO SEU main.py...")
    
    main_py_path = os.path.join(BASE_DIR, "main.py")
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r') as f:
            content = f.read()
            
        # Procurar onde as features são criadas
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'input_data = [' in line or 'features = [' in line:
                print(f"   Linha {i+1}: {line.strip()}")
                # Mostrar as próximas linhas também
                for j in range(i+1, min(i+10, len(lines))):
                    if ']' in lines[j]:
                        print(f"   Linha {j+1}: {lines[j].strip()}")
                        break
                    print(f"   Linha {j+1}: {lines[j].strip()}")
    
    print(f"\n🎯 CONCLUSÃO:")
    print(f"   1. Seu modelo tem {n_features if hasattr(model, 'n_features_in_') else '?'} features")
    print(f"   2. A ORDEM no main.py DEVE bater com essa quantidade")
    print(f"   3. Verifique os coeficientes acima para entender o peso de cada feature")
    
    print(f"\n🔧 PRÓXIMOS PASSOS:")
    print(f"   1. Compare a ordem das features no main.py com os coeficientes acima")
    print(f"   2. Se a ordem estiver errada, corrija no main.py")
    print(f"   3. Teste novamente com diferentes valores")
    
except Exception as e:
    print(f"\n❌ ERRO GRAVE: {e}")
    import traceback
    traceback.print_exc()