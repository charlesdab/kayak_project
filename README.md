# Projet Kayak – Bloc 1 : Infrastructure de données

## 🎯 Objectif du projet

L’objectif de ce projet est de construire une infrastructure de données pour recommander les meilleures destinations touristiques en France, selon la météo et la qualité des hôtels.

J'ai conçu un pipeline complet de collecte, transformation et stockage des données pour 35 villes françaises, dans un cadre pédagogique.

---

## 🧩 Étapes réelles du pipeline

### 1. 📍 Liste des villes à analyser
- Liste définie manuellement dans `booking_scraping/data/raw/cities.txt`

### 2. 🔍 Récupération des coordonnées GPS
- Script : `scripts/extraction/get_city_gps.py`
- Résultat : `booking_scraping/data/processed/city_gps_coordinates.csv`

### 3. ☁️ Récupération des données météo (prévision sur 5 jours)
- Script : `scripts/extraction/get_city_weather.py`
- Résultat brut : `booking_scraping/data/raw/city_weather_forecast.csv`
- Résultat final (wide format) : `booking_scraping/data/processed/city_weather_forecast_wide.csv`

### 4. 🏨 Scraping des hôtels depuis Booking.com
- Crawler Scrapy avec Playwright : `booking_scraping/spiders/booking_spider.py`
- Résultat : `booking_scraping/data/raw/hotels_scraped.csv`
- Enrichissement : coordonnées GPS, notes utilisateurs
- Résultat enrichi : `booking_scraping/data/processed/updated_hotels_google_maps.csv`

### 5. 📌 Enrichissement des hôtels sans coordonnées GPS
- Script : `scripts/enrichment/api_google_missing_longitudes.py`

### 6. 🔗 Consolidation des données
- Script : `scripts/consolidation/joint_data.py`
- Résultat : `booking_scraping/data/processed/consolidated_data_utf8.csv`

### 7. 🗃️ Stockage dans une base relationnelle (Data Warehouse)
- Script de création de la table : `database/create_table.sql`
- Script de chargement depuis S3 : `database/download_from_s3.py`

---

## 📦 Résultat final

- Un fichier CSV complet et encodé en UTF-8 avec météo + hôtels : `consolidated_data_utf8.csv`
- Une base SQL interrogeable
- Cartes générées dans le notebook : météo, hôtels, destinations recommandées

---

## 🔐 RGPD & Éthique du scraping

- Aucune donnée personnelle n’a été collectée.
- Les données météo et géographiques proviennent d’APIs publiques.
- Le scraping de Booking.com a été réalisé dans un cadre strictement pédagogique.
- ⚠️ Certaines pages utilisées (notamment les fiches d’hôtels) sont listées comme interdites dans le fichier `robots.txt` du site.
- J’ai limité le volume de requêtes pour ne pas impacter le site.

---

## 📁 Organisation du projet

- `notebooks/kayak_exploration_final.ipynb` → analyse et visualisations
- `scripts/` → extraction, enrichissement, consolidation, conversion
- `booking_scraping/` → spider Scrapy, données raw et processed
- `database/` → table SQL + chargement
- `images/` → captures pour vérification

---

## 🔗 Lien GitHub

👉 https://github.com/charlesdab/kayak_project
"""
