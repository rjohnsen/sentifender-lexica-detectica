from pathlib import Path
import scrapy
import csv

class TableindexerSpider(scrapy.Spider):
    name ="tableindexer"

    def start_requests(self):        
        yield scrapy.Request(
            url="https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-schema-tables?view=o365-worldwide",
            callback=self.parse
        )

    def parse(self, response):
        links = response.xpath("//a/@href").extract()

        with open("table-source.csv", "w") as csv_out:
            writer = csv.writer(csv_out, delimiter=',')

            for link in links:
                if "advanced-hunting" in link and ".md" not in link and "table" in link:
                    writer.writerow([f"https://learn.microsoft.com/en-us/microsoft-365/security/defender/{link}"])