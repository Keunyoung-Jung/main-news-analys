import scrapy


class DaumSpider(scrapy.Spider):
    name = 'daum'
    main_url = 'http://https://news.daum.net/'

    def parse(self, response):
        pass
