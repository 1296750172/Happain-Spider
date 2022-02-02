# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import json
import os
import time
from urllib.parse import urlparse

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import  FilesPipeline
from itemadapter import ItemAdapter
from scrapy import Request
from .settings import FILES_STORE
from projects.happainMysql import mySqlUtil
from projects.happainTranslate.main import translate
from projects.happainMysql.mySql import  mysql
from projects.items import ZmeroPerformerItem,ZmeroItem,ZmeroTypeItem
import datetime
from pymysql import escape_string

md5 = hashlib.md5()
def get_md5(string):
    md5.update(string.encode("utf-8"))
    return md5.hexdigest()


# 文件管道类
class MoviePipeline(FilesPipeline):
    # 运行的最大数量
    max_pool = []

    # 每次下载都会调用一次
    def file_path(self, request, response=None, info=None, *, item=None):
        filename = str(request.meta['num'])+"-"+request.meta['filename']
        return filename

    # 获取下载请求 然后执行file path
    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        filename = get_md5(adapter['title'])
        for file_url in enumerate(adapter['file_urls']):
            yield Request(url=file_url[1],meta={'title':adapter['title'],'num':file_url[0],'filename':filename+".ts"})


    def item_completed(self, results, item, info):
        paths = [x['path'] for ok,x in results if ok]
        if not paths:
            mySqlUtil.movie_insert(title=str(item['title']), url=str(item['url']), flag='2',file_num=0)
            raise DropItem("文件下载异常")
        adapter = ItemAdapter(item)
        adapter['filename'] = paths

        with open(os.path.join(FILES_STORE,item['title']+".mp4"),'wb') as f:
            paths.sort(key=lambda x: int(x.split("-")[0]))
            for i in paths:
                with open(os.path.join(FILES_STORE,i),'rb') as f1:
                    data = f1.read()
                f.write(data)
                print(i,"写入完毕")
                os.remove(os.path.join(FILES_STORE,i))
                print(i,"删除完毕")

        print("{}下载成功,一共{}个ts文件".format(item['title'],len(paths)))
        mySqlUtil.movie_insert(title=str(item['title']),url=str(item['url']),flag='1',file_num=len(paths))
        return item


# 文件下载管道
class FilePipeline(FilesPipeline):

    def item_completed(self, results, item, info):
        return item

    def get_media_requests(self, item, info):
        if info.spider.name == 'zemro_spider':
            pass

    def file_path(self, request, response=None, info=None, *, item=None):
        return ''




# 图片管道
class ImgPipe(ImagesPipeline):

    # 发送下载链接
    def get_media_requests(self, item, info):
        yield Request(item['src'])

    #返回图片的名称
    def file_path(self, request, response=None, info=None, *, item=None):
        print(item)
        return item['name']

    # 返回给下一个管道类
    def item_completed(self, results, item, info):
        return item


# 项目管道
class ProjectsPipeline:
    conn = None
    def process_item(self, item, spider):

        if spider.name == "zmero_spider":
            # 存储演员
            if isinstance(item,ZmeroPerformerItem):

                result = self.conn.execute_res("select id from zmero_performer where link = '{link}'".format(link =item['link']))
                if len(result)==0:
                    print(item)
                    zhname = translate(item['name'],src='jp',tar="zh")
                    print(zhname)
                    sql = "insert into zmero_performer values(default ,'%s','%s','%s','%s',%d,'%s' )"%(
                        escape_string(item['name']),
                        escape_string(zhname),
                        escape_string(item['link']),
                        escape_string(item['headImgUrl']),
                        int(item['vedioNum']),
                        datetime.datetime.now()
                    )
                    try:
                        self.conn.execute(sql)
                    except Exception as e:
                        print(e)
                        print(sql)
                    return item
            # 储存类别
            if isinstance(item,ZmeroTypeItem):
                result = self.conn.execute_res("select id from zmero_type where link = '{}'".format(item['link']))
                if len(result) ==0:
                    item['typeJp'] = translate(item[ 'type'], src="jp",tar="zh")
                    print(item)
                    self.conn.execute(
                        "insert into zmero_type(link,`type`,type_jp) values ('%s','%s','%s')"%(escape_string(item['link']),
                                                                                               item['type'],
                                                                                      item['typeJp']))
                    time.sleep(1)
                    return item
            # 储存视频
            if isinstance(item,ZmeroItem):
                # 翻译
                item['name'] = translate(item['name'],src="jp",tar="zh")
                vedio_res = self.conn.execute_res("select id from zmero_vedio where vedio_down_url = '{}'".format(
                    item['vedioDownUrl']))
                if len(vedio_res) ==0:
                    # 添加视频表
                    vedio_id = self.conn.execute("insert into zmero_vedio values (default ,'{name}','{url}',"
                                                "'{vdownurl}',"
                                       "'{vname}',"
                                      "'{vdate}','{imgdownurl}','{imgname}',"
                                      "'{typelist}','{performer}','{imglist}',default)".format(
                        name=item['name'],
                        url=item['url'],
                        vdownurl=item['vedioDownUrl'],
                        vname='',
                        vdate=item['vedioDate'],
                        imgdownurl=item['imgDownUrl'],
                        imgname= '',
                        typelist=json.dumps(item['typeList']),
                        performer=json.dumps(item['performer']),
                        imglist= json.dumps(item['imgUrlList'])
                    ))
                    # 添加详情图片数据
                    for i in item['imgUrlList']:
                        if len(self.conn.execute_res("select id from zmero_img where img_url = '{}'".format(i))) == 0:
                            self.conn.execute("insert into zmero_img values (default ,{},'{}','{}','{}',default )"
                                              .format(vedio_id, item['name'], item['imgDownUrl'], i))
                    # 添加视频类别表
                    for i in item['typeList']:
                        try:
                            (typeid, typejp, link) = self.conn.execute_res("select id,type_jp,link from zmero_type where "
                                                                           "`type`='{}'".format(i))[0]
                        except Exception as e:
                            print(e)
                            print("type_vedio")
                            continue

                        if len(self.conn.execute_res("select id from zmero_type_vedio where type_id={} and vedio_id={}".format(typeid, vedio_id))) == 0:
                            self.conn.execute("insert into zmero_type_vedio values (default ,{},'{}','{}',{},'{}',"
                                              "'{}',default )".format(typeid, typejp, link, vedio_id, item['name'], item['vedioDownUrl']))
                else:
                    vedio_id  = vedio_res[0][0]
                # 添加演员与视频
                (id,name,link,img) = self.conn.execute_res("select id,`name`,link,head_img_url from zmero_performer where name = '{}'"
                                                               .format(item['pername']))[0]
                if len(self.conn.execute_res("select id from zmero_performer_vedio where performer_id={} and vedio_id={}".format(id,vedio_id)))==0:
                    self.conn.execute("insert into zmero_performer_vedio values(default ,{},'{}','{}','{}',{},'{}','{}','{}',default )".format(
                        id,name,link,img,vedio_id,item['name'],item['vedioDownUrl'],item['imgDownUrl']))

                return item

    def open_spider(self,spider):
        self.conn = mysql(localhost='127.0.0.1', username='root', password='123456', mydb='happain-scrapy')
        pass
    def close_spider(self,spider):
        self.conn.close()
        pass







