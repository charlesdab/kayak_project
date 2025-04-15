input_file = "C:/projects/scraping_booking/booking_scraping/data/processed/consolidated_data.csv"
output_file = "C:/projects/scraping_booking/booking_scraping/data/processed/consolidated_data_utf8.csv"

with open(input_file, "r", encoding="ISO-8859-1") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
    f_out.write(f_in.read())

print("✅ Fichier converti en UTF-8 avec succès !")
