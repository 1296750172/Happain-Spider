# -!- coding: utf-8 -!-
import re
import scrapy
from scrapy.http import Response,Request

class I7SpiderSpider(scrapy.Spider):
    name = 'i7_spider'
    # start_urls = {'网页特效':'https://www.17sucai.com/category/4?p=119',
    #               'flash':'https://www.17sucai.com/category/5',
    #               'html5_css':'https://www.17sucai.com/category/31',
    #               '网页模板':'https://www.17sucai.com/category/47',
    #               '网页素材':'https://www.17sucai.com/category/48',
    #               '整站代码':'https://www.17sucai.com/category/88'}
    start_urls = {'网页特效': 'https://www.17sucai.com/category/4?p=119'}

    def start_requests(self):
        for i in self.start_urls.items():
            yield Request(url=i[1],meta={'title':i[0]})

    # 解析列表页
    def parse(self,response):
        meta = response.request.meta
        li_list = response.xpath("//div[@class='pins-list waterfall']/ul/li")
        for i in li_list:
            # 图片链接
            img = i.xpath("./div[@class='pic ']/a/img/@data-src").get()
            # 链接
            href = i.xpath("./p[@class='title']/a/@href").get()
            # 名称
            title = i.xpath("./p[@class='title']/a/text()").get()

            print(img)
            print(title)
            print(href)
            meta['name'] = title
            meta['img'] = img
            yield Request(url=href,callback=self.parse_detail,meta=meta)
            break

    # 下载封面图片
    def parse_detail(self,response):
        meta = response.request.meta
        # try:
        yanshi = response.xpath("//a[@class='view button']/@href").get('')
        tag_list = response.xpath("//div[@class='tag-list clear']/a/text()").extract()
        # except Exception as e:
        #     print(e)
        #     print(response.url)
        #     print("parse_detail")
        #     return
        meta['tag_list'] = tag_list
        yield Request(url=yanshi,callback=self.parse_yanshi,meta=meta)


    # 解析演示界面
    def parse_yanshi(self,response):
        meta = response.request.meta
        # try:
        real_src = response.xpath("//iframe[@id='iframe']/@src").get()
        print(real_src)
        # except Exception as e:
        #     print(e)
        #     print(response.url)
        #     print("parse_yanshi")
        #     return
        yield Request(url=real_src,callback=self.download_core,meta=meta)

    # 完美拷贝页面
    def download_core(self,response):
        meta = response.request.meta
        print(meta)
        re.compile('src="static/picture/2.jpg"')
        pass




