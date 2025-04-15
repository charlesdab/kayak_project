import pandas as pd

# Chemin du fichier CSV (à adapter si nécessaire)
csv_path = "C:/projects/scraping_booking/booking_scraping/data/processed/consolidated_data.csv"

# Charger uniquement les en-têtes du CSV
df = pd.read_csv(csv_path, nrows=0)

# Nom de la table
table_name = "consolidated_data"

# Générer la requête SQL pour créer la table
sql_create = f"CREATE TABLE public.{table_name} (\n"
sql_create += ",\n".join([f"    \"{col}\" TEXT" for col in df.columns])  # Ajout de guillemets pour éviter les conflits avec des noms de colonnes spéciaux
sql_create += "\n);"

# Enregistrer la requête dans un fichier SQL
with open("create_table.sql", "w", encoding="utf-8") as f:
    f.write(sql_create)

# Afficher la requête générée
print("✅ La requête SQL pour créer la table a été générée dans 'create_table.sql'.")
print("➡️ Ouvre ce fichier et exécute son contenu dans PostgreSQL.")
