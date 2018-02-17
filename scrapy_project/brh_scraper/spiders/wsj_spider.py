import scrapy
from scrapy.loader import ItemLoader
from brh_scraper.items import WSJData, WSJDataLoader

class WSJSpider(scrapy.Spider):
    name = "wsj_com"

    urls = {
        "http://www.wsj.com/mdc/public/page/2_3022-bondmkt.html" : {
            "Ryan 3-Month Treasury Index" : '//table[contains(@class,"mdcTable")]/descendant::td[contains(.,"3 Month Treasury")]/parent::*/td[contains(@class,"num")][1]/text()',
            "Ryan 3-Month Treasury Current" : '//table[contains(@class,"mdcTable")]/descendant::td[contains(.,"3 Month Treasury")]/parent::*/td[contains(@class,"num")][2]/text()'
            },
        "http://www.wsjf.com/mdc/public/page/2_3022-bondbnchmrk.html?mod=topnav_2_3022" : {
            "Barclays US Aggregate Index" : '//table[contains(@class,"mdcTable")]/descendant::td[contains(.,"Barclays Aggregate")]/parent::*/td[contains(@class,"pnum")][1]/text()'
            }
        }

    def start_requests(self):
        for u in self.urls:
            request = scrapy.Request(u, callback=self.parse)
            request.meta["vals"] = self.urls[u]
            yield request

    def parse(self, response):
        for v in response.meta["vals"]:
            ldr = WSJDataLoader(item=WSJData(), response=response)
            ldr.add_value('name', v)
            ldr.add_xpath('value', response.meta["vals"][v]) 
            yield ldr.load_item()

