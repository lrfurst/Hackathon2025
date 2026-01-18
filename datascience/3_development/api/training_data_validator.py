"""
Script para comparar predições da API com resultados do treinamento.
Execute este script APÓS o treinamento para criar um arquivo de validação.
"""

import pandas as pd
import numpy as np
import joblib
import json
import pickle

def create_validation_reference():
    """
    Cria um arquivo de referência baseado no treinamento.
    
    PASSO A PASSO:
    1. Execute este script após o treinamento
    2. Ele criará um arquivo 'validation_reference.json'
    3. Use esse arquivo para preencher TRAINING_VALIDATION_DATA no main.py
    """
    
    # CONFIGURAÇÃO - AJUSTE ESTES VALORES
    MODEL_PATH = "../models/logistic_regression_optimized_final.joblib"
    TRAINING_DATA_PATH = "../data/processed/training_data.csv"  # Ajuste o caminho
    ENCODERS_PATH = "../models/encoders/"
    
    try:
        # Carregar modelo
        print("🔍 Carregando modelo...")
        model = joblib.load(MODEL_PATH)
        
        # Carregar dados de treino (se disponível)
        print("📊 Carregando dados de treino...")
        try:
            X_train = pd.read_csv(TRAINING_DATA_PATH)
            print(f"   Dimensões: {X_train.shape}")
            
            # Pegar algumas amostras representativas
            samples = X_train.sample(min(5, len(X_train)))
            
            validation_cases = []
            for idx, sample in samples.iterrows():
                # Converter para lista de features (ajuste conforme suas colunas)
                features = sample.values.tolist()[:model.n_features_in_]
                
                # Fazer predição
                probs = model.predict_proba([features])[0]
                
                validation_cases.append({
                    "sample_index": int(idx),
                    "features": features,
                    "probabilities": {
                        "class_0": float(probs[0]),
                        "class_1": float(probs[1])
                    },
                    "prediction": int(model.predict([features])[0])
                })
                
        except Exception as e:
            print(f"   ❌ Não foi possível carregar dados de treino: {e}")
            validation_cases = []
        
        # Criar casos de teste conhecidos
        print("🧪 Criando casos de teste de referência...")
        
        # CASO 1: Baseline (todas features zero/mínimas)
        baseline_features = [0] * model.n_features_in_
        baseline_probs = model.predict_proba([baseline_features])[0]
        
        # CASO 2: Features máximas (ajuste conforme seus dados)
        max_features = [10 if i == 0 else 2 for i in range(model.n_features_in_)]  # Exemplo
        max_probs = model.predict_proba([max_features])[0]
        
        reference_data = {
            "model_info": {
                "model_type": str(type(model)),
                "n_features": model.n_features_in_,
                "classes": model.classes_.tolist() if hasattr(model, 'classes_') else [],
                "model_hash": "..."  # Você pode adicionar hash aqui
            },
            "validation_cases": [
                {
                    "name": "baseline_all_zeros",
                    "features": baseline_features,
                    "expected_proba_range": [
                        float(baseline_probs[0]) * 0.9,  # 10% de margem
                        float(baseline_probs[0]) * 1.1
                    ]
                },
                {
                    "name": "max_values_example",
                    "features": max_features,
                    "expected_proba_range": [
                        float(max_probs[0]) * 0.9,
                        float(max_probs[0]) * 1.1
                    ]
                }
            ] + validation_cases,
            "feature_names": [f"feature_{i}" for i in range(model.n_features_in_)]  # Nomeie suas features!
        }
        
        # Salvar referência
        output_path = "validation_reference.json"
        with open(output_path, 'w') as f:
            json.dump(reference_data, f, indent=2)
        
        print(f"\n✅ Referência de validação salva em: {output_path}")
        print(f"\n📋 INFORMAÇÕES PARA O main.py:")
        print("="*50)
        print("\n1. Número de features esperadas:", model.n_features_in_)
        print("\n2. Use esta ordem de features:")
        for i, feature in enumerate(reference_data["feature_names"]):
            print(f"   [{i}] {feature}")
        
        print("\n3. Copie os casos de validação para TRAINING_VALIDATION_DATA:")
        print(json.dumps(reference_data["validation_cases"][:2], indent=2))
        
        return reference_data
        
    except Exception as e:
        print(f"❌ Erro ao criar referência: {e}")
        return None

def compare_with_training():
    """Compara predições atuais com resultados do treinamento"""
    
    # Carregar referência
    try:
        with open("validation_reference.json", 'r') as f:
            reference = json.load(f)
    except:
        print("❌ Execute primeiro create_validation_reference()")
        return
    
    # Testar cada caso
    print("\n🔬 COMPARANDO COM REFERÊNCIA DE TREINAMENTO")
    print("="*60)
    
    import requests
    
    for case in reference["validation_cases"]:
        print(f"\nCaso: {case['name']}")
        
        # Testar via API
        try:
            response = requests.post(
                "http://127.0.0.1:8000/test-model",
                json={"features": case["features"]}
            ).json()
            
            if response["status"] == "success":
                current_prob = response["probabilities"]["class_0"]
                expected_min, expected_max = case["expected_proba_range"]
                
                print(f"  Probabilidade atual: {current_prob:.4f}")
                print(f"  Faixa esperada: {expected_min:.4f} - {expected_max:.4f}")
                
                if expected_min <= current_prob <= expected_max:
                    print(f"  ✅ DENTRO DA FAIXA ESPERADA")
                else:
                    print(f"  ❌ FORA DA FAIXA ESPERADA")
                    print(f"     Diferença: {abs(current_prob - ((expected_min+expected_max)/2)):.4f}")
            else:
                print(f"  ❌ Erro na API: {response.get('message', 'Unknown')}")
                
        except Exception as e:
            print(f"  ❌ Falha na requisição: {e}")

if __name__ == "__main__":
    print("="*70)
    print("🛠️  VALIDADOR DE CONSISTÊNCIA DO TREINAMENTO")
    print("="*70)
    
    # Opção 1: Criar referência do treinamento (execute APÓS treinar)
    # reference = create_validation_reference()
    
    # Opção 2: Comparar com referência (execute com API rodando)
    compare_with_training()