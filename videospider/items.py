import scrapy

class VideoItem(scrapy.Item):
    video_list = scrapy.Field()
    keyword = scrapy.Field()