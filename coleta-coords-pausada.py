import pandas as pd
import googlemaps
import os

def bairro_in_coord(bairro):
    endereco = f"bairro {bairro}, Teresina-PI, Brasil"
    gmaps = googlemaps.Client(key=os.environ['GOOGLE_MAPS_API_KEY'])
    geocode_result = gmaps.geocode(endereco)
    return geocode_result[0]['geometry']['location']

if __name__ == '__main__':
    # Arquivo de entrada e saída
    input_file = 'ibge-2022.csv'
    output_file = 'ibge-2022-com-coordenadas.csv'
    temp_file = 'ibge-2022-temporario.csv'

    # Carregar o arquivo original
    df = pd.read_csv(input_file, sep=';', encoding='latin1')
    df.sort_values(df.columns[1], inplace=True)
    df = df.iloc[1:]

    # Verificar se existe progresso salvo
    if os.path.exists(temp_file):
        df_temp = pd.read_csv(temp_file, sep=';', encoding='latin1')
        processed_indices = set(df_temp.index)  # Índices já processados
    else:
        df_temp = df.copy()
        df_temp['latitude'] = None
        df_temp['longitude'] = None
        processed_indices = set()

    # Processar as linhas restantes
    for index, row in df.iterrows():
        if index in processed_indices:
            continue  # Pula as linhas já processadas

        try:
            coords = bairro_in_coord(row[df.columns[0]])
            df_temp.at[index, 'latitude'] = coords['lat']
            df_temp.at[index, 'longitude'] = coords['lng']

            # Salvar progresso temporário
            df_temp.to_csv(temp_file, sep=';', encoding='latin1', index=False)
        except Exception as e:
            print(f"Erro ao processar {row[df.columns[0]]}: {e}")

    # Salvar o arquivo final
    df_temp.to_csv(output_file, sep=';', encoding='latin1', index=False)

    # Remover o arquivo temporário após finalizar
    if os.path.exists(temp_file):
        os.remove(temp_file)
