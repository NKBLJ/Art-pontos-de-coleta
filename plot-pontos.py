import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx  # Para adicionar o mapa de fundo

# Carregar os dados
df = pd.read_csv('pontos-coleta-com-coords.csv', sep=';', encoding='latin1')
df.sort_values(df.columns[1], inplace=True)

# Criar um gráfico com mapa de fundo
fig, ax = plt.subplots(figsize=(10, 10))

# Plotar os pontos no gráfico
ax.scatter(df['longitude'], df['latitude'], color='red', label='Pontos de coleta')

# Adicionar o mapa de fundo
ctx.add_basemap(
    ax,
    source=ctx.providers.OpenStreetMap.Mapnik,  # Fonte do mapa base
    crs="EPSG:4326"  # Sistema de coordenadas de latitude/longitude
)

# Configurar os rótulos e título
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Mapa de Pontos de Coleta')
ax.legend()

plt.savefig('map_plot_pontos_coleta.png')
plt.show()