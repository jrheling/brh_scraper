#!/bin/sh

TGT="/scrapy/brh_scraper_settings.py"

echo "configuring from ENV"
# FIXME: add empty var checking
echo "##### spider-specific settings" >> ${TGT}
echo "SHEETSU_API_URL = \"$(SHEETSU_API_URL)\"">> ${TGT}
