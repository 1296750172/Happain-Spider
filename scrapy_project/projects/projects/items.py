import scrapy
from  scrapy import Field

# 电影爬虫
class MovieItem(scrapy.Item):
    # 标题
    title = Field()
    # url
    url = Field()
    # flag 是否合成为视频
    flag = Field()
    # url 字段
    file_urls = Field()
    # 文件信息的对象
    files = Field()
    # 文件目录
    filename = Field()


class ZmeroItem(scrapy.Item):
    # 视频名字
    name = Field()
    # 初始演员名字
    pername = Field()
    # 原始链接
    url = Field()
    # 视频下载地址
    vedioDownUrl = Field()
    # 图片封面下载地址
    imgDownUrl = Field()
    # 图片封面文件名
    imgName = Field()
    # 视频文件名
    vedioName = Field()
    # 视频日期
    vedioDate = Field()
    # 详细图片
    imgUrlList = Field()
    # 类别
    typeList = Field()
    # 演员
    performer = Field()


# 演员类
class ZmeroPerformerItem(scrapy.Item):
    name = Field()
    link = Field()
    headImgUrl = Field()
    vedioNum = Field()

# 类别
class ZmeroTypeItem(scrapy.Item):
    link = Field()
    type = Field()
    typeJp = Field()

