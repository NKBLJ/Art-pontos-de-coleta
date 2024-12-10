import pandas as pd
import pulp
import numpy as np
from geopy.distance import geodesic

# Carregar dados
dados_bairros = pd.read_csv("../calculo prog iteira/bairros-agrupados-local.csv", sep=";", encoding='latin')
dados_pontos = pd.read_csv("../calculo prog iteira/pontos-coleta-com-coords.csv", sep=";", encoding='latin')


# Função para calcular a distância geodésica (em km) entre dois pontos geográficos
def calcular_distancia(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# Criar listas de bairros e suas coordenadas
bairros = dados_bairros[['Bairro', 'População', 'latitude', 'longitude']]
bairros['coordenadas'] = list(zip(bairros['latitude'], bairros['longitude']))

# Criar lista de pontos de coleta existentes
pontos_existentes = dados_pontos[['latitude', 'longitude']]
pontos_existentes = pontos_existentes.copy()
pontos_existentes['coordenadas'] = list(zip(pontos_existentes['latitude'], pontos_existentes['longitude']))

# Número de novos pontos de coleta a serem adicionados
num_novos_pontos = 4

# Inicializar o problema de otimização
prob = pulp.LpProblem("Otimização_Localização_Novos_Pontos", pulp.LpMinimize)

# Variáveis de decisão: coordenadas dos novos pontos de coleta (latitude e longitude)
novos_latitudes = [pulp.LpVariable(f"Lat_Novo_{i}", lowBound=-90, upBound=90) for i in range(num_novos_pontos)]
novos_longitudes = [pulp.LpVariable(f"Lon_Novo_{i}", lowBound=-180, upBound=180) for i in range(num_novos_pontos)]

# Combinar os novos pontos com os existentes para calcular a distância
def distancia_mais_proxima(bairro, novos_pontos):
    # Calcula a menor distância entre o bairro e todos os pontos (existentes + novos)
    distancias = [
        calcular_distancia(bairro['latitude'], bairro['longitude'], ponto[0], ponto[1])
        for ponto in pontos_existentes['coordenadas']
    ]
    distancias += [
        calcular_distancia(bairro['latitude'], bairro['longitude'], novos_pontos[i][0], novos_pontos[i][1])
        for i in range(num_novos_pontos)
    ]
    return min(distancias)


# Função objetivo: minimizar a distância total ponderada pela população
prob += pulp.lpSum(
    distancia_mais_proxima(bairro, [(novos_latitudes[i], novos_longitudes[i]) for i in range(num_novos_pontos)]) * bairro['População']
    for _, bairro in bairros.iterrows()
)

# Resolver o problema
prob.solve()


# Resultados
if pulp.LpStatus[prob.status] == 'Optimal':
    print("Solução ótima encontrada!\n")
    for i in range(num_novos_pontos):
        print(f"Novo Ponto {i+1}: Latitude = {pulp.value(novos_latitudes[i])}, Longitude = {pulp.value(novos_longitudes[i])}")
else:
    print("Não foi encontrada uma solução ótima.")
