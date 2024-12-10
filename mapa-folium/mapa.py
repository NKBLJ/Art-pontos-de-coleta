import pandas as pd
from folium.plugins import MarkerCluster
import folium

# df = pd.read_csv('../ibge-2022-com-coordenadas.csv', sep=';', encoding='latin1')
df = pd.read_csv('../pontos-coleta-com-coords.csv', sep=';', encoding='latin1')

mapa = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)

# Usar MarkerCluster para agrupar pontos próximos (opcional)
marker_cluster = MarkerCluster().add_to(mapa)

# Adicionar marcadores ao mapa
for _, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['endereço']
    ).add_to(marker_cluster)

# Exibir o mapa
mapa.save("mapa-coleta.html")