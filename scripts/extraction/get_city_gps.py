
import pandas as pd
import requests
import time

# Charger la liste des villes depuis le fichier cities.txt dans data/raw/
with open("../data/raw/cities.txt", "r", encoding="utf-8") as f:
    cities = [line.strip() for line in f.readlines()]

# URL de l'API Nominatim
url = "https://nominatim.openstreetmap.org/search"

# En-tête User-Agent plus crédible pour éviter le blocage
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

# Liste pour stocker les résultats des coordonnées GPS
gps_data = []

# Boucle sur chaque ville pour récupérer ses coordonnées GPS
for city in cities:
    payload = {'q': city, 'format': 'json', 'limit': 1}  # On récupère seulement le premier résultat

    try:
        response = requests.get(url, params=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Vérifie si la requête est réussie

        data = response.json()
        if len(data) > 0:
            gps_data.append({
                "city": city,
                "lat": data[0]['lat'],
                "lon": data[0]['lon']
            })
        else:
            print(f"Aucune coordonnée trouvée pour {city}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête pour {city}: {e}")

    time.sleep(3)  # Pause plus longue pour éviter d’être bloqué

# Convertir en DataFrame et sauvegarder dans le bon dossier
gps_df = pd.DataFrame(gps_data)
output_path = "../data/processed/city_gps_coordinates.csv"
gps_df.to_csv(output_path, index=False)

print(f"Les coordonnées GPS ont été enregistrées dans '{output_path}'.")
