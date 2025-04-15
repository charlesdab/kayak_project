# Scrapy settings for booking_scraping project

BOT_NAME = "booking_scraping"

SPIDER_MODULES = ["booking_scraping.spiders"]
NEWSPIDER_MODULE = "booking_scraping.spiders"

# Désactiver robots.txt pour éviter que Scrapy soit bloqué par Booking
ROBOTSTXT_OBEY = False

# Activer Playwright pour Scrapy
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Activer le middleware Playwright pour gérer les requêtes JavaScript
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
    "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler": 543,  # ✅ Bon chemin
}


# Utiliser le bon réacteur pour Scrapy (nécessaire pour Playwright)
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Encodage des fichiers de sortie Scrapy
FEED_EXPORT_ENCODING = "utf-8"

# Configurer le délai entre les requêtes pour éviter d’être bloqué (facultatif)
DOWNLOAD_DELAY = 3

# Activer AutoThrottle pour limiter les requêtes selon la charge du site (facultatif)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Activer le cache HTTP pour éviter de recharger les pages inutilement (facultatif)
HTTPCACHE_ENABLED = False

# Définir un User-Agent pour éviter d’être bloqué par le site
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
FEEDS = {
    "hotels.csv": {
        "format": "csv",
        "encoding": "utf8",
        "overwrite": True,  # ✅ Permet d'écraser l'ancien fichier
    },
}
