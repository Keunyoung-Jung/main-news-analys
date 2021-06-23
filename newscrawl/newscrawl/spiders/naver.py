import scrapy
from konlpy.tag import Okt
from newscrawl.items import NewscrawlItem
import time
from datetime import datetime

class NaverSpider(scrapy.Spider):
    name = 'naver'
    main_url = 'https://news.naver.com'
    okt = Okt()
    tagset = ['Noun','Alpha','Foreign']
    quotes_special = ['“','”','‘','’','/']

    def start_requests(self):
        yield scrapy.Request(url=self.main_url, callback=self.parse)
            
    def parse(self, response):
        #헤드라인 뉴스 기사
        headline_article_url = response.css('#today_main_news > div.hdline_news > ul > li > div.hdline_article_tit > a::attr(href)').getall()
        headline_img_article_url = response.css('#today_main_news > div.hdline_news > div > div > a::attr(href)').getall()
        headline_article_url = [self.main_url+url for url in headline_article_url]
        for url in headline_article_url : 
            yield scrapy.Request(url=url, callback=self.parse_article_info, meta={'section' : 'headline'})
        # self.loop_article(headline_article_url, meta_name='headline')
        #섹션별 크롤링 
        for section in ['politics','economy','society','life','world','it'] :
            article_url = response.css(f'#section_{section} > div.com_list > div > ul > li > a::attr(href)').getall()
            for url in article_url : 
                yield scrapy.Request(url=url, callback=self.parse_article_info, meta={'section' : section})
        
    def parse_article_info(self, response) :
        doc = NewscrawlItem()
        press = response.css('#main_content > div.article_header > div.press_logo > a > img::attr(title)').get()
        title = response.css('#articleTitle::text').get()
        write_time = response.css('#main_content > div.article_header > div.article_info > div > span::text').get().replace('오후','PM').replace('오전','AM')
        write_time_dtime = datetime.strptime(write_time,"%Y.%m.%d. %p %I:%M")
        section = response.meta['section']
        
        print('-'*20)
        print(section)
        print(title)
        print(press)
        st = time.time()
        pos = self.okt.pos(title)
        keywords = [word[0] for word in pos if word[1] in self.tagset and word[0] not in self.quotes_special]
        print(keywords)
        print('소요 시간',time.time()-st)
        
        # doc['press'] = press
        # doc['title'] = title