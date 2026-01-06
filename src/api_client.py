import requests
import pandas as pd
import time
from settings import PARTENAIRE_FILE, PARTENAIRE_GEO_CSV, API_DELAY

API_URL = "https://api-adresse.data.gouv.fr/search/"

def geocode_address(address, city, postcode):
    query = f"{address} {postcode} {city}"
    try:
        response = requests.get(API_URL, params={"q": query, "limit": 1}, timeout=10)
        response.raise_for_status()
        data = response.json()
        features = data.get("features")
        if features:
            coords = features[0]["geometry"]["coordinates"]
            return coords[0], coords[1]
    except requests.RequestException as e:
        print(f"erreur API pour {query} : {e}")
    return None, None

def geocode_csv(input_file=PARTENAIRE_FILE, output_file=PARTENAIRE_GEO_CSV):
    df = pd.read_csv(input_file)
    longitudes = []
    latitudes = []

    for i, row in df.iterrows():
        lon, lat = geocode_address(row['adresse'], row['ville'], row['code_postal'])
        longitudes.append(lon)
        latitudes.append(lat)
        print(f"{i+1}/{len(df)} géocodé : {row['nom_librairie']}")
        time.sleep(API_DELAY)

    df['longitude'] = longitudes
    df['latitude'] = latitudes

    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"fichier géocodé créé : {output_file}")

if __name__ == "__main__":
    geocode_csv()
