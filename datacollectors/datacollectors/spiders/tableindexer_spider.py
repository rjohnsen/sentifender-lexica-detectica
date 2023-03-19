from pathlib import Path
from datetime import datetime

import scrapy

class Page(scrapy.Item):
    scraped = scrapy.Field()
    url = scrapy.Field()

class TableindexerSpider(scrapy.Spider):
    name ="tableindexer"

    def start_requests(self):        
        yield scrapy.Request(
            url="https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-schema-tables?view=o365-worldwide",
            callback=self.parse
        )

    def parse(self, response):
        hrefs = response.xpath("//a/@href")

        for href in hrefs:
            print(href.extract())





        """
        links = response.xpath("//a/@href").extract()

        for link in links:
            if "advanced-hunting" in link and ".md" not in link and "-table" in link:
                yield Page(
                    scraped=datetime.now(),
                    url=f"https://learn.microsoft.com/en-us/microsoft-365/security/defender/{link}"
                )

        """