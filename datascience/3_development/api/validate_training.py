import json
import requests
import pandas as pd
import numpy as np

def validate_training_consistency():
    """Valida se as predições da API são consistentes com o treinamento"""
    
    BASE_URL = "http://127.0.0.1:8000"
    
    print("="*70)
    print("🔬 VALIDAÇÃO DA INTEGRIDADE DO MODELO DE TREINAMENTO")
    print("="*70)
    
    # 1. Verificar saúde da API
    print("\n1️⃣ Verificando saúde da API...")
    try:
        health = requests.get(f"{BASE_URL}/health").json()
        print(f"   Status: {health['status']}")
        print(f"   Model Hash: {health.get('model_hash', 'N/A')}")
        print(f"   Features esperadas: {health.get('features_count', 'N/A')}")
    except:
        print("   ❌ API não responde")
        return
    
    # 2. Obter informações de debug
    print("\n2️⃣ Informações do modelo...")
    debug_info = requests.get(f"{BASE_URL}/debug").json()
    print(f"   Tipo do modelo: {debug_info['model_info']['type']}")
    print(f"   Classes: {debug_info['model_info'].get('classes', [])}")
    print(f"   Ordem das features: {debug_info['feature_order']}")
    
    # 3. Executar validação automática
    print("\n3️⃣ Executando testes de validação...")
    validation = requests.post(f"{BASE_URL}/validate").json()
    
    print(f"\n   Resumo dos testes:")
    print(f"   Total: {validation['summary']['total_tests']}")
    print(f"   Passou: {validation['summary']['passed']}")
    print(f"   Falhou: {validation['summary']['failed']}")
    print(f"   Erros: {validation['summary']['errors']}")
    
    # 4. Testar casos específicos do treinamento
    print("\n4️⃣ Testando casos do treinamento...")
    
    # CASOS QUE VOCÊ DEVE PREENCHER COM DADOS REAIS DO SEU TREINAMENTO
    training_cases = [
        {
            "name": "Voo curto manhã",
            "data": {
                "companhia": "LATAM",
                "aeroporto_origem": "GRU",
                "aeroporto_destino": "CGH",
                "distancia": 50,
                "hora_partida": "manha",
                "dia_semana": 1
            },
            "expected": "pontual"  # O que você espera baseado no treino
        },
        {
            "name": "Voo longo noite sexta",
            "data": {
                "companhia": "GOL",
                "aeroporto_origem": "GRU",
                "aeroporto_destino": "SSA",
                "distancia": 2500,
                "hora_partida": "noite",
                "dia_semana": 5
            },
            "expected": "atraso"  # O que você espera baseado no treino
        }
    ]
    
    results = []
    for case in training_cases:
        try:
            response = requests.post(f"{BASE_URL}/predict", json=case["data"]).json()
            
            if "error" in response:
                result = "❌ ERRO"
            else:
                prediction = "atraso" if response["atraso"] else "pontual"
                prob = response["probabilidade_atraso"]
                correct = (prediction == case["expected"])
                result = "✅ CORRETO" if correct else f"❌ ESPERAVA {case['expected'].upper()}"
                
                results.append({
                    "Caso": case["name"],
                    "Probabilidade": f"{prob:.2%}",
                    "Predição": prediction.upper(),
                    "Esperado": case["expected"].upper(),
                    "Resultado": result
                })
                
        except Exception as e:
            results.append({
                "Caso": case["name"],
                "Probabilidade": "N/A",
                "Predição": "ERRO",
                "Esperado": case["expected"].upper(),
                "Resultado": f"❌ {str(e)}"
            })
    
    # Mostrar tabela de resultados
    df = pd.DataFrame(results)
    print(f"\n{df.to_string(index=False)}")
    
    # 5. Testar coeficientes do modelo
    print("\n5️⃣ Analisando comportamento do modelo...")
    
    # Testar com features extremas
    print("\n   Testando comportamento com inputs extremos:")
    
    extreme_tests = [
        {"name": "Todas features zero", "features": [0, 0, 0, 0, 0, 0, 0]},
        {"name": "Distância máxima", "features": [10, 1, 1, 0, 0, 0, 3]},
        {"name": "Noite + Sexta", "features": [2.5, 2, 1, 0, 0, 0, 5]},
    ]
    
    for test in extreme_tests:
        try:
            response = requests.post(f"{BASE_URL}/test-model", 
                                   json={"features": test["features"]}).json()
            
            if response["status"] == "success":
                prob_atraso = response["probabilities"]["class_1"]
                print(f"   {test['name']}: {prob_atraso:.2%} de atraso")
            else:
                print(f"   {test['name']}: ERRO - {response.get('message', 'Unknown')}")
                
        except Exception as e:
            print(f"   {test['name']}: Falha na requisição")
    
    # 6. Conclusão
    print("\n" + "="*70)
    print("📋 CONCLUSÃO DA VALIDAÇÃO")
    print("="*70)
    
    if validation['summary']['passed'] > 0 and len([r for r in results if '✅' in r['Resultado']]) > 0:
        print("✅ O modelo parece estar usando os dados de treinamento corretamente.")
        print("   As predições são consistentes com o comportamento esperado.")
    else:
        print("⚠️  Possíveis problemas detectados:")
        print("   1. Ordem das features pode estar incorreta")
        print("   2. Encoders podem não estar sendo aplicados corretamente")
        print("   3. Modelo pode estar corrompido ou diferente do treinado")
    
    print(f"\n🛠️  Próximos passos:")
    print(f"   1. Preencha TRAINING_VALIDATION_DATA com dados reais do treino")
    print(f"   2. Verifique a ordem das features usadas no treinamento")
    print(f"   3. Compare o hash do modelo atual com o do treinamento")

def extract_training_info():
    """Extrai informações do modelo treinado para preencher validation_data"""
    import joblib
    
    MODEL_PATH = "../models/logistic_regression_optimized_final.joblib"
    
    try:
        model = joblib.load(MODEL_PATH)
        
        print("\n📊 INFORMAÇÕES DO MODELO TREINADO:")
        print("="*50)
        
        # Informações básicas
        print(f"Tipo: {type(model)}")
        print(f"Número de features: {model.n_features_in_}")
        print(f"Classes: {model.classes_}")
        
        # Coeficientes (se disponível)
        if hasattr(model, 'coef_'):
            print(f"\nCoeficientes (primeiros 10):")
            for i, coef in enumerate(model.coef_[0][:10]):
                print(f"  Feature {i}: {coef:.4f}")
        
        # Intercept
        if hasattr(model, 'intercept_'):
            print(f"\nIntercept: {model.intercept_[0]:.4f}")
        
        # Informações sobre as features
        print(f"\n💡 DICAS PARA PREENCHER VALIDATION_DATA:")
        print("1. Execute predições em dados conhecidos do conjunto de treino")
        print("2. Anote as probabilidades obtidas durante o treinamento")
        print("3. Use essas probabilidades como 'expected_proba_range'")
        print("4. Verifique a ordem das features usadas no pipeline de treino")
        
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")

if __name__ == "__main__":
    # Extrair informações do modelo (execute uma vez para preencher dados)
    extract_training_info()
    
    # Validar a API em execução
    print("\n" + "="*70)
    input("Pressione Enter para validar a API em execução...")
    validate_training_consistency()