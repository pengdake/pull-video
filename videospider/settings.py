import os

BOT_NAME = "videospider"

SPIDER_MODULES = ["videospider.spiders"]
NEWSPIDER_MODULE = "videospider.spiders"

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    "videospider.pipelines.VideoDownloadPipeline": 300,
}

# 设置代理
PROXY = os.getenv('PROXY', 'socks5://192.168.31.99:7890')

# 视频下载目录
VIDEO_DIR = '/videos/'

DOWNLOADER_MIDDLEWARES = {
    "videospider.middlewares.ProxyMiddleware": 100,

}

CHROMEDRIVER_PATH = '/usr/bin/chromedriver'  # 替换为实际的 chromedriver 路径

LOG_ENABLED = True
#LOG_FILE = 'scrapy.log'  # 日志输出路径
#LOG_LEVEL = 'DEBUG'            # 可选: DEBUG, INFO, WARNING, ERROR, CRITICAL

# settings.py
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Playwright 浏览器设置
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "args": [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
    ]
}


