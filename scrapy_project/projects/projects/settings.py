# Scrapy settings for projects project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'projects'

SPIDER_MODULES = ['projects.spiders']
NEWSPIDER_MODULE = 'projects.spiders'
LOG_LEVEL = "DEBUG"
LOG_ENCODING= "utf-8"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'



# 并发量
CONCURRENT_REQUESTS = 64

REACTOR_THREADPOOL_MAXSIZE = 64
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 32
CONCURRENT_REQUESTS_PER_IP = 16

# 这个相当于 requests.seesion
COOKIES_ENABLED = False
# 下载超时 180秒
DOWNLOAD_TIMEOUT=15
# 禁止重试
RETRY_ENABLED = False
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}


# 爬虫中间件
# SPIDER_MIDDLEWARES = {
#    'projects.middlewares.MovieSpiderMiddleware': 543,
# }


# 下载中间件
DOWNLOADER_MIDDLEWARES = {
   'projects.middlewares.ProjectsDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


# 设置管道文件
ITEM_PIPELINES = {
   'projects.pipelines.ProjectsPipeline': 100,
   'projects.pipelines.FilePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# 初始下载延迟
AUTOTHROTTLE_START_DELAY = 5
# 在高延迟情况下设置的最大下载延迟
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 文件目录
FILES_STORE = 'D:/projects'
FILES_URLS_FIELD = 'file_url'
FILES_RESULT_FIELD = 'files'

# 文件重复下载持久天数
FILES_EXPIRES = 0



# scrapy-redis配置
# REDIS_HOST="127.0.0.1"
# REDIS_PORT=6379
#
# REDIS_URL = 'redis://@127.0.0.1:6379/1'
#
# # 调度器启用Redis存储Requests队列
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#
# # 确保所有的爬虫实例使用Redis进行重复过滤
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#
# # 将Requests队列持久化到Redis，可支持暂停或重启爬虫
# SCHEDULER_PERSIST = True
#
# # Requests的调度策略，默认优先级队列
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
#
# # item 到 redis中的键
# REDIS_ITEMS_KEY = '%(spider)s:items'
#
# REDIS_ENCODING = 'utf-8'
