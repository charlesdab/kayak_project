from scrapy.crawler import CrawlerProcess
from booking_scraping.spiders.booking_spider import BookingSpider

process = CrawlerProcess()
process.crawl(BookingSpider)
process.start()
