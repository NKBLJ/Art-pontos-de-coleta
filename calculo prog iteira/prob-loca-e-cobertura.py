import numpy as np
from scipy.optimize import minimize
import pandas as pd

# Importação dos dados
dados_bairros = pd.read_csv("../calculo prog iteira/bairros-agrupados-local.csv", sep=";", encoding='latin')
dados_coleta = pd.read_csv("../calculo prog iteira/pontos-coleta-com-coords.csv", sep=";", encoding='latin')

# Pontos dos bairros
bairros = np.array(dados_bairros[['latitude', 'longitude']].values)
populacoes = np.array(dados_bairros[['População']].values)

# Pontos de coleta já existentes
pontos_fixos = np.array(dados_coleta.loc[dados_coleta['tipo'] == 'fixo', ['latitude', 'longitude']])

# Número de novos pontos de coleta
k = 4
alpha = 10.0  # Peso para a cobertura
beta = 1.0  # Peso para o espalhamento

# Calcular os limites (bounds)
x_min, x_max = bairros[:, 0].min(), bairros[:, 0].max()
y_min, y_max = bairros[:, 1].min(), bairros[:, 1].max()
bounds = [(x_min, x_max), (y_min, y_max)] * k  # Repetir para cada ponto


# Função de custo combinada
def funcao_objetivo(pontos):
    pontos = pontos.reshape((k, 2))  # Reformata para coordenadas (x, y)

    # Termo 1: Custo de cobertura
    custo_cobertura = 0
    todos_pontos = np.vstack([pontos_fixos, pontos])  # Inclui os pontos fixos
    for i, bairro in enumerate(bairros):
        distancias = np.linalg.norm(bairro - todos_pontos, axis=1)
        custo_cobertura += populacoes[i] * np.min(distancias)  # Considera todos os pontos

    # Termo 2: Custo de espalhamento (apenas entre os novos pontos)
    distancias_pontos = []
    for j in range(k):
        for l in range(j + 1, k):
            distancias_pontos.append(np.linalg.norm(pontos[j] - pontos[l]))

    if distancias_pontos:
        custo_espalhamento = -np.min(distancias_pontos)  # Queremos maximizar, então invertido
    else:
        custo_espalhamento = 0

    # Combinação dos dois termos
    return alpha * custo_cobertura + beta * custo_espalhamento


# Configurações iniciais
pontos_iniciais = np.random.uniform(low=[x_min, y_min] * k, high=[x_max, y_max] * k)

# Otimização
resultado = minimize(funcao_objetivo, pontos_iniciais, bounds=bounds, method='L-BFGS-B')

# Resultados
pontos_otimizados = resultado.x.reshape((k, 2))
print("Coordenadas dos novos pontos de coleta:")
print(pontos_otimizados)

# Coordenadas finais (fixos + novos)
todos_pontos_finais = np.vstack([pontos_fixos, pontos_otimizados])
print("Todos os pontos de coleta (fixos e novos):")
print(todos_pontos_finais)
