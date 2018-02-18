#!/bin/bash

# intended to be used as the docker entrypiont, this script will use the settings
#  configured in the environment to finish the settings file, run the crawl job, and
#  verify success.
#
# Exit codes:
#
# 0 : success
# 1 : crawler didn't finish
# 2 : crawler finished, but didn't write the expected number of data columns
#
# This may be run from cron, so it has no output unless something went wrong.

# support structure for godawful error detecting hack below - needs to change whenever
#   the number of columns collected changes
EXPECTED_COL_COUNT=4

TGT="/scrapy/brh_scraper/settings.py"

#echo "configuring from ENV"

: ${SHEETSU_API_URL:?"Missing SHEETSU_API_URL in environment"}
: ${SHEETSU_API_KEY:?"Missing SHEETSU_API_KEY in environment"}
: ${SHEETSU_API_SECRET:?"Missing SHEETSU_API_SECRET in environment"}

echo "##### spider-specific settings" >> ${TGT}
echo "SHEETSU_API_URL = \"${SHEETSU_API_URL}\"">> ${TGT}
echo "SHEETSU_API_KEY = \"${SHEETSU_API_KEY}\"">> ${TGT}
echo "SHEETSU_API_SECRET = \"${SHEETSU_API_SECRET}\"">> ${TGT}

#echo "running scraper"
cd /scrapy/
TMPFILE=`mktemp`
scrapy crawl wsj_com 2>${TMPFILE}

## UGH! This is a pretty nasty and fragile way to catch errors, but scrapy
##   doesn't make this easy.
OUTPUT_SUMMARY=`grep "CLOSING SPIDER AFTER WRITING" ${TMPFILE}`
if [ $? -ne 0 ]
then
    echo "spider didn't finish - details follow"
    cat ${TMPFILE}
    exit 1
fi
COLUMN_COUNT=`echo $OUTPUT_SUMMARY | cut -d ' ' -f 9`
if [ $COLUMN_COUNT -ne $EXPECTED_COL_COUNT ]
then
    echo "Wrote $COLUMN_COUNT columns, but expected $EXPECTED_COL_COUNT"
    echo "Details:"
    cat ${TMPFILE}
    exit 2
fi
