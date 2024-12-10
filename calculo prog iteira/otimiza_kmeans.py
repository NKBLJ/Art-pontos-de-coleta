import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# Carregar dados
dados_bairros = pd.read_csv("../calculo prog iteira/bairros-agrupados-local.csv", sep=";", encoding='latin')
dados_pontos = pd.read_csv("../calculo prog iteira/pontos-coleta-com-coords.csv", sep=";", encoding='latin')

# Criar listas de bairros e suas coordenadas
bairros = dados_bairros[['Bairro', 'População', 'latitude', 'longitude']]
bairros['coordenadas'] = list(zip(bairros['latitude'], bairros['longitude']))

# Criar lista de pontos de coleta existentes
pontos_existentes = dados_pontos[['latitude', 'longitude']]
pontos_existentes = pontos_existentes.copy()
pontos_existentes['coordenadas'] = list(zip(pontos_existentes['latitude'], pontos_existentes['longitude']))

# Exemplo de dados: [(x, y), ...] representando as coordenadas dos bairros
local_bairros = bairros['coordenadas'].tolist()

# População de cada bairro
populacoes = dados_bairros['População'].tolist()

# Implementação do K-médias
kmeans = KMeans(n_clusters=3)
kmeans.fit(local_bairros, sample_weight=populacoes)

# Localizações dos 3 pontos ótimos
pontos = kmeans.cluster_centers_
print("Localizações dos pontos de instalação:", pontos)