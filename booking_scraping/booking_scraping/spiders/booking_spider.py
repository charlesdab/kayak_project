import scrapy
import re
import logging

class BookingSpider(scrapy.Spider):
    name = "booking_spider"
    allowed_domains = ["booking.com"]

    cities = [
        "Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens", "Lille",
        "Strasbourg", "Chateau du Haut Koenigsbourg", "Colmar", "Eguisheim", "Besancon", "Dijon",
        "Annecy", "Grenoble", "Lyon", "Gorges du Verdon", "Bormes les Mimosas", "Cassis", "Marseille",
        "Aix en Provence", "Avignon", "Uzes", "Nimes", "Aigues Mortes", "Saintes Maries de la mer",
        "Collioure", "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz", "Bayonne", "La Rochelle"
    ]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "DOWNLOAD_DELAY": 3,
        "AUTOTHROTTLE_ENABLED": True,
        "FEED_EXPORT_ENCODING": "utf-8",
        "LOG_LEVEL": "INFO",
    }

    def start_requests(self):
        """Lance les requêtes pour toutes les villes"""
        for city in self.cities:
            search_url = f"https://www.booking.com/searchresults.html?ss={city.replace(' ', '%20')}&checkin=2025-03-05&checkout=2025-03-09&group_adults=2&group_children=0&no_rooms=1"
            self.logger.info(f"🔍 Recherche des hôtels à {city}...")
            yield scrapy.Request(url=search_url, callback=self.parse, meta={"city": city})

    def parse(self, response):
        """Récupère la liste des hôtels sur la page de résultats"""
        city = response.meta["city"]
        hotels = response.css("div[data-testid='property-card']")
        self.logger.info(f"🏙️ {city} - Hôtels trouvés : {len(hotels)}")

        if not hotels:
            self.logger.warning(f"⚠️ Aucun hôtel trouvé pour {city}. Vérifiez l'URL ou la ville.")

        for hotel in hotels:
            name = hotel.css("div[data-testid='title']::text").get(default="N/A").strip()
            url = response.urljoin(hotel.css("a[data-testid='title-link']::attr(href)").get(default=""))
            price = hotel.css("span[data-testid='price-and-discounted-price']::text").get(default="N/A").strip()

            self.logger.info(f"🏨 Hôtel trouvé : {name} - Prix: {price}")

            yield scrapy.Request(
                url=url,
                callback=self.parse_hotel,
                meta={"city": city, "hotel_name": name, "hotel_url": url, "price": price},
                errback=self.errback
            )

    async def parse_hotel(self, response):
        """Récupère les détails de chaque hôtel"""
        city = response.meta["city"]
        hotel_name = response.meta["hotel_name"]
        hotel_url = response.meta["hotel_url"]
        price = response.meta["price"]

        # Extraction des coordonnées GPS avec fallback
        script_content = response.xpath("//script[contains(text(), 'b_map_center_latitude')]/text()").get()
        latitude = re.search(r"b_map_center_latitude\s*=\s*([\d\.]+);", script_content) if script_content else None
        longitude = re.search(r"b_map_center_longitude\s*=\s*([\d\.]+);", script_content) if script_content else None
        latitude = latitude.group(1) if latitude else "N/A"
        longitude = longitude.group(1) if longitude else "N/A"

        if latitude == "N/A" or longitude == "N/A":
            self.logger.warning(f"⚠️ Coordonnées non trouvées pour {hotel_name}, tentative alternative...")

        # Extraction alternative pour la note de l'hôtel
        rating = response.css("div.a3b8729ab1.d86cee9b25::text").get()
        if not rating:
            rating = response.css("div.b5cd09854e.d10a6220b4::text").get()
        if not rating:
            rating = response.css("span.a3b8729ab1.d86cee9b25::text").get()
        rating = rating.strip() if rating else "N/A"

        if rating == "N/A":
            self.logger.warning(f"⚠️ Note non trouvée pour {hotel_name}, vérifiez le format CSS.")

        # Extraction de la description
        description = response.css("p.a53cbfa6de.b3efd73f69::text").get(default="N/A").strip()

        self.logger.info(f"📍 Coordonnées GPS pour {hotel_name} : {latitude}, {longitude}")
        self.logger.info(f"⭐ Note : {rating}")
        self.logger.info(f"📜 Description : {description[:100]}...")

        yield {
            "city": city,
            "hotel_name": hotel_name,
            "hotel_url": hotel_url,
            "latitude": latitude,
            "longitude": longitude,
            "rating": rating,
            "description": description,
            "price": price
        }

    async def errback(self, failure):
        """Gestion des erreurs"""
        self.logger.error(repr(failure))
