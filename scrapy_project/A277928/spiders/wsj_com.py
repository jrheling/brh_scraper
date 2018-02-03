from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem


class Wsj(BasePortiaSpider):
    name = "www.wsj.com"
    allowed_domains = [u'www.wsj.com']
    start_urls = [
        u'http://www.wsj.com/mdc/public/page/2_3022-bondmkt.html',
        u'http://www.wsj.com/mdc/public/page/2_3022-bondbnchmrk.html?mod=topnav_2_3022']
    rules = [
        Rule(
            LinkExtractor(
                allow=(),
                deny=('.*')
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [[Item(PortiaItem,
                   None,
                   u'.mdcTable > tr:nth-child(4), .mdcTable > tbody > tr:nth-child(4)',
                   [Field(u'ryan_treas_3mo_index',
                          '.mdcTable > tr:nth-child(4) > td:nth-child(2) *::text, .mdcTable > tbody > tr:nth-child(4) > td:nth-child(2) *::text',
                          []),
                       Field(u'ryan_treas_3mo_curr',
                             '.mdcTable > tr:nth-child(4) > td:nth-child(3) *::text, .mdcTable > tbody > tr:nth-child(4) > td:nth-child(3) *::text',
                             [])]),
              Item(PortiaItem,
                   None,
                   u'.mdcTable > tr:nth-child(5), .mdcTable > tbody > tr:nth-child(5)',
                   [Field(u'barclays_us_aggreg_index',
                          '.mdcTable > tr:nth-child(5) > td:nth-child(2) *::text, .mdcTable > tbody > tr:nth-child(5) > td:nth-child(2) *::text',
                          [])])]]
