import scrapy


class DaumSpider(scrapy.Spider):
    name = 'daum'
    main_url = 'https://news.daum.net/'

    def start_requests(self):
        return scrapy.Request(url=self.main_url, callback=self.parse)
    def parse(self, response):
        title = response.css('#today_main_news > div.hdline_news > ul > li > div.hdline_article_tit > a::text').getall()
        
        print(title)