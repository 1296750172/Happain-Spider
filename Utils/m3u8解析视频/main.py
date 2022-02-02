# -!- coding: utf-8 -!-
import os

import m3u8
from urllib.parse import urljoin,urlparse
import requests
import asyncio
import aiohttp
from aiohttp import ClientSession
import functools
import shutil

def get_ts_url(url,base_url=None):
    # 不为空
    if base_url is not None:
        res = m3u8.load(uri=urljoin(base_url,url))
        playlist = res.data['playlists']
        if len(playlist) > 0:
            print(playlist)
            return urljoin(base_url, playlist[0]['uri'])
    else:
        res = m3u8.load(uri=url)
        playlist = res.data['playlists']
        if len(playlist) > 0:
            print(playlist)
            base = urlparse(url)
            return urljoin(str(base.scheme)+"://"+str(base.netloc), playlist[0]['uri'])
    return None



# 解析ts列表
def get_ts_list(url,base_url=None):
    ts_list = []
    # 如果基础url不为空
    if base_url is not None:
        m3 = m3u8.load(uri=urljoin(base_url,url))
        for i in m3.segments:
            ts_list.append(urljoin(base_url,i.uri))
        return ts_list
    else:
        m3 = m3u8.load(uri=url)
        base = urlparse(url)
        for i in m3.segments:
            ts_list.append(urljoin(str(base.scheme)+"://"+str(base.netloc), i.uri))
        return ts_list

async def request_get(**kwargs):
    # 限制并发数2
    async with asyncio.Semaphore(1):
        async with ClientSession() as session:
            async with session.get(**kwargs) as response:
                response = await response.content.read()
                return response


# 执行回调方法
def callback_parse(num,task):

    with open('projects/{}_ts.ts'.format(num),'wb') as f:
        f.write(task.result())
        print("写入task_{}成功".format(num))

# 删除目录文件
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

# 下载ts
async  def download(ts_list,num):
    task_list = []

    for i in enumerate(ts_list):
        task = asyncio.ensure_future(request_get(url=i[1],verify_ssl=False,timeout=5))
        task.add_done_callback(functools.partial(callback_parse,i[0]))
        task_list.append(task)
        if i[0]%num == 0 or i[0] == len(ts_list):
            await asyncio.wait(task_list)
            await asyncio.sleep(3)
            task_list = []




# mp4
def to_mp4():
    base = './projects/'
    filelist = os.listdir(base)
    with open('demo1.mp4','wb') as f:
        for i in sorted(filelist,key=lambda x: int(x.split("_")[0])):
            with open(os.path.join(base,i),'rb') as f1:
                print(i)
                f.write(f1.read())




if __name__ == '__main__':
    del_file("movie")
    base_url = 'https://play.bo7758991.com/123123'
    d = get_ts_url(url="/20210912/0OVQXDOn/index.m3u8",base_url=base_url)
    ts_list = get_ts_list(url=d)
    # 开启事件循环
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download(ts_list,8))
    to_mp4()
    del_file("movie")



