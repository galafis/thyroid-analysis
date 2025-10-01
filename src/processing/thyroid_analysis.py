#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script principal para análise de dados de tireoide, incluindo pré-processamento, treinamento de modelo e avaliação.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Definir o caminho base para os dados
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')

def load_data(filename='thyroid_balanced_cleaned.csv'):
    """
    Carrega o dataset de tireoide.
    """
    filepath = os.path.join(DATA_PATH, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo de dados não encontrado: {filepath}")
    return pd.read_csv(filepath)

def preprocess_data(df):
    """
    Realiza o pré-processamento dos dados.
    """
    # Codificação de rótulos para a variável alvo
    le = LabelEncoder()
    df['diagnosis'] = le.fit_transform(df['diagnosis'])
    
    # Separar features e target
    X = df.drop('diagnosis', axis=1)
    y = df['diagnosis']
    
    # Normalização das features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y, le, scaler

def train_model(X_train, y_train):
    """
    Treina um modelo RandomForestClassifier.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, label_encoder):
    """
    Avalia o modelo e imprime as métricas.
    """
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"\n--- Avaliação do Modelo ---")
    print(f"Acurácia: {accuracy:.4f}")
    print(f"Precisão: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    return accuracy, precision, recall, f1

def save_artifacts(model, scaler, label_encoder):
    """
    Salva o modelo treinado, o scaler e o label encoder.
    """
    os.makedirs(MODEL_PATH, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_PATH, 'random_forest_model.pkl'))
    joblib.dump(scaler, os.path.join(MODEL_PATH, 'scaler.pkl'))
    joblib.dump(label_encoder, os.path.join(MODEL_PATH, 'label_encoder.pkl'))
    print(f"Modelo, scaler e label encoder salvos em {MODEL_PATH}")

def main():
    """
    Função principal para executar o pipeline de análise de tireoide.
    """
    print("Iniciando pipeline de análise de tireoide...")
    
    # 1. Carregar dados
    df = load_data()
    print(f"Dados carregados. Shape: {df.shape}")
    
    # 2. Pré-processar dados
    X_scaled, y, label_encoder, scaler = preprocess_data(df)
    print("Dados pré-processados.")
    
    # 3. Dividir dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Dados divididos: Treino={X_train.shape}, Teste={X_test.shape}")
    
    # 4. Treinar modelo
    model = train_model(X_train, y_train)
    print("Modelo treinado.")
    
    # 5. Avaliar modelo
    accuracy, precision, recall, f1 = evaluate_model(model, X_test, y_test, label_encoder)
    
    # 6. Salvar artefatos
    save_artifacts(model, scaler, label_encoder)
    
    print("Pipeline de análise de tireoide concluído com sucesso!")

if __name__ == "__main__":
    main()

