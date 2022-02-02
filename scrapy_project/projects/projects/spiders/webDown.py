# -!- coding: utf-8 -!-
import os
from urllib.parse import urljoin
import chardet
import requests
import re
from lxml import etree



# css内部下载
def cssindownload(base_url,path):
    with open(path,'r',encoding='utf-8') as f:
        data = f.read()
    url_list = re.compile('url\((.*?)\) ').findall(data)
    print(url_list)

    pass


# css文件下载
def cssdownload(basepath,name,content):
    with open(os.path.join(basepath, "css", name), 'wb') as f:
        f.write(content)
    pass

# js下载
def jsdownload(basepath,name,content):
    with open(os.path.join(basepath, "js", name), 'wb') as f:
        f.write(content)

# 静态文件下载
def filedownload(basepath,name,content):
    with open(os.path.join(basepath, "file", name), 'wb') as f:
        f.write(content)

# 主入口
def download(url,path):
    basepath = "../web/demo/static/"
    # html 的名称
    rootname = url.rsplit("/",1)[1]
    baseurl = url.split("://")[1].rsplit("/")[0]
    print(baseurl)
    root_url = url.rsplit("/",1)[0]+"/"
    print(root_url)

    root_res = requests.get(url)
    root_res.encoding = chardet.detect(root_res.content)['encoding']


    root_res_text = root_res.text
    href_list = re.compile('href="(.*?)"').findall(root_res.text)
    src_list = re.compile('src="(.*?)"').findall(root_res.text)
    print(href_list)
    print(src_list)

    # 下载href
    for i in href_list:
        print(i)
        name = i.rsplit("/",1)[1]
        root_res_text = root_res_text.replace(i,"static/css/"+name)

        res = requests.get(url=urljoin(root_url,i))

        # 下载css
        if i.endswith(".css"):
            cssdownload(basepath,name,res.content)

        if i.endswith(".html"):
            print(i)
            # download()

    # 下载src
    for i in src_list:
        name = i.rsplit("/",1)[1]
        print(name)
        res = requests.get(url=urljoin(root_url, i))
        if i.endswith(".js"):
            root_res_text = root_res_text.replace(i, "static/js/" + name)
            jsdownload(basepath,name,res.content)
        else:
            root_res_text = root_res_text.replace(i, "static/file/" + name)
            filedownload(basepath,name,res.content)



    # 主页内容下载
    with open(os.path.join("../web/demo/",rootname),'w',encoding='utf-8') as f:
        f.write(root_res_text)


if __name__ == '__main__':
    download(url="https://www.17sucai.com/preview/776298/2021-09-23/hyy/index.html",path="../web/demo")
    # cssindownload(base_url="https://www.17sucai.com/preview/776298/2021-09-23/hyy",path='../web/demo/static/css/style.css')
    pass

