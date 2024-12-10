import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx  # Para adicionar o mapa de fundo
from matplotlib.lines import Line2D  # Para personalizar a legenda

# Carregar os dados
df = pd.read_csv('agrupando-pontos/bairros-agrupados-local.csv', sep=';', encoding='latin1')
df.sort_values(df.columns[1], inplace=True)

# Escalar a população para ajustar o tamanho dos pontos
df['scaled_pop'] = df['População'] / df['População'].max() * 2000  # Ajuste o fator conforme necessário

# Criar um gráfico com mapa de fundo
fig, ax = plt.subplots(figsize=(10, 10))

# Plotar os pontos no gráfico, com tamanhos proporcionais à população
scatter = ax.scatter(
    df['longitude'],
    df['latitude'],
    s=df['scaled_pop'],  # Tamanho dos pontos
    color='red',
    alpha=0.6,  # Transparência dos pontos
)

# Adicionar o mapa de fundo
ctx.add_basemap(
    ax,
    source=ctx.providers.OpenStreetMap.Mapnik,  # Fonte do mapa base
    crs="EPSG:4326",  # Sistema de coordenadas de latitude/longitude
    zoom=10
)

# Criar uma legenda personalizada com tamanho fixo para o marcador
legend_marker = Line2D(
    [0], [0],
    marker='o',
    color='w',
    markerfacecolor='red',  # Cor dos pontos
    markersize=10,  # Tamanho fixo para a legenda
    label='Bairros'
)

# Adicionar a legenda manualmente com o marcador fixo
ax.legend(handles=[legend_marker])

# Configurar os rótulos e título
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Mapa de Bairros com Coordenadas')

# Salvar e exibir o gráfico
plt.savefig('map_plot.png')
plt.show()
