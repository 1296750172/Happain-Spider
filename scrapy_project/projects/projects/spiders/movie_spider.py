import re
import m3u8
import scrapy
from scrapy.http import Response,Request
from urllib.parse import urljoin
from projects.items import MovieItem
from projects.happainMysql import mySqlUtil
import time
from projects.pipelines import  MoviePipeline

class MovieSpiderSpider(scrapy.Spider):
    name = 'movie_spider'
    start_urls = ['https://app.kpdapp.la/dongman/youma/']
    type_url = "https://app.kpdapp.la/dongman/youma/"
    base_url = 'https://app.kpdapp.la'
    m3u8_url = 'https://play.bo7758991.com'
    num = 2
    flag = True
    def start_requests(self):
        for i in self.start_urls:
            yield Request(url=i)

    # 解析列表页
    def parse(self, response):
        title = response.xpath("//title/text()").get("")
        if "404" in title or title == '':
            return
        link_href = [self.base_url + i.extract() for i in response.xpath("//a[@class='mb-wrap']/@href")]
        for i in link_href:
            if not mySqlUtil.movie_check(i):
                print(i)
                while self.flag:
                    print("目前{}个项目在运行".format(len(MoviePipeline.max_pool)))
                    print(MoviePipeline.max_pool)
                    if len(MoviePipeline.max_pool) <=1:
                        break
                    time.sleep(3)
                yield Request(url=i,callback=self.desc_parse)
                time.sleep(60)

        yield Request(url=self.type_url+"index_{}.html".format(self.num),callback=self.parse)
        self.num+=1
        print("当前页数-",self.num)
    # 解析详情页 播放界面
    def desc_parse(self,response):
        meta = {}
        title = response.xpath("//title/text()").get("")
        if title == "kpd_K频道":
            return
        meta['title'] = title
        meta['url'] = response.url
        print("准备解析{}".format(title))
        movie_url = self.base_url+response.xpath('//iframe[@name="iFrame1"]/@src')[0].extract()
        print(movie_url)
        yield Request(url=movie_url,callback=self.m3u8_parse,meta=meta)

    # 解析m3u8下载地址
    def m3u8_parse(self,response):
        item = MovieItem()
        item['title'] = response.request.meta['title']
        item['url'] = response.request.meta['url']
        try:
            m3u8_url = re.compile("var video=\['(.*?)'\];").findall(response.text)[0]
        except Exception as e:
            print(e)
            return
        res = m3u8.load(m3u8_url)
        try:
            url = res.data['playlists'][0]['uri']
            item['file_urls'] =[urljoin(self.m3u8_url,i.uri) for i in m3u8.load(self.m3u8_url+url).segments]
            print("一共有{}个ts文件准备下载.........".format(len(item['file_urls'])))
            MoviePipeline.max_pool.append(item['url'])
            yield item
        except Exception as e:
            print(e)
            print("没有找到地址")
        pass

