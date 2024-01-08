import scrapy

class wikiSpider(scrapy.Spider):
    name = 'wikiSpider'
    start_urls = ['https://en.wikipedia.org/wiki/List_of_film_noir_titles']

    custom_settings = {'USER AGENT': 'Mozilla/5.0 (Windows NT 10.0;Win64) \
        AppleWebkit/537.36 (KHTML, like Gecko) \
        Chrome/89.0.4389.82 Safari/537.36',
        'DOWNLOAD_DELAY' : 1,
        'CONCURRENT_REQUESTS' : 1,
        'RETRY_TIMES' : 3,
        'RETRY_HTTP_CODES' : [500, 503, 504, 400, 403, 404, 408],
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'filmNoir_1940.csv',
        'DOWNLOADER_MIDDLEWARES' : {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        }    
    }

    def parse(self, response):
        # the last thing in response is the one you want to iterate over, in this case it is li not ul
        # xpath to choose something relative 
        for movie in response.xpath('//style[@data-mw-deduplicate="TemplateStyles:r1184024115"]/following-sibling::div[1]//ul/li'):
            yield {
                'title': movie.css('i a::text').get()
            }
