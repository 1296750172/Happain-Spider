-   创建项目
    -   scrapy startproject ""
    -   创建爬虫
        -   cd 项目目录
        -   scrapy genspider example example.com
    
-   导出文件
    scrapy crawl 爬虫名 -O xxx.json

-   爬虫中间件与下载中间件
    -   爬虫中间件
        -   在发送给管道之前执行  处理异常之类
    -   下载中间件
        -   在请求之前执行  设置代理