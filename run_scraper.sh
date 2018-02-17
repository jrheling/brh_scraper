#!/bin/bash

TGT="/scrapy/brh_scraper/settings.py"

echo "configuring from ENV"

: ${SHEETSU_API_URL:?"Missing SHEETSU_API_URL in environment"}
: ${SHEETSU_API_KEY:?"Missing SHEETSU_API_KEY in environment"}
: ${SHEETSU_API_SECRET:?"Missing SHEETSU_API_SECRET in environment"}

echo "##### spider-specific settings" >> ${TGT}
echo "SHEETSU_API_URL = \"${SHEETSU_API_URL}\"">> ${TGT}
echo "SHEETSU_API_KEY = \"${SHEETSU_API_KEY}\"">> ${TGT}
echo "SHEETSU_API_SECRET = \"${SHEETSU_API_SECRET}\"">> ${TGT}

echo "running scraper"
cd /scrapy/
scrapy crawl wsj_com
if [ $? -ne 0 ]
then
    echo "failed"
fi
exit $?
