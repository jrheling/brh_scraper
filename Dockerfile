# build image to scrape wsj.com data for BRH
# 

FROM scrapinghub/scrapinghub-stack-scrapy:1.1 as scrapy
# here for build/debug work
#RUN apt-get install less
#COPY /vimrc.txt /root/.vimrc

RUN pip install sheetsu
RUN echo US/Central > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN mkdir /scrapy
COPY scrapy_project/brh_scraper /scrapy/brh_scraper/
COPY scrapy_project/scrapy.cfg /scrapy/


#VOLUME /scrapy
#RUN pip install dateparser
# FIXME: make this run as non-root?
#COPY scrapy_project /scrapy
#RUN python /scrapy/setup.py install
#CMD cd /scrapy && scrapy crawl www.wsj.com
