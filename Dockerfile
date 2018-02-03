# build image to scrape wsj.com data for BRH
# 
# background:
# - used Portia to (visually) define the scraper I wanted, and to validate that it worked
# - exported scraper from Portia as scrapy code

FROM scrapinghub/scrapinghub-stack-scrapy:1.1 as scrapy
RUN pip install dateparser
# FIXME: make this run as non-root
COPY scrapy_project /scrapy    
RUN python /scrapy/setup.py install
CMD cd /scrapy && scrapy crawl www.wsj.com
