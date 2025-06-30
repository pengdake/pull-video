import json

def extract_video_requests(logs, keyword):
    """
    从浏览器日志中提取视频请求的URL。

    :param logs: 浏览器性能日志
    :param keyword: 关键词，用于匹配视频请求
    :return: 匹配的视频请求URL列表
    """

    for entry in logs:
        log = json.loads(entry['message'])['message']
        if log['method'] == 'Network.requestWillBeSent':
            request = log['params']['request']
            if 'url' in request and keyword in request['url']:
                return request['url']
    return None
