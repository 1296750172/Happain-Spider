import scrapy
from scrapy.http import FormRequest

class TestSpiderSpider(scrapy.Spider):
    name = 'post_spider'
    start_urls = ['https://www.baidu.com']
    def start_requests(self):
        return [FormRequest(url="http://www.lookdiv.com/index/index/indexcode.html",
                                   formdata={'key':'213'},
                                   callback=self.parse)]

    # 解析列表页
    def parse(self, response):
        print(response.text)