import numpy as np
import pandas as pd
from itertools import product

# Importação dos dados
dados_bairros = pd.read_csv("../calculo prog iteira/bairros-agrupados-local.csv", sep=";", encoding='latin')
dados_coleta = pd.read_csv("../calculo prog iteira/pontos-coleta-com-coords.csv", sep=";", encoding='latin')

# Pontos dos bairros
bairros = np.array(dados_bairros[['latitude', 'longitude']].values)
populacoes = np.array(dados_bairros[['População']].values)

# Pontos fixos
pontos_fixos = np.array(dados_coleta.loc[dados_coleta['tipo'] == 'fixo', ['latitude', 'longitude']])

# Número de novos pontos de coleta
k = 4  # Número de novos pontos

# Calcular os limites (bounds)
x_min, x_max = bairros[:, 0].min(), bairros[:, 0].max()
y_min, y_max = bairros[:, 1].min(), bairros[:, 1].max()

# Função de custo com pesos
def funcao_objetivo(pontos):
    pontos = pontos.reshape((k, 2))  # Reformata para coordenadas (x, y)
    todos_pontos = np.vstack([pontos_fixos, pontos])  # Inclui os pontos fixos
    custo_total = 0
    for bairro, pop in zip(bairros, populacoes):
        distancias = np.linalg.norm(bairro - todos_pontos, axis=1)  # Distâncias a todos os pontos
        custo_total += pop * np.min(distancias)  # Soma ponderada pela população
    return custo_total

# Configuração da grade
resolucao = 50  # Número de divisões em cada dimensão (maior valor = mais precisão, mas mais lento)
x_vals = np.linspace(x_min, x_max, resolucao)
y_vals = np.linspace(y_min, y_max, resolucao)

# Busca exaustiva
melhor_custo = float('inf')
melhores_pontos = None

for combinacao in product(product(x_vals, y_vals), repeat=k):
    pontos_array = np.array(combinacao)
    custo = funcao_objetivo(pontos_array.flatten())
    if custo < melhor_custo:
        melhor_custo = custo
        melhores_pontos = pontos_array

print("Ótimos novos pontos de coleta (Busca Exaustiva):")
print(melhores_pontos)
print(f"Custo total ótimo: {melhor_custo}")
