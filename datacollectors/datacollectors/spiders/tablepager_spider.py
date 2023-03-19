from pathlib import Path
from datetime import datetime
import scrapy
import csv
import json

class Table(scrapy.Item):
    scraped = scrapy.Field()
    name = scrapy.Field()
    fields = scrapy.Field()

class Field(scrapy.Item):
    name = scrapy.Field()
    definition = scrapy.Field()
    description = scrapy.Field()

class TableindexerSpider(scrapy.Spider):
    name ="tablepager"

    def start_requests(self):        
        with open("output/links.json", "r") as linksfile:
            for link in json.load(linksfile):
                yield scrapy.Request(
                    url=link["url"],
                    callback=self.parse
                )

    def parse(self, response):
        table = Table()
        table["scraped"] = datetime.now()
        table["name"] = response.xpath("//h1/text()").get()
        table["fields"] = []

        for row in response.xpath("//tr"):
            field = Field()
            counter = 0

            for cell in row.xpath("td"):

                if counter < 2:
                    text = cell.xpath("code/text()").get()

                    if counter == 0:
                        field["name"] = text
                    elif counter == 1: 
                        field["definition"] = text
                else:
                    field["description"] = cell.xpath("text()").get()

                table["fields"].append(field)

                counter += 1

        yield table
            


