"""
transform_simple.py - Transformador de features simplificado para MVP

Transforma 5 inputs do usuário em 7 features para o modelo de previsão de atrasos.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import time
from typing import Dict, Any, Optional
import json

class MVPTrafficFeatureTransformer:
    """Transformador de features simplificado para MVP"""
    
    def __init__(self, encoders_path: Optional[str] = None):
        """
        Inicializa o transformador.
        
        Args:
            encoders_path: Caminho para arquivo JSON com encoders pré-treinados
        """
        self.airline_encoder = {}
        self.route_encoder = {}
        self.min_distance = 0
        self.max_distance = 5000
        
        if encoders_path:
            self.load_encoders(encoders_path)
    
    def load_encoders(self, path: str):
        """Carrega encoders de um arquivo JSON"""
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.airline_encoder = data.get('airline_encoder', {})
        self.route_encoder = data.get('route_encoder', {})
        distance_stats = data.get('distance_stats', {})
        self.min_distance = distance_stats.get('min_distance', 0)
        self.max_distance = distance_stats.get('max_distance', 5000)
    
    def save_encoders(self, path: str):
        """Salva encoders em um arquivo JSON"""
        data = {
            'airline_encoder': self.airline_encoder,
            'route_encoder': self.route_encoder,
            'distance_stats': {
                'min_distance': self.min_distance,
                'max_distance': self.max_distance
            },
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def fit(self, df: pd.DataFrame):
        """Aprende encodings dos dados de treino"""
        # Encoding de companhia aérea
        if 'OP_CARRIER' in df.columns:
            airlines = df['OP_CARRIER'].dropna().unique()
            self.airline_encoder = {airline: idx for idx, airline in enumerate(sorted(airlines))}
        
        # Encoding de rotas
        if 'ORIGIN' in df.columns and 'DEST' in df.columns:
            routes = df.apply(lambda row: f"{row['ORIGIN']}-{row['DEST']}", axis=1).unique()
            self.route_encoder = {route: idx for idx, route in enumerate(sorted(routes))}
        
        # Estatísticas de distância
        if 'DISTANCE' in df.columns:
            self.min_distance = df['DISTANCE'].min()
            self.max_distance = df['DISTANCE'].max()
        
        return self
    
    def transform_single(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforma inputs do usuário em features do modelo.
        
        Args:
            user_inputs: {
                'companhia_aerea': str (ex: 'AA'),
                'aeroporto_origem': str (ex: 'JFK'),
                'aeroporto_destino': str (ex: 'LAX'),
                'data_hora_partida': str (ISO 8601),
                'distancia_km': float
            }
        
        Returns:
            Dicionário com 7 features para o modelo
        """
        # 1. Companhia aérea
        airline_code = user_inputs.get('companhia_aerea', 'UNKNOWN')
        encoded_simple_airline = self.airline_encoder.get(airline_code, -1)
        
        # 2. Rota
        origin = user_inputs.get('aeroporto_origem', 'UNK')
        dest = user_inputs.get('aeroporto_destino', 'UNK')
        route_pair = f"{origin}-{dest}"
        encoded_route_pair = self.route_encoder.get(route_pair, -1)
        
        # 3. Data/hora
        departure_datetime = pd.to_datetime(user_inputs.get('data_hora_partida', datetime.now()))
        
        hour_of_day = departure_datetime.hour
        
        # Categoria do horário
        if 0 <= hour_of_day < 6:
            time_of_day_category = 'madrugada'
        elif 6 <= hour_of_day < 12:
            time_of_day_category = 'manha'
        elif 12 <= hour_of_day < 18:
            time_of_day_category = 'tarde'
        else:
            time_of_day_category = 'noite'
        
        day_of_week = departure_datetime.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # 4. Distância
        distance_km = user_inputs.get('distancia_km', 0.0)
        distance_normalized = (distance_km - self.min_distance) / (self.max_distance - self.min_distance + 1e-10)
        distance_normalized = max(0.0, min(1.0, distance_normalized))
        
        return {
            'encoded_simple_airline': encoded_simple_airline,
            'encoded_route_pair': encoded_route_pair,
            'hour_of_day': hour_of_day,
            'time_of_day_category': time_of_day_category,
            'day_of_week': day_of_week,
            'distance_km': distance_normalized,
            'is_weekend': is_weekend
        }
    
    def validate_input(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Valida inputs do usuário"""
        errors = []
        
        # Validar companhia aérea
        airline = user_inputs.get('companhia_aerea', '')
        if not isinstance(airline, str) or len(airline) != 2:
            errors.append('companhia_aerea deve ser string de 2 caracteres')
        
        # Validar aeroportos
        for field in ['aeroporto_origem', 'aeroporto_destino']:
            airport = user_inputs.get(field, '')
            if not isinstance(airport, str) or len(airport) != 3:
                errors.append(f'{field} deve ser string de 3 caracteres')
        
        # Validar data/hora
        try:
            pd.to_datetime(user_inputs.get('data_hora_partida'))
        except:
            errors.append('data_hora_partida deve ser data/hora válida')
        
        # Validar distância
        distance = user_inputs.get('distancia_km', 0)
        if not isinstance(distance, (int, float)) or distance < 0 or distance > 5000:
            errors.append('distancia_km deve ser número entre 0 e 5000')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

# Exemplo de uso
if __name__ == "__main__":
    # Criar transformador
    transformer = MVPTrafficFeatureTransformer()
    
    # Exemplo de input
    example_input = {
        'companhia_aerea': 'AA',
        'aeroporto_origem': 'JFK',
        'aeroporto_destino': 'LAX',
        'data_hora_partida': '2024-01-15T14:30:00',
        'distancia_km': 3980.0
    }
    
    # Validar input
    validation = transformer.validate_input(example_input)
    if validation['is_valid']:
        # Transformar
        features = transformer.transform_single(example_input)
        print("Features geradas:", features)
    else:
        print("Erros:", validation['errors'])
