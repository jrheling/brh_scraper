# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime, timedelta
from sheetsu import SheetsuClient
from brh_scraper import settings

class SheetsuPipeline(object):


    """
    Return the best guess date of market close for a value scraped, based on scrape time.

    :param scrape_date: datetime of scraping (UTC)
    :returns: market close date, as string YYYY-MM-DD

    We're scraping for closing values, so assume that data was collected between market
    close on one day and open on the next. This is a convenience heuristic to guess at 
    that market date based on the scraping time.
    """
    @staticmethod
    def market_date(dt=None):
        if dt is None:
            # use now
            dt = datetime.utcnow()
        if dt.hour < 22:
            # it's early enough in the day that we'll assume this is yesterday's data
            # NOTE: running this at something like 4pm ET is not advised, but we're not
            #        stopping you
            dt = dt - timedelta(days=1)
        return "%s-%s-%s" % (dt.year, dt.month, dt.day)

    def __init__(self, row_limit=21, sheet_name="Sheet1"):
        self.client = None
        self.rowdata = {}
        self.ROW_LIMIT = row_limit # sheetsu free access only supports up to 50 rows / sheet
        self.sheet = sheet_name

    def trim_sheet(self):
        rows = self.client.read(sheet=self.sheet)
        rows_to_remove = None
        row_count = len(rows)
        print("************ %d rows:" % row_count)
        for i in range(0, row_count):
            print("%d: %s" % (i, rows[i]))
        if len(rows) >= self.ROW_LIMIT:
            rows_to_remove = len(rows) + 1 - self.ROW_LIMIT
            print("*************** removing %d" % rows_to_remove)

        # BEWARE - there's an implicit assumption that there's only one row per date
        #  - this code treats "Closing Date" like an index; if "Closing Date" isn't unique
        #  we'll overtrim (but in that case the data was probably junk anyway)
        if rows_to_remove is not None:
            vals_to_delete = []
            sorted_by_date = sorted(rows, key=lambda k: k["Closing Date"])
            for r in range(0, rows_to_remove):
                vals_to_delete.append(sorted_by_date[r]["Closing Date"])

            for close_date in vals_to_delete:
                self.client.delete(sheet=self.sheet, column="Closing Date",\
                        value=close_date, destroy="true")

    def open_spider(self, spider):
        self.client = SheetsuClient(settings.SHEETSU_API_URL, api_key=settings.SHEETSU_API_KEY,\
                                    api_secret=settings.SHEETSU_API_SECRET)
        self.trim_sheet()
        self.rowdata["Closing Date"] = self.market_date()


    def process_item(self, item, spider):
        name = item["name"][0]     ## improve - better to not load a list into the item 
        value = item["value"][0]
        #spider.logger.debug("name is %s", name)
        #spider.logger.debug("val is %s", value)
        self.rowdata[name] = value
        return item

    def close_spider(self, spider):
        self.client.create_many(sheet="Sheet1", *[self.rowdata])
