import os
import pandas as pd

def transform_weather_to_wide(input_path, output_path):
    """
    Transforme le CSV météo (format long) en format wide en pivotant plusieurs colonnes.
    On suppose que le CSV contient au moins la colonne 'city' et les colonnes météo listées.
    """
    # Charger le CSV météo
    df_weather = pd.read_csv(input_path)
    
    # Liste des colonnes météo à pivoter (selon votre fichier)
    expected_cols = [
        "city", "temp", "temp_min", "temp_max", 
        "weather_main", "weather_description", 
        "humidity", "wind_speed", "wind_deg"
    ]
    
    # Vérifier que toutes les colonnes attendues sont présentes
    missing = [col for col in expected_cols if col not in df_weather.columns]
    if missing:
        raise ValueError(f"Les colonnes suivantes sont manquantes dans le CSV météo : {missing}")
    else:
        print("[INFO] Toutes les colonnes météo attendues sont présentes.")
    
    # Créer un indice de prévision pour chaque ville (en se basant sur l'ordre d'apparition)
    df_weather['forecast_index'] = df_weather.groupby('city').cumcount() + 1
    
    # Les colonnes à pivoter (toutes sauf "city")
    columns_to_pivot = expected_cols.copy()
    columns_to_pivot.remove("city")
    
    # Effectuer un pivot_table qui créera un MultiIndex pour les colonnes (variable, forecast_index)
    df_wide = df_weather.pivot_table(
        index="city",
        columns="forecast_index",
        values=columns_to_pivot,
        aggfunc="first"
    )
    
    # Aplatir le MultiIndex : ("temp", 1) -> "temp_1", ("temp", 2) -> "temp_2", etc.
    df_wide.columns = [f"{var}_{idx}" for var, idx in df_wide.columns]
    
    # Réinitialiser l'index pour avoir 'city' en colonne
    df_wide.reset_index(inplace=True)
    
    # Sauvegarder le CSV wide
    df_wide.to_csv(output_path, index=False)
    print(f"[OK] CSV météo transformé (wide) enregistré sous : {output_path}")
    return df_wide

def consolidate_data():
    # On suppose que ce script se trouve dans : C:\projects\scraping_booking\scripts\consolidation\
    # Remonter de deux niveaux pour atteindre la racine du projet
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    # Chemins des fichiers selon votre arborescence actuelle
    weather_long_path = os.path.join(base_dir, "booking_scraping", "data", "raw", "city_weather_forecast.csv")
    weather_wide_path = os.path.join(base_dir, "booking_scraping", "data", "processed", "city_weather_forecast_wide.csv")
    gps_path = os.path.join(base_dir, "booking_scraping", "data", "raw", "city_gps_coordinates.csv")
    hotels_path = os.path.join(base_dir, "booking_scraping", "data", "processed", "updated_hotels_google_maps.csv")
    output_consolidated = os.path.join(base_dir, "booking_scraping", "data", "processed", "consolidated_data.csv")
    
    # Transformation du CSV météo en format wide
    print("[INFO] Transformation du CSV météo en format wide...")
    df_weather_wide = transform_weather_to_wide(weather_long_path, weather_wide_path)
    
    # Charger les autres CSV
    df_gps = pd.read_csv(gps_path)  # Colonnes attendues: city, lat, lon
    df_hotels = pd.read_csv(hotels_path)  # Données hôtelières enrichies, incluant 'city'
    
    # Fusion des données hôtelières avec le CSV météo wide (jointure sur 'city')
    df_merged = pd.merge(df_hotels, df_weather_wide, on="city", how="left")
    
    # Fusion avec le CSV GPS pour ajouter les coordonnées de la ville
    df_merged = pd.merge(df_merged, df_gps[["city", "lat", "lon"]], on="city", how="left")
    df_merged.rename(columns={"lat": "city_lat", "lon": "city_lon"}, inplace=True)
    
    # Réorganiser les colonnes pour mettre en avant 'city', 'city_lat', 'city_lon'
    primary_cols = ["city", "city_lat", "city_lon"]
    remaining_cols = [col for col in df_merged.columns if col not in primary_cols]
    df_merged = df_merged[primary_cols + remaining_cols]
    
    # Enregistrer le CSV consolidé final
    df_merged.to_csv(output_consolidated, index=False)
    print(f"[OK] CSV consolidé enregistré sous : {output_consolidated}")

if __name__ == "__main__":
    consolidate_data()
