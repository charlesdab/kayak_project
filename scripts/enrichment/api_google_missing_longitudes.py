import time
import googlemaps
import pandas as pd

# Remplacez par votre clé API Google Maps
api_key = "AIzaSyBWtHzMIHTTp9qsDJlsLevydambjmg_Ofg"  # Mettez votre clé API ici

# Initialiser le client Google Maps
gmaps = googlemaps.Client(key=api_key)

# Charger le fichier hotels.csv
hotels_df = pd.read_csv("../../booking_scraping/data/raw/hotels_scraped.csv")

# Fonction pour récupérer les coordonnées avec Google Maps
def get_coordinates(hotel_name, city_name):
    try:
        # Construire la requête complète
        location = gmaps.geocode(f"{hotel_name}, {city_name}")
        if location:
            lat = location[0]['geometry']['location']['lat']
            lon = location[0]['geometry']['location']['lng']
            return lat, lon
        else:
            return None, None
    except Exception as e:
        print(f"Erreur avec {hotel_name}: {e}")
        return None, None

# Filtrer les hôtels sans longitude
hotels_missing_longitude = hotels_df[hotels_df['longitude'].isna()]

# Appliquer la fonction de géocodage uniquement aux hôtels sans longitude
coordinates = []
for index, row in hotels_missing_longitude.iterrows():
    lat, lon = get_coordinates(row['hotel_name'], row['city'])
    coordinates.append((lat, lon))
    time.sleep(1)  # Respecter la limite de requêtes

# Ajouter les coordonnées récupérées au DataFrame
for i, (lat, lon) in enumerate(coordinates):
    hotels_missing_longitude.loc[hotels_missing_longitude.index[i], 'latitude'] = lat
    hotels_missing_longitude.loc[hotels_missing_longitude.index[i], 'longitude'] = lon

# Mettre à jour les données dans le DataFrame principal
hotels_df.update(hotels_missing_longitude)

# Sauvegarder le fichier mis à jour
hotels_df.to_csv("updated_hotels_google_maps.csv", index=False)

# Afficher les premiers résultats
print(hotels_df.head())
