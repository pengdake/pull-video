from util.yt_dlp_download import download_video
import os

class VideoDownloadPipeline:
    def process_item(self, item, spider):
        base_dir = spider.settings.get('VIDEO_DIR')
        if not base_dir:
            spider.logger.error("VIDEO_DIR is not set in settings.")
            return item
        url = item.get('video_url')
        name = item.get('video_name')
        output_dir = os.path.join(base_dir, name)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{name}.%(ext)s")
        if os.path.exists(output_path):
            spider.logger.info(f"Video {name} already exists, skipping download.")
            return item

        spider.logger.info(f"Downloading video {name} from {url} to {output_path}")
        proxy = spider.settings.get('PROXY')
        try:
            download_video(url, output_path, proxy)
        except Exception as e:
            spider.logger.error(f"Failed to download video {name}: {e}")
            return item
        spider.logger.info(f"Video {name} downloaded successfully.")
        return item