import functools
import time
from datetime import datetime
import schedule
import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from newscrawl.spiders.daum import DaumSpider
from newscrawl.spiders.naver import NaverSpider

def print_elapsed_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        print(f'LOG: Running job "{func.__name__}" at {datetime.now()}')
        result = func(*args, **kwargs)
        print(f'LOG: Job "{func.__name__}" completed in {time.time() - start_timestamp} seconds')
        print(f'LOG: Finished job "{func.__name__}" at {datetime.now()}')
        return result

    return wrapper

def start_spider():
    custom_settings= {
        'ITEM_PIPELINES' : {
            'newscrawl.pipelines.NewscrawlPipeline': 300
        }
    }
    def crawler_func():
        configure_logging()
        runner = CrawlerRunner(custom_settings)

        @defer.inlineCallbacks
        def crawl() :
            yield runner.crawl(DaumSpider)
            yield runner.crawl(NaverSpider)
            reactor.stop()
        crawl()
        reactor.run() 
    crawler_func()


@print_elapsed_time
def job_every_time_crawl() :
    start_spider()


# schedule.every().day.at("15:02").do(job_every_time_crawl)
job_every_time_crawl()

# while True:
#     schedule.run_pending()
#     time.sleep(1)