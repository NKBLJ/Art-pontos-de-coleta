import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from itertools import combinations

# Função para calcular o centro de gravidade ponderado
def centro_de_gravidade(latitudes, longitudes, populações):
    total_pop = np.sum(populações)
    lat_centro = np.sum(np.array(latitudes) * np.array(populações)) / total_pop
    lon_centro = np.sum(np.array(longitudes) * np.array(populações)) / total_pop
    return lat_centro, lon_centro

# Função para agrupar bairros próximos
def agrupar_bairros(df, k=4):
    coordenadas = df[['latitude', 'longitude']].to_numpy()
    populações = df['População'].to_numpy()

    # Matriz de distâncias
    dist_matrix = distance_matrix(coordenadas, coordenadas)

    # Lista para armazenar os grupos
    grupos = []
    visitados = set()

    for i, bairro in enumerate(df['Bairro']):
        if i in visitados:
            continue

        # Encontrar os k-1 bairros mais próximos
        proximos_indices = np.argsort(dist_matrix[i])[:k]
        proximos_indices = [idx for idx in proximos_indices if idx not in visitados]

        # Garantir que o grupo tenha no máximo k bairros
        if len(proximos_indices) > k:
            proximos_indices = proximos_indices[:k]

        # Marcar como visitados
        visitados.update(proximos_indices)

        # Criar o grupo
        grupo_bairros = df.iloc[proximos_indices]
        nomes = "-".join(grupo_bairros['Bairro'])
        pop_soma = grupo_bairros['População'].sum()
        lat_centro, lon_centro = centro_de_gravidade(
            grupo_bairros['latitude'], grupo_bairros['longitude'], grupo_bairros['População']
        )

        grupos.append({
            'Bairro': nomes,
            'População': pop_soma,
            'latitude': lat_centro,
            'longitude': lon_centro
        })

    return pd.DataFrame(grupos)

# Carregar os dados
df = pd.read_csv('../ibge-2022-com-coordenadas.csv', sep=';', encoding='latin')

# Agrupar os bairros e calcular o centro de gravidade
grupos_df = agrupar_bairros(df, k=4)

# Salvar o resultado em um novo arquivo CSV
grupos_df.to_csv('bairros_agrupados.csv', sep=';', encoding='latin', index=False)

# Exibir o resultado
print(grupos_df.head())
