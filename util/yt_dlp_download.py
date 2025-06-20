from yt_dlp import YoutubeDL

#PROXY = 'socks5://192.168.31.22:7897'
PROXY = 'socks5://192.168.31.99:7890'

def download_video(url: str, output_path: str, proxy: str = None):
    """
    下载视频到指定路径。

    :param url: 视频的 URL 地址
    :param output_dir: 输出目录
    :param referer: HTTP Referer 头
    """
    ydl_opts = {
        'hls_prefer_native': True,                        # 强制使用 yt-dlp 自带的 HLS 下载器
        'add_header': [                                   # 添加 HTTP 请求头（防止 403）
            #('Referer', referer),
            ('User-Agent', 'Mozilla/5.0'),
        ],
        'hls_prefer_native': True,
        'outtmpl': output_path,                           # 设置输出文件名
        'noplaylist': True,                               # 避免下载整个播放列表（如果是的话）
    }
    if proxy:
        ydl_opts['proxy'] = proxy
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    url = "https://m8t.vboku.com/20190627/XnW4B78V/index.m3u8?sign=ySYYMdvqwVQdu1Ragzjit7aAITePpmy9tZINeaJ2QfU%253D"
    output_path = '/videos/长安的荔枝/长安的荔枝-06'  # 替换为实际的输出目录
    download_video(url, output_path, PROXY)
    print(f'视频已下载到 {output_path}')