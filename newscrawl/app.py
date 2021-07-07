from flask import Flask,request,render_template
from twisted.internet import reactor, defer
from newscrawl.spiders.naver import NaverSpider
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from mongo_ctl import get_mongo_data

app = Flask(__name__)

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
            yield runner.crawl(NaverSpider)
            reactor.stop()
        crawl()
        reactor.run() 
    crawler_func()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl')
def crawl():
    if request.method == 'GET':
        start_spider()
        return 'True',200
    return 'False', 400

@app.route('/view')
def view():
    if request.method == 'GET' :
        return get_mongo_data(),200
    return 'False',400
    
if __name__=='__main__' :
    app.run(host='0.0.0.0',port=8888,debug=True)