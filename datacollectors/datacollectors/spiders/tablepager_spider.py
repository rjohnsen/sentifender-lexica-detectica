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
        table["fields"] = []

        table["name"] = response.css("div.content").xpath("h1/text()").get()

        for row in response.css("div.content").xpath("//table/tbody/tr"):
            tds = row.xpath("td")
            
            table["fields"].append(Field(
                name=tds[0].xpath("code/text()").get(),
                definition=tds[1].xpath("code/text()").get(),
                description=tds[2].xpath("text()").get()
            ))

        return table
