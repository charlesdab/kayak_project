import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

# Charger la liste des villes avec leurs coordonnées GPS depuis city_gps_coordinates.csv
gps_file = "../data/processed/city_gps_coordinates.csv"
if not os.path.exists(gps_file):
    raise FileNotFoundError(f"Le fichier {gps_file} est introuvable.")

df = pd.read_csv(gps_file)

# Vérifier la présence des colonnes nécessaires
if not {'lat', 'lon'}.issubset(df.columns):
    raise ValueError("Le fichier CSV doit contenir les colonnes 'lat' et 'lon'.")

# Clé API OpenWeatherMap (mettre votre clé ici ou utiliser une variable d'environnement)
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")


# URL de base de l'API OpenWeatherMap pour les prévisions à 5 jours
url_base = "http://api.openweathermap.org/data/2.5/forecast"

# DataFrame pour stocker les résultats
weather_data = []

# Itérer sur les lignes du DataFrame et faire des requêtes à l'API OpenWeatherMap
for index, row in df.iterrows():
    lat, lon = row['lat'], row['lon']
    city = row['city']

    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,  # Ta clé API
        'units': "metric",  # Température en °C
        'lang': 'fr',  # Langue des résultats
    }

    try:
        response = requests.get(url_base, params=params, timeout=10)
        response.raise_for_status()  # Vérifie si la requête est réussie

        weather_json = response.json()
        # Extraire les informations des prévisions à 5 jours
        for forecast in weather_json['list']:
            weather_data.append({
                'city': city,
                'lat': lat,
                'lon': lon,
                'date_time': forecast['dt_txt'],  # Date et heure de la prévision
                'temp': forecast['main']['temp'],
                'temp_min': forecast['main']['temp_min'],
                'temp_max': forecast['main']['temp_max'],
                'weather_main': forecast['weather'][0]['main'],
                'weather_description': forecast['weather'][0]['description'],
                'humidity': forecast['main']['humidity'],
                'wind_speed': forecast['wind']['speed'],
                'wind_deg': forecast['wind']['deg']
            })
    except requests.exceptions.RequestException as e:
        print(f"Erreur API pour {city} (lat={lat}, lon={lon}): {e}")

    time.sleep(2)  # Pause pour éviter d’être bloqué

# Convertir en DataFrame et sauvegarder dans le bon dossier
weather_df = pd.DataFrame(weather_data)
output_file = "../data/processed/city_weather_forecast.csv"
weather_df.to_csv(output_file, index=False)

print(f"Les données météo ont été enregistrées dans '{output_file}'.")
