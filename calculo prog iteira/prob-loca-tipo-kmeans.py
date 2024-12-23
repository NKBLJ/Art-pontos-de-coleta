import numpy as np
from scipy.optimize import minimize
import pandas as pd

# Importação dos dados
dados_bairros = pd.read_csv("../calculo prog iteira/bairros-agrupados-local.csv", sep=";", encoding='latin')
dados_coleta = pd.read_csv("../calculo prog iteira/pontos-coleta-com-coords.csv", sep=";", encoding='latin')

# Pontos dos bairros
bairros = np.array(dados_bairros[['latitude', 'longitude']].values)
populacoes = np.array(dados_bairros[['População']].values)

pontos_fixos = np.array(dados_coleta.loc[dados_coleta['tipo'] == 'fixo', ['latitude', 'longitude']])

# Número de novos pontos de coleta
k = 4  # Apenas um novo ponto

# Calcular os limites (bounds)
x_min, x_max = bairros[:, 0].min(), bairros[:, 0].max()
y_min, y_max = bairros[:, 1].min(), bairros[:, 1].max()
bounds = [(x_min, x_max), (y_min, y_max)] * k

# Função de custo com pesos
def funcao_objetivo(pontos):
    pontos = pontos.reshape((k, 2))  # Reformata para coordenadas (x, y)
    todos_pontos = np.vstack([pontos_fixos, pontos])  # Inclui os pontos fixos
    custo_total = 0
    for bairro, pop in zip(bairros, populacoes):
        distancias = np.linalg.norm(bairro - todos_pontos, axis=1)  # Distâncias a todos os pontos
        custo_total += pop * np.min(distancias)  # Soma ponderada pela população
    return custo_total

# Ponto inicial aleatório dentro dos limites
pontos_iniciais = np.random.uniform(
    low=[x_min, y_min],
    high=[x_max, y_max],
    size=(k, 2)  # k pontos de 2 coordenadas cada
).flatten()  # Achata para que a otimização funcione

# Otimização
resultado = minimize(funcao_objetivo, pontos_iniciais, bounds=bounds, method='L-BFGS-B')

# Resultado final
pontos_otimizados = resultado.x.reshape((k, 2))
print("Novo ponto de coleta otimizado:")
print(pontos_otimizados)

# Todos os pontos
todos_pontos_finais = np.vstack([pontos_fixos, pontos_otimizados])
print("Todos os pontos de coleta (fixos e novos):")
print(todos_pontos_finais)

# Custo total após a otimização
custo_final = resultado.fun
print(f"Custo total após a otimização: {custo_final}")

# [[ -5.01211719 -42.79093269]
#  [ -5.09949165 -42.73918167]
#  [ -5.04748578 -42.82296153]
#  [ -5.0492309  -42.75206014]
# Custo final: 10341.56
