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
    #url = "https://s6-e1.sbacii.com/ppot/_definst_/mp4:s15/ivod/lxj-cadlz-09-025F12456.mp4/chunklist.m3u8?vendtime=1750581960&vhash=575vNO6OYO9uoPLZF910kV5Wc5jlgtFjZ4kcjeHZc_c=&vCustomParameter=0_188.253.115.249_HK_1_0&lb=45fdd9fe1c4bc8d1cdd8568eb590b591&us=1&proxy=SpOjPJ4kSs9XOsbfBcDlRNnpDYrbCIvYQNHtONbbONGkOsyslZcR5hAObp4yNHtRsTbRcLoOMmkOsyslZcR5hAObpeqjhAuEJAnihINCRUslZcR5hAObpkmlBetixUtCfSnjxD"
    url = "https://6tm.wdubo.com/20250609/wMCOvkEM/index.m3u8?sign=xjPe2h6mZIoHDt2zcFgObtt5PD3EH3Chaaz9hKI%252BNcM%253D"
    output_path = '/videos/长安的荔枝/长安的荔枝-07'  # 替换为实际的输出目录
    download_video(url, output_path, PROXY)
    print(f'视频已下载到 {output_path}')