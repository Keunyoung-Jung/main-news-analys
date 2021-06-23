import scrapy


class NaverSpider(scrapy.Spider):
    name = 'naver'
    main_url = 'http://https://news.naver.com/'

    def parse(self, response):
        pass
