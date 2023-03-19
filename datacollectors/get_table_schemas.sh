#!/usr/bin/env bash

echo "Getting Table Schemas from Microsoft"
rm output/*.json
scrapy crawl tableindexer -o output/links.json
scrapy crawl tablepager -o output/schemas.json
