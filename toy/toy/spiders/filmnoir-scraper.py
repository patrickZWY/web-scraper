"""
import scrapy
import schedule
import time
from scrapy import cmdline

# spider
class FilmNoirSpider(scrapy.Spider):
    name = 'film_noir'
    # starting url
    start_urls = ["https://en.wikipedia.org/wiki/Category:Film_noir"]

    # user agent, download delay, concurrent requests
    custom_settings = {
        'USER AGENT': 'Mozilla/5.0 (Windows NT 10.0;Win64) \
        AppleWebkit/537.36 (KHTML, like Gecko) \
        Chrome/89.0.4389.82 Safari/537.36',
        'DOWNLOAD_DELAY' : 1,
        'CONCURRENT_REQUESTS' : 1,
        'RETRY_TIMES' : 3,
        'RETRY_HTTP_CODES' : [500, 503, 504, 400, 403, 404, 408],
        'DOWNLOADER_MIDDLEWARES' : {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    }
    }

    def parse(self, response):
        films = response.css("div#mw-pages div.mw-category div.mw-category-group ul li")
        for film in films:
            title = film.css('a::text').get()
            url = film.css('a::attr(href)').get()
            if url:
                url = response.urljoin(url)
                yield scrapy.Request(url, callback=self.parse_film, meta={'title': title})

    def parse_film(self, response):
        title = response.meta['title']
        year = response.css('table.infobox th:contains("Release date") + td::text').get()

        if year:
            year = ''.join(filter(str.isdigit, year[:4]))
        else:
            year = 'Unknown'

        yield {
            'title': title,
            'year': year
        }


# run spider
def crawl_filmnoir():
    cmdline.execute("scrapy crawl film_noir".split())

schedule.every(1).minute.do(crawl_filmnoir)

while True:
    schedule.run_pending()
    time.sleep(1)
"""
import scrapy
import asyncio
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# spider
class FilmNoirSpider(scrapy.Spider):
    name = 'film_noir'
    # starting url
    start_urls = ["https://en.wikipedia.org/wiki/Category:Film_noir"]

    # user agent, download delay, concurrent requests
    custom_settings = {
        'USER AGENT': 'Mozilla/5.0 (Windows NT 10.0;Win64) \
        AppleWebkit/537.36 (KHTML, like Gecko) \
        Chrome/89.0.4389.82 Safari/537.36',
        'DOWNLOAD_DELAY' : 1,
        'CONCURRENT_REQUESTS' : 1,
        'RETRY_TIMES' : 3,
        'RETRY_HTTP_CODES' : [500, 503, 504, 400, 403, 404, 408],
        'DOWNLOADER_MIDDLEWARES' : {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    }
    }

    async def parse(self, response):
        films = response.css("div#mw-pages div.mw-category div.mw-category-group ul li")
        for film in films:
            title = film.css('a::text').get()
            url = film.css('a::attr(href)').get()
            if url:
                url = response.urljoin(url)
                yield scrapy.Request(url, callback=self.parse_film, meta={'title': title})

    async def parse_film(self, response):
        title = response.meta['title']
        year_selectors = [
            'table.infobox th:contains("Release date") + td::text',
            'table.infobox th:contains("Released") + td::text',
            'table.infobox th:contains("Release") + td::text'
        ]
        year = None
        for selector in year_selectors:
            year = response.css(selector).get()
            if year:
                break
        if year:
            year = ''.join(filter(str.isdigit, year[:4]))
        else:
            year = 'Unknown'
        
        if year.isdigit() and 1940 <= int(year) <= 1949:
            yield {
                'title': title,
                'year': year
            }


# run spider
async def crawl():
    process = CrawlerProcess(get_project_settings())
    process.crawl(FilmNoirSpider)
    await process.start()

async def schedule_crawl():
    while True:
        await crawl()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(schedule_crawl())