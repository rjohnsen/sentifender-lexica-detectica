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
        urls = [
            "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-aadsignineventsbeta-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-aadspnsignineventsbeta-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-alertevidence-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-alertinfo-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-behaviorentities-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-behaviorinfo-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-cloudappevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-cloudauditevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-cloudprocessevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-datasecuritybehaviors-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-datasecurityevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicebaselinecomplianceassessment-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicebaselinecomplianceassessmentkb-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicebaselinecomplianceprofiles-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicefilecertificateinfo-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicefileevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceimageloadevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceinfo-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicelogonevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicenetworkevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicenetworkinfo-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceregistryevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmbrowserextensions-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmbrowserextensionskb-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmcertificateinfo-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmhardwarefirmware-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvminfogathering-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvminfogatheringkb-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmsecureconfigurationassessment-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmsecureconfigurationassessmentkb-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmsoftwareevidencebeta-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmsoftwareinventory-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmsoftwarevulnerabilities-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicetvmsoftwarevulnerabilitieskb-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-emailattachmentinfo-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-emailevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-emailpostdeliveryevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-emailurlinfo-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-exposuregraphedges-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-exposuregraphnodes-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-identitydirectoryevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-identityinfo-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-identitylogonevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-identityqueryevents-table",
"https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-urlclickevents-table"
        ]

        for url in urls:
            yield scrapy.Request(
                url=url,
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
