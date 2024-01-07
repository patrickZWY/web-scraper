import scrapy

class BFISpider(scrapy.Spider):
    name = 'movies_1940s'
    start_urls = ['https://www.bfi.org.uk/sight-and-sound/greatest-films-all-time']

    custom_settings = {'USER AGENT': 'Mozilla/5.0 (Windows NT 10.0;Win64) \
        AppleWebkit/537.36 (KHTML, like Gecko) \
        Chrome/89.0.4389.82 Safari/537.36',
        'DOWNLOAD_DELAY' : 1,
        'CONCURRENT_REQUESTS' : 1,
        'RETRY_TIMES' : 3,
        'RETRY_HTTP_CODES' : [500, 503, 504, 400, 403, 404, 408],
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'movies_1940s.csv',
        'DOWNLOADER_MIDDLEWARES' : {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        }    
    }

    def parse(self, response):
        for movie in response.css('body #root div.ResultsPage__PollPage-sc-of10co-18.eYhEFo main.Landmark-sc-1aeknwx-0.ResultsPage__ResultsMain-sc-of10co-4.iyyYYR.byorKl div.ResultsPage__ResultGrid-sc-of10co-0.jwsIcX article'):

            year_line = movie.css('a .ResultsPage__P-sc-of10co-2.cPbLUx::text').get()
            year = int(year_line.split()[0])
            if 1940 <= year <= 1949:
                yield {
                    'title': movie.css('a h1::text').get(),
                    'year': year
                }
