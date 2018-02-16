# build image to scrape wsj.com data for BRH
# 

FROM scrapinghub/scrapinghub-stack-scrapy:1.1 as scrapy

RUN pip install sheetsu
RUN echo US/Central > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN mkdir /scrapy
COPY scrapy_project/brh_scraper /scrapy/brh_scraper/
COPY scrapy_project/scrapy.cfg /scrapy/
COPY run_scraper.sh /scrapy/

# temp hack until my PR is merged
RUN git clone https://github.com/jrheling/sheetsu-python.git --branch add_destroy --single-branch my_sheetsu
RUN rm -rf /usr/local/lib/python2.7/site-packages/sheetsu
RUN mv my_sheetsu/sheetsu /usr/local/lib/python2.7/site-packages/


#ENTRYPOINT ["/scrapy/run_scraper.sh"]

