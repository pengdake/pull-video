import os
import time
import scrapy
from videospider.items import VideoItem
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import undetected_chromedriver as uc
import cloudscraper


class VideoSpider(scrapy.Spider):
    name = "videospider"

    def __init__(self, keyword=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #if not keyword:
        #    raise ValueError("Missing keyword parameter, run with -a keyword=your_keyword")
        keyword = "周处除三害"
        self.keyword = keyword

        proxy_url = self.settings.get("PROXY")

        # selenium-wire 的代理配置
        #wire_options = {
        #    'proxy': {
        #        'http': proxy_url,
        #        'https': proxy_url,
        #        'no_proxy': 'localhost,127.0.0.1'
        #    }
        #}

        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument(f"--proxy-server={proxy_url}")
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--window-size=1280,720")

        #chrome_options.add_argument("--ignore-certificate-errors")

        #service = Service(executable_path=self.settings.get("CHROMEDRIVER_PATH"))

        # 使用 seleniumwire 的 webdriver 并传入代理配置
        #self.driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=wire_options, service=service)
        self.driver = uc.Chrome(options=chrome_options, driver_executable_path=self.settings.get("CHROMEDRIVER_PATH"))
        self.index_url = "https://www.duboku.tv/"

        self.wait = WebDriverWait(self.driver, 300)

        self.debug_dir = "debug_screens"
        os.makedirs(self.debug_dir, exist_ok=True)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(
            *args,
            settings=crawler.settings,  # ✅ 显式注入
            **kwargs
        )


    def start_requests(self):
        try:
            self.logger.info(f"Starting video search for keyword: {self.keyword}")
            self.driver.get(self.index_url)

            self.driver.save_screenshot(f"{self.debug_dir}/index.png")
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "wd")))
            search_box.clear()
            search_box.send_keys(self.keyword)
            search_button = self.wait.until(EC.element_to_be_clickable((By.ID, "searchbutton")))
            search_button.click()

            # 找到唯一“查看详情”并点击
            self.logger.info("Waiting for search results to load...")
            self.driver.save_screenshot(f"{self.debug_dir}/search_results.png")
            detail_link = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), '查看详情')]")
            ))
            detail_link.click()

            # 等待列表页加载，获取所有视频播放链接
            self.logger.info("Waiting for video list to load...")
            video_links = self.wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "ul > li > a[href^='/vodplay']")
            ))

            self.driver.save_screenshot(f"{self.debug_dir}/video_list.png")
            for i in range(len(video_links)):
                #self.driver.requests.clear()  # 清除之前的请求记录

                self.logger.info(f"Processing video {i + 1}/{len(video_links)}: {video_links[i].text.strip() or f'Video {i + 1}'}")
                video_link = video_links[i]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", video_link)
                link_name = video_link.text.strip() or f"{i + 1}"
                video_name = "-".join([self.keyword, link_name])
                video_link.click()

                time.sleep(10)  # 等待页面加载
                
                ad_iframe = self.driver.find_element(By.CSS_SELECTOR, 'iframe[id*="aswift"]')
                if ad_iframe:
                    self.logger.info("Ad iframe found, switching to it...")
                    self.wait.until(
                        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id*='aswift']"))
                    )
                    in_iframe = self.driver.execute_script("return window.self !== window.top")
                    self.logger.info(f"当前是否在 iframe 中：{in_iframe}")

                    time.sleep(5)  # 等待广告加载
                    close_btn = self.wait.until(
                        EC.element_to_be_clickable((By.ID, "dismiss-button"))
                    )
                    close_btn.click()
                    self.logger.info("Ad dismissed, switching back to default content...")
                    self.driver.switch_to.default_content()
                    time.sleep(5)  # 等待广告关闭
                    video_link.click()  # 再次点击视频链接以确保加载正确


                # 切换iframe到视频播放页面
                self.logger.info("Switching to video iframe...")
                self.wait.until(EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "#playleft > iframe")  # 假设视频播放页面的iframe以/play开头
                ))
                iframe = self.driver.find_element(By.CSS_SELECTOR, "#playleft > iframe")
                self.driver.switch_to.frame(iframe)

                


                # 等待播放按钮出现并点击
                self.logger.info("Waiting for play button to become clickable...")
                play_button = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[title='Play Video']")
                ))
                self.driver.save_screenshot(f"{self.debug_dir}/video_{i + 1}_play_button.png")
                play_button.click()

                # 提取视频url
                video_src = None
                for request in self.driver.requests:
                    if request.response and "m3u8" in request.url:
                        video_src = request.url
                        self.logger.info(f"Found video URL: {video_src}")
                        break

                if video_src:
                    self.driver.requests.clear()
                    yield VideoItem(video_url=video_src, video_name=video_name)

                self.logger.info(f"Video {i + 1} processed, returning to video list page.")
                self.driver.back()  # 返回视频列表页
                self.wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "ul > li > a[href^='/vodplay']")
                ))

            self.driver.quit()
        except Exception as e:
            self.driver.quit()
