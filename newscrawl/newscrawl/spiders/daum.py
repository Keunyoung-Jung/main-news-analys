import scrapy
from konlpy.tag import Okt
from newscrawl.items import NewscrawlItem
from datetime import datetime


class DaumSpider(scrapy.Spider):
    name = 'daum'
    main_url = 'https://news.daum.net/'
    okt = Okt()
    tagset = ['Noun','Alpha','Foreign']
    quotes_special = ['“','”','‘','’','/']
    section_map = {
        '정치' : 'politics',
        '경제' : 'economy',
        '사회' : 'society',
        '문화' : 'life',
        '국제' : 'world',
        'IT' : 'it'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.main_url, callback=self.parse)
        
    def parse(self, response):
        with_image_headline_url = response.css('#cSub > div > ul > li > div.item_issue > div > strong > a::attr(href)').getall()
        for url in with_image_headline_url : 
            yield scrapy.Request(url=url, callback=self.parse_article_info)
        #연관 기사로 나오는 하위 항목 제외
        box_headline_url = response.css('#mArticle > div.box_headline > ul > li > strong > a::attr(href)').getall()
        for url in box_headline_url : 
            yield scrapy.Request(url=url, callback=self.parse_article_info)
        box_with_image_headline_url = response.css('#mArticle > div.box_headline > ul > li.item_main > a::attr(href)').getall()
        for url in box_with_image_headline_url : 
            yield scrapy.Request(url=url, callback=self.parse_article_info)
        
        most_view_url = response.css('#mArticle > div.box_peruse > div > ol > li > a::attr(href)').getall()
        for url in most_view_url : 
            yield scrapy.Request(url=url, callback=self.parse_article_info)
        most_comment_url = response.css('#mArticle > div.box_g.box_popnews > div.pop_news.pop_cmt > ol > li > a::attr(href)').getall()
        for url in most_comment_url : 
            yield scrapy.Request(url=url, callback=self.parse_article_info)
        
        age_pop_url = response.css('#mArticle > div.box_g.box_popnews > div.pop_news.pop_age > div > ul > li > a::attr(href)').getall()
        for url in age_pop_url : 
            yield scrapy.Request(url=url, callback=self.parse_article_info)
        
    def parse_article_info(self, response) :
        doc = NewscrawlItem()
        press = response.css('#cSub > div > em > a > img::attr(alt)').get()
        title = response.css('#cSub > div > h3::text').get()
        # write_time = response.css('#cSub > div > span > span:nth-child(2) > span::text').get()
        section = response.css('#kakaoBody::text').get()
        
        pos = self.okt.pos(title)
        keywords = [word[0] for word in pos if word[1] in self.tagset and word[0] not in self.quotes_special]
        
        doc['press'] = press
        doc['title'] = title
        # doc['write_time'] = datetime.strptime(write_time,'%Y. %m. %d. %H:%M')
        doc['section'] = self.section_map[section]
        doc['keywords'] = keywords
        doc['crawl_time'] = datetime.now()
        
        yield doc