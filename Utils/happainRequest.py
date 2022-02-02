# -!- coding: utf-8 -!-

import requests
import traceback
import chardet
from requests_toolbelt.multipart.encoder import MultipartEncoder


class happainRequests():
    def __init__(self):

        pass

    @staticmethod
    def get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 '
                                           'Safari/537.36'},
            ssl=True, timeout=3000, retry=3):
        num = 1
        while True:
            try:
                res = requests.get(url=url, headers=headers, timeout=timeout, verify=ssl)
                encode_type = chardet.detect(res.content)['encoding']
                if encode_type is None:
                    res.encoding = 'utf-8'
                else:
                    res.encoding = encode_type
                return res
            except Exception as e:
                print(e)
                # 定位异常在哪一行
                print(traceback.print_exc())
                num += 1
                if num > retry:
                    print("重试失败")
                    break
        return None


    """
       post请求有分 在请求头中 Content-type的类型区别对待

       1. multipart/form-data
           表单格式
           ------WebKitFormBoundaryrGKCBY7qhFd3TrwA
           Content-Disposition: form-data; name="text"
           title
       2. application/x-www-form-urlencoded
           html原生表单的提交方式
           直接用dict字典的方式传递即可
       3. application/json
           传递 data = json.dumps()
       4.
    """
    @staticmethod
    def post(url, data, type=0, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                                          'like Gecko) Chrome/97.0.4692.71 '
                                         'Safari/537.36'},ssl=True, timeout=3000, retry=3):

        # 0 普通表单 1是json格式 2是mutilate form
        post_type = ['application/x-www-form-urlencoded', 'application/json;charset=UTF-8',]

        if type == 0:
            headers['Content-Type'] = post_type[type]
        if type == 1:
            headers['Content-Type'] = post_type[type]
        if type == 2:
            """
            例子
            {
                  # 普通字符类型
                "act": 'dopost',
                # 数组类型
                'extra[job]': '1,7,9,20',
                # 文件类型
                'mymps_img_0': (
                    ('1.jpg', open(imagepath, 'rb'), 'image/jpg')
                )
            }
            """
            m = MultipartEncoder(
                fields=data
            )
            headers['Content-Type'] = m.content_type
        num = 1
        while True:
            try:
                res = requests.post(url=url, data=data, headers=headers, timeout=timeout, verify=ssl)
                encode_type = chardet.detect(res.content)['encoding']
                if encode_type is None:
                    res.encoding = 'utf-8'
                else:
                    res.encoding = encode_type
                return res
            except Exception as e:
                print(e)
                # 定位异常在哪一行
                print(traceback.print_exc())
                num += 1
                if num > retry:
                    print("重试失败")
                    break
        return None

if __name__ == '__main__':
    pass