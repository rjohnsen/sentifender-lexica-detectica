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
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-aadsignineventsbeta-table?view=o365-worldwide,learn.microsoft.com,AADSignInEventsBeta",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-aadspnsignineventsbeta-table?view=o365-worldwide,learn.microsoft.com,AADSpnSignInEventsBeta",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-alertevidence-table?view=o365-worldwide,learn.microsoft.com,AlertEvidence",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-alertinfo-table?view=o365-worldwide,learn.microsoft.com,AlertInfo",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-cloudappevents-table?view=o365-worldwide,learn.microsoft.com,CloudAppEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-deviceevents-table?view=o365-worldwide,learn.microsoft.com,DeviceEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicefilecertificateinfo-table?view=o365-worldwide,learn.microsoft.com,DeviceFileCertificateInfo",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicefileevents-table?view=o365-worldwide,learn.microsoft.com,DeviceFileEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-deviceimageloadevents-table?view=o365-worldwide,learn.microsoft.com,DeviceImageLoadEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-deviceinfo-table?view=o365-worldwide,learn.microsoft.com,DeviceInfo",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicelogonevents-table?view=o365-worldwide,learn.microsoft.com,DeviceLogonEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicenetworkevents-table?view=o365-worldwide,learn.microsoft.com,DeviceNetworkEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicenetworkinfo-table?view=o365-worldwide,learn.microsoft.com,DeviceNetworkInfo",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-deviceprocessevents-table?view=o365-worldwide,learn.microsoft.com,DeviceProcessEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-deviceregistryevents-table?view=o365-worldwide,learn.microsoft.com,DeviceRegistryEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicetvmhardwarefirmware-table?view=o365-worldwide,learn.microsoft.com,DeviceTvmHardwareFirmware",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicetvminfogathering-table?view=o365-worldwide,learn.microsoft.com,DeviceTvmInfoGathering",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicetvminfogatheringkb-table?view=o365-worldwide,learn.microsoft.com,DeviceTvmInfoGatheringKB",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicetvmsecureconfigurationassessment-table?view=o365-worldwide,learn.microsoft.com,DeviceTvmSecureConfigurationAssessment",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicetvmsecureconfigurationassessmentkb-table?view=o365-worldwide,learn.microsoft.com,DeviceTvmSecureConfigurationAssessmentKB",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicetvmsoftwareevidencebeta-table?view=o365-worldwide,learn.microsoft.com,DeviceTvmSoftwareEvidenceBeta",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicetvmsoftwareinventory-table?view=o365-worldwide,learn.microsoft.com,DeviceTvmSoftwareInventory",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicetvmsoftwarevulnerabilities-table?view=o365-worldwide,learn.microsoft.com,DeviceTvmSoftwareVulnerabilities",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-devicetvmsoftwarevulnerabilitieskb-table?view=o365-worldwide,learn.microsoft.com,DeviceTvmSoftwareVulnerabilitiesKB",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-emailattachmentinfo-table?view=o365-worldwide,learn.microsoft.com,EmailAttachmentInfo",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-emailevents-table?view=o365-worldwide,learn.microsoft.com,EmailEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-emailpostdeliveryevents-table?view=o365-worldwide,learn.microsoft.com,EmailPostDeliveryEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-emailurlinfo-table?view=o365-worldwide,learn.microsoft.com,EmailUrlInfo",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-identitydirectoryevents-table?view=o365-worldwide,learn.microsoft.com,IdentityDirectoryEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-identityinfo-table?view=o365-worldwide,learn.microsoft.com,IdentityInfo",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-identitylogonevents-table?view=o365-worldwide,learn.microsoft.com,IdentityLogonEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-identityqueryevents-table?view=o365-worldwide,learn.microsoft.com,IdentityQueryEvents",
            "https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-urlclickevents-table?view=o365-worldwide,learn.microsoft.com,UrlClickEvents"
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
