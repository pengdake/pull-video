import scrapy

class VideoItem(scrapy.Item):
    video_list = scrapy.Field()
    keyword = scrapy.Field()
    use_proxy = scrapy.Field(default=True)