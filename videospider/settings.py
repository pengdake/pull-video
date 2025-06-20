BOT_NAME = "videospider"

SPIDER_MODULES = ["videospider.spiders"]
NEWSPIDER_MODULE = "videospider.spiders"

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    "videospider.pipelines.VideoDownloadPipeline": 300,
}

#PROXY = 'socks5://192.168.31.22:7897'
PROXY = 'socks5://192.168.31.99:7890'
VIDEO_DIR = '/videos/'

DOWNLOADER_MIDDLEWARES = {
    "videospider.middlewares.ProxyMiddleware": 100,

}

CHROMEDRIVER_PATH = '/usr/bin/chromedriver'  # 替换为实际的 chromedriver 路径

LOG_ENABLED = True
LOG_FILE = 'scrapy.log'  # 日志输出路径
LOG_LEVEL = 'DEBUG'            # 可选: DEBUG, INFO, WARNING, ERROR, CRITICAL
