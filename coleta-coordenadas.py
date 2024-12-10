# Abrir o CSV em pandas
import pandas as pd
import googlemaps
import os

def bairro_in_coord(bairro):
    endereco = f"{bairro}, Teresina-PI"
    gmaps = googlemaps.Client(key=os.environ['GOOGLE_MAPS_API_KEY'])
    geocode_result = gmaps.geocode(endereco)

    return geocode_result[0]['geometry']['location']

def add_coordinates(row):
    coords = bairro_in_coord(row[df.columns[1]])
    return pd.Series([coords['lat'], coords['lng']], index=['latitude', 'longitude'])


if __name__ == '__main__':

    df = pd.read_csv('pontos-reciclagem.csv', sep=';', encoding='latin1')
    # Sort the DataFrame by the second column
    # df.sort_values(df.columns[1], inplace=False)
    # df = df.iloc[:1]

    for index, row in df.iterrows():
        print(row)
        df[['latitude', 'longitude']] = df.apply(add_coordinates, axis=1)

    # Save the DataFrame to a new CSV file in latin1 encoding
    df.to_csv('pontos-coleta-com-coords.csv', sep=';', encoding='latin1', index=False)

    # print(bairro_in_coord("R. Gov. Raimundo Artur Vasconcelos, 4838 - Itaperu"))