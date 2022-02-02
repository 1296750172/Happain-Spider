import mitmproxy.http

from mitmproxy import ctx, http,tcp

class Joker:
    def request(self, flow: mitmproxy.http.HTTPFlow):
        print("请求是")
        print(flow.request.url)


    def response(self, flow: mitmproxy.http.HTTPFlow):
        print("响应是")
        print(flow.request.text)

