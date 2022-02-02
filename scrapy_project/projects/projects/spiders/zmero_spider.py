import re
import m3u8
import scrapy
from scrapy.http import Response,Request
from urllib.parse import urljoin
from projects.items import MovieItem
from projects.happainMysql import mySqlUtil
import time
from projects.pipelines import  MoviePipeline
from urllib.parse import urljoin
from projects.items import ZmeroItem,ZmeroPerformerItem,ZmeroTypeItem
from projects.happainMysql.mySql import mysql
from projects.happainRedis.myRedis import MyRedis

class ZmeroSpider(scrapy.Spider):
    name = 'zmero_spider'
    start_urls = ['https://zmero.com/category/8237/']
    # 每个spider 自己的设置
    custom_settings = {
        'FILES_STORE' : 'D:/projects',
        'FILES_URLS_FIELD' : 'file_url',
        'FILES_RESULT_FIELD' : 'files'
    }
    # 网站跟目录
    base_url="https://zmero.com"
    # 类别目录
    type_url = 'https://zmero.com/genre/'

    start_performerurl = ["https://zmero.com/av/initial/mu/"]

    conn = mysql(localhost='127.0.0.1', username='root', password='123456', mydb='happain-scrapy')

    def start_requests(self):
        data = self.conn.execute_res("select `name`,link from zmero_performer")
        for i in data:
            yield Request(url=i[1],callback=self.parse,meta={'name':i[0]})
        self.conn.close()




    # 爬取类别
    def type_parse(self,response):
        item = ZmeroTypeItem()
        a_link = response.xpath("//a[@class='btn btn-outline-blue px-2 py-1 h-100 d-flex justify-content-center "
                       "align-items-center']")
        for i in a_link:
            # 链接
            link = urljoin(self.base_url,i.xpath("./@href").get(""))
            type = i.xpath("./text()").get("")
            item['link'] = link
            item['type'] = type
            yield item
    # 爬取演员的五十音图
    def performer_parse(self,response):
        a_link = response.xpath("//a[contains(@class,'btn btn-outline-secondary flex-grow-1 p-1')]/@href").extract()
        for i in a_link:
            print(i)
            yield Request(url=urljoin(self.base_url,i),callback=self.performer_list_parse)
    # 爬取演员的itemlist
    def performer_list_parse(self,response):
        item =ZmeroPerformerItem()
        div_list = response.xpath("//div[@class='col-4 col-sm-3 col-md-2 col-lg-2 col-xl-1 col-xxl-1']")
        for i in div_list:
            # 名字
            name = i.xpath("./a/div[@class='card-body link-dark p-0 mt-1 text-center']/p[@class='card-text "
                           "text-primary mb-0']/text()").get("")
            # 链接
            link = urljoin(self.base_url,i.xpath("./a/@href").get(""))
            # 头像链接
            img_head_url = "https:"+i.xpath("./a/div[@class='object-fit-container-actor']/img/@src").get("")
            # 视频数量
            vedio_num = i.xpath("./a/div[@class='card-body link-dark p-0 mt-1 text-center']/p[@class='card-text "
                                "text-muted']/text()").get("").replace("件","")
            item['name'] = name
            item['link'] = link
            item['headImgUrl'] = img_head_url
            item['vedioNum'] = vedio_num
            yield item
        nexta = response.xpath("//a[@rel='next']/@href").get("")
        if nexta!='':
            url = urljoin(self.base_url,nexta)
            print(url)
            yield Request(url=url,callback=self.performer_list_parse)
    # 解析列表页
    def parse(self, response):
        per_name = response.request.meta['name']
        print(per_name)

        a_list = response.xpath("//a[@class='card border-0']")
        for i in a_list:
            meta_data = {}
            # 图片链接
            img_url = i.xpath("./div[@class='object-fit-container']/img/@src").get("")
            # 链接
            a_link = urljoin(response.url,i.xpath("./@href").get(""))
            # 名字
            name = i.xpath("./div[@class='card-body link-dark pt-1 px-1 pb-0']/p/text()").get("")
            # 时间
            vedio_date = i.xpath("./div[@class='card-text text-muted px-1 pb-0 mt-1 text-left']/span/text()").get("")
            meta_data['img_url'] = img_url
            meta_data['name'] = name
            meta_data['vedio_date'] = vedio_date
            meta_data['performer_name'] = per_name
            if not MyRedis.check_data("zmero_spider",a_link):
                yield Request(url=a_link,callback=self.vedio_parse,meta=meta_data)
        nexta = response.xpath("//a[@rel='next']/@href").get("")
        if nexta != '':
            url = urljoin(self.base_url, nexta)
            print(url)
            yield Request(url=url, callback=self.parse,meta={'name':per_name})
    #  获取二级详情页
    def vedio_parse(self,response):

        item = ZmeroItem()
        meta_data = response.request.meta
        # 视频地址
        vedio_url = 'https:'+response.xpath("//source/@src").get("")
        # 出演者
        performer = response.xpath("//div[@class='d-flex mt-3 align-items-center'][3]/div[@class='flex-grow-1 "
                                   "ps-2']/a/text()").extract()

        if len(performer) == 0:
            performer = ""
        # 图片列表
        img_url_list = response.xpath("//div[@class='object-fit-container-entry']/a/@href").extract()

        # 类别
        tem  = response.xpath("//div[@class='d-flex mt-3 align-items-center']")
        type_name = tem[-1].xpath("./div[@class='flex-grow-1 ps-2']/a/text()").extract()
        # 类别链接
        type_link = [urljoin(self.base_url,i) for i in tem[-1].xpath("./div[@class='flex-grow-1 "
                                                                    "ps-2']/a/@href").extract()]
        type_list= {}
        for i in zip(type_name,type_link):
            type_list[i[0]]=i[1]


        item['name'] = meta_data['name']
        item['imgDownUrl'] = meta_data['img_url']
        item['vedioDate'] = meta_data['vedio_date']
        item['vedioDownUrl'] = vedio_url
        item['performer'] = performer
        item['pername'] = meta_data['performer_name']
        item['imgUrlList'] = img_url_list
        item['typeList'] = type_list
        item['url'] = response.url

        yield item



