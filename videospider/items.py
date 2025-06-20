import scrapy

class VideoItem(scrapy.Item):
    video_url = scrapy.Field()
    video_name = scrapy.Field()