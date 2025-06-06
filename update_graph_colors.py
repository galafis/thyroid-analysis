#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para atualizar as cores dos gráficos no repositório thyroid-analysis.
Este script gera novos gráficos com cores mais diferenciadas para melhorar a interpretação visual.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import os

# Configurações gerais
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Definindo a nova paleta de cores
PALETA_ALGORITMOS = {
    'Random Forest': '#1E88E5',  # Azul Royal
    'SVM': '#D81B60',            # Rosa Escuro
    'Neural Network': '#FFC107', # Amarelo Âmbar
    'XGBoost': '#004D40',        # Verde Escuro
    'LightGBM': '#6A1B9A',       # Roxo Escuro
    'CatBoost': '#FF5722'        # Laranja Profundo
}

# Cores para visualizações SHAP
SHAP_COLORS = ['#1976D2', '#BDBDBD', '#D32F2F']  # Azul, Cinza, Vermelho
shap_cmap = LinearSegmentedColormap.from_list('shap_cmap', SHAP_COLORS)

# Cores para visualizações gerais
CORES_GERAIS = ['#2E7D32', '#C62828', '#1565C0', '#F57F17', '#6A1B9A', '#00838F']

def gerar_grafico_comparacao_algoritmos():
    """
    Gera um novo gráfico de comparação de algoritmos com cores mais diferenciadas.
    """
    # Dados simulados baseados no gráfico original
    algoritmos = ['Random Forest', 'SVM', 'Neural Network', 'XGBoost']
    metricas = ['Accuracy', 'Precision', 'Recall', 'F1-score']
    
    # Valores aproximados do gráfico original
    valores = {
        'Random Forest': [0.75, 0.85, 0.88, 0.86],
        'SVM': [0.73, 0.83, 0.85, 0.84],
        'Neural Network': [0.77, 0.87, 0.90, 0.88],
        'XGBoost': [0.76, 0.86, 0.89, 0.87]
    }
    
    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Largura das barras
    bar_width = 0.2
    index = np.arange(len(metricas))
    
    # Plotando as barras para cada algoritmo
    for i, (algoritmo, vals) in enumerate(valores.items()):
        ax.bar(index + i * bar_width, vals, bar_width, 
               label=algoritmo, color=PALETA_ALGORITMOS[algoritmo])
    
    # Adicionando rótulos e título
    ax.set_xlabel('Métricas', fontsize=14, fontweight='bold')
    ax.set_ylabel('Valor', fontsize=14, fontweight='bold')
    ax.set_title('Comparison of Machine Learning Algorithms for Thyroid Disease Classification', 
                fontsize=18, fontweight='bold')
    ax.set_xticks(index + bar_width * (len(algoritmos) - 1) / 2)
    ax.set_xticklabels(metricas, fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1.0)
    
    # Adicionando a legenda
    ax.legend(fontsize=12)
    
    # Adicionando grade
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adicionando valores nas barras
    for i, (algoritmo, vals) in enumerate(valores.items()):
        for j, val in enumerate(vals):
            ax.text(j + i * bar_width, val + 0.02, f'{val:.2f}', 
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Adicionando ícones ilustrativos para cada algoritmo
    fig.text(0.15, 0.5, "Random Forest", fontsize=14, fontweight='bold', color=PALETA_ALGORITMOS['Random Forest'])
    fig.text(0.15, 0.45, "XGBoost", fontsize=14, fontweight='bold', color=PALETA_ALGORITMOS['XGBoost'])
    fig.text(0.15, 0.4, "Neural Network", fontsize=14, fontweight='bold', color=PALETA_ALGORITMOS['Neural Network'])
    
    # Salvando o gráfico
    plt.tight_layout()
    plt.savefig('ml_algorithms_comparison_new.png', dpi=300, bbox_inches='tight')
    print("Gráfico de comparação de algoritmos gerado com sucesso!")

def gerar_grafico_interpretabilidade():
    """
    Gera um novo gráfico de interpretabilidade do modelo com cores mais diferenciadas.
    """
    # Criando uma figura para o gráfico de interpretabilidade
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Configurando o título principal
    fig.suptitle('MODEL INTERPRETABILITY FOR THYROID DISEASE CLASSIFICATION', 
                fontsize=20, fontweight='bold', y=1.05)
    fig.text(0.5, 0.96, 'SHAP AND LIME VISUALIZATIONS EXPLAINING MODEL PREDICTIONS', 
             ha='center', fontsize=14)
    
    # Simulando dados para SHAP Summary Plot
    features = ['TSH', 'T3', 'T4']
    feature_importance = [0.55, 0.35, 0.25]
    
    # SHAP Summary Plot
    axes[0].set_title('SHAP SUMMARY PLOT', fontsize=14, fontweight='bold')
    axes[0].barh(features, feature_importance, color=CORES_GERAIS[:3])
    axes[0].set_xlabel('Feature importance\n(SHAP value)', fontsize=12)
    axes[0].set_xlim(0, 0.6)
    
    # SHAP Force Plot
    axes[1].set_title('SHAP FORCE PLOT', fontsize=14, fontweight='bold')
    # Simulando dados para o force plot
    base_value = 0.5
    shap_values = [0.23, 0.15, 0.14]
    features_display = ['TSH = 7.4', 'T2 = 7.4', 'T3 = 2.5']
    
    # Plotando as barras
    axes[1].barh(['Base value', features_display[0], features_display[1], features_display[2]], 
                [base_value, shap_values[0], shap_values[1], shap_values[2]], 
                color=[CORES_GERAIS[3], CORES_GERAIS[0], CORES_GERAIS[1], CORES_GERAIS[2]])
    axes[1].axvline(x=0.5, color='gray', linestyle='--')
    axes[1].text(0.5, 4, 'Expected value', ha='center', va='bottom')
    axes[1].text(0.8, 4, '0.52', ha='center', va='bottom')
    axes[1].text(0.2, 4, 'Negative', ha='center', va='bottom')
    axes[1].text(0.3, 4, '0.23', ha='center', va='bottom')
    
    # LIME Explanation
    axes[2].set_title('LIME EXPLANATION', fontsize=14, fontweight='bold')
    # Simulando dados para LIME
    lime_features = ['TSH = 6.8', 'T3 = 2.5']
    lime_contributions = [0.15, 0.10]
    
    # Plotando as barras
    axes[2].barh(lime_features, lime_contributions, color=[CORES_GERAIS[4], CORES_GERAIS[5]])
    axes[2].set_xlabel('Contribution to classifier', fontsize=12)
    axes[2].text(0, -0.5, '0', ha='center', va='top')
    axes[2].text(0.15, -0.5, '0.15', ha='center', va='top')
    axes[2].text(0.10, -0.5, '0.10', ha='center', va='top')
    
    # Ajustando o layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    
    # Salvando o gráfico
    plt.savefig('model_interpretability_new.png', dpi=300, bbox_inches='tight')
    print("Gráfico de interpretabilidade gerado com sucesso!")

def gerar_grafico_visualizacao_ml():
    """
    Gera um novo gráfico de visualização ML com cores mais diferenciadas.
    """
    # Criando uma figura para o gráfico de visualização
    plt.figure(figsize=(16, 10))
    
    # Definindo um fundo escuro para o gráfico
    plt.style.use('dark_background')
    
    # Título principal
    plt.suptitle('THYROID GLAND ANALYSIS\nWITH MACHINE LEARNING', 
                fontsize=24, fontweight='bold', color='#00BCD4', y=0.98)
    
    # Criando um grid para organizar os elementos visuais
    gs = plt.GridSpec(3, 3)
    
    # Área para a forma da tireoide
    ax_thyroid = plt.subplot(gs[0:2, 0:3])
    ax_thyroid.axis('off')
    
    # Simulando a forma da tireoide com pontos
    theta = np.linspace(0, 2*np.pi, 100)
    r = 1 + 0.3 * np.sin(3*theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    # Criando a forma da tireoide
    ax_thyroid.plot(x, y, 'o', color='#00BCD4', alpha=0.7, markersize=8)
    
    # Adicionando pontos de conexão para simular uma rede neural
    np.random.seed(42)
    for _ in range(30):
        x1, y1 = np.random.choice(x), np.random.choice(y)
        x2, y2 = np.random.choice(x), np.random.choice(y)
        ax_thyroid.plot([x1, x2], [y1, y2], '-', color='#00BCD4', alpha=0.3)
    
    # Áreas para métricas e visualizações
    ax_tsh = plt.subplot(gs[2, 0])
    ax_tsh.set_title('TSH', color='#FF5722', fontsize=18, fontweight='bold')
    ax_tsh.axis('off')
    ax_tsh.text(0.5, 0.5, '7.4 mU/L', ha='center', va='center', color='#FF5722', fontsize=16)
    
    ax_t3 = plt.subplot(gs[2, 1])
    ax_t3.set_title('T3', color='#FFC107', fontsize=18, fontweight='bold')
    ax_t3.axis('off')
    ax_t3.text(0.5, 0.5, '2.1 nmol/L', ha='center', va='center', color='#FFC107', fontsize=16)
    
    ax_t4 = plt.subplot(gs[2, 2])
    ax_t4.set_title('T4', color='#4CAF50', fontsize=18, fontweight='bold')
    ax_t4.axis('off')
    ax_t4.text(0.5, 0.5, '110 nmol/L', ha='center', va='center', color='#4CAF50', fontsize=16)
    
    # Adicionando elementos decorativos
    for i in range(20):
        plt.figtext(np.random.random(), np.random.random(), '.', color='#424242')
    
    # Salvando o gráfico
    plt.tight_layout()
    plt.savefig('thyroid_ml_visualization_new.png', dpi=300, bbox_inches='tight', facecolor='#0A192F')
    print("Gráfico de visualização ML gerado com sucesso!")

def main():
    """
    Função principal que gera todos os gráficos.
    """
    print("Gerando novos gráficos com cores mais diferenciadas...")
    
    # Gerando os gráficos
    gerar_grafico_comparacao_algoritmos()
    gerar_grafico_interpretabilidade()
    gerar_grafico_visualizacao_ml()
    
    print("Todos os gráficos foram gerados com sucesso!")
    print("Novos arquivos:")
    print("- ml_algorithms_comparison_new.png")
    print("- model_interpretability_new.png")
    print("- thyroid_ml_visualization_new.png")

if __name__ == "__main__":
    main()

