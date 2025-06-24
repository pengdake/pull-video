import scrapy
import aiohttp
import playwright
from videospider.items import VideoItem


class IkanBotsSpider(scrapy.Spider):
    name = 'ikanbots'

    def __init__(self, keyword=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not keyword:
            raise ValueError("Missing keyword parameter, run with -a keyword=your_keyword")
        self.keyword = keyword
        self.start_url = "https://v.ikanbot.com/"

    async def check_url_validity(self, url):
        """
        检查视频链接的有效性。
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return True
                    else:
                        return False
        except Exception as e:
            self.logger.error(f"Error checking URL {url}: {e}")
            return False
    
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
            },
            callback=self.parse
        )

    
    async def parse(self, response):
        video_list = []
        page = response.meta["playwright_page"]
        await page.get_by_role("textbox", name="请输入影片、短剧、演职人员").click()
        await page.get_by_role("textbox", name="请输入影片、短剧、演职人员").fill(self.keyword)
        await page.get_by_role("button", name="搜索").click()
        await page.get_by_role("link", name=self.keyword).first.click()
        await page.wait_for_selector("div[name='lineData']")
        # 获取不同线路下的视频链接
        items = await page.locator("div[name='lineData']").all()
        self.logger.info(f"Found {len(items)} video links for keyword '{self.keyword}'")
        # 如果链接包含粤的文字话，则跳过，选择下一个链接
        video_flag = None
        for item in items:
            line_name = await item.inner_text()
            if "粤" in line_name:
                self.logger.info(f"Skipping line with name '{line_name}' as it contains '粤'")
                continue
            video_name = "-".join([self.keyword, line_name])
            video_url = await item.get_attribute("udata")
            if video_url:
                if video_flag:
                    video_id = await item.get_attribute("id")
                    if video_id and video_id.startswith(video_flag):
                        self.logger.info(f"Add video with ID '{video_id}' as it matches the previous video flag '{video_flag}'")
                        video_list.append({
                            "video_url": video_url,
                            "video_name": video_name,
                        })
                        self.logger.info(f"Found video URL: {video_url}")
                        if await self.check_url_validity(video_url):
                            self.logger.info(f"Video URL is valid: {video_url}")    
                else:
                    # 这里可以处理视频链接，比如下载或存储
                    self.logger.info(f"Found video URL: {video_url}")
                    if await self.check_url_validity(video_url):
                        self.logger.info(f"Video URL is valid: {video_url}")
                        video_list.append({
                            "video_url": video_url,
                            "video_name": video_name,
                        })
                        video_id = await item.get_attribute("id")
                        video_flag = video_id.rsplit("-", maxsplit=1)[0]
                    else:
                        self.logger.warning(f"Video URL is invalid: {video_url}")
        yield VideoItem(video_list=video_list, keyword=self.keyword, use_proxy=False)
