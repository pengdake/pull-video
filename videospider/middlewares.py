class ProxyMiddleware:
    def process_request(self, request, spider):
        proxy = spider.settings.get("PROXY")
        if proxy:
            request.meta["proxy"] = proxy
