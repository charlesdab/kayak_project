import boto3

# Nom de ton bucket S3
bucket_name = "bucket-projet-kayak-charles"

# Clés S3 pour chaque fichier
s3_file_key_1 = "city_weather_forecast.csv"
s3_file_key_2 = "city_gps_coordinates.csv"
s3_file_key_3 = "hotels.csv"

# Emplacement local pour enregistrer les fichiers (modifié vers database)
local_file_1 = "C:/projects/scraping_booking/database/city_weather_forecast.csv"
local_file_2 = "C:/projects/scraping_booking/database/city_gps_coordinates.csv"
local_file_3 = "C:/projects/scraping_booking/database/hotels.csv"

# Connexion à S3
s3 = boto3.client("s3")

# Télécharger les fichiers depuis S3 vers ton dossier local
s3.download_file(bucket_name, s3_file_key_1, local_file_1)
print(f"✅ Fichier {s3_file_key_1} téléchargé avec succès dans {local_file_1}")

s3.download_file(bucket_name, s3_file_key_2, local_file_2)
print(f"✅ Fichier {s3_file_key_2} téléchargé avec succès dans {local_file_2}")

s3.download_file(bucket_name, s3_file_key_3, local_file_3)
print(f"✅ Fichier {s3_file_key_3} téléchargé avec succès dans {local_file_3}")
