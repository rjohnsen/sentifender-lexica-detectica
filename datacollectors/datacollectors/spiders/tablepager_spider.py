from pathlib import Path
import scrapy
import csv
import json

class TableindexerSpider(scrapy.Spider):
    name ="tablepager"

    def start_requests(self):        
        with open("table-source.csv", "r") as csv_in:
            reader = csv.reader(csv_in, delimiter=",")

            for row in reader:
                url = row[0]
                yield scrapy.Request(
                    url=url,
                    callback=self.parse
                )

    def parse(self, response):
        table_name = response.xpath("//h1/text()").get()

        with open(f"table-schemas/{table_name.lower()}.json", "w") as table_data_file:
            table_data = {
                "table_name": table_name,
                "fields": []
            }

            for row in response.xpath("//tr"):
                counter = 0

                field = {}

                for cell in row.xpath("td"):
                    if counter < 2:
                        text = cell.xpath("code/text()").get()

                        if counter == 0:
                            field["column_name"] = text
                        elif counter == 1: 
                            field["type"] = text
                    else:
                        field["description"] = cell.xpath("text()").get()

                    table_data["fields"].append(field)

                    counter += 1

            table_data_file.write(json.dumps(table_data))
            


