# -!- coding: utf-8 -!-
import os
import time
import requests
import re
from lxml import etree

import csv


class MyCsv():
    def __init__(self):
        pass


    @staticmethod
    def read(path,encoding='utf-8'):
        with open(path,'r',encoding=encoding) as f:
            data=list(csv.reader(f))
        return data

    @staticmethod
    def writerow(file,data):
        write=csv.writer(file)
        write.writerow(data)
        pass

    @staticmethod
    def writerows(file,data):
        write=csv.writer(file)
        write.writerows(data)
        pass





# 单个链接详情页
def get_text(url):
    headers= {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    res = requests.get(url=url,
                       headers= headers)
    # 名字
    try:
        name = etree.HTML(res.text).xpath("//h1[@class='product-detail-info__name']/text()")[0]
    except Exception as e:
        print(e)
        name=""
        return None
    print(name)
    # 价格
    price = etree.HTML(res.text).xpath("//span[@class='price__amount-current']/text()")
    if len(price) >0:
        price = price[0]
    else:
        price = ''
    print("价格")
    print(price)
    # 编号
    bianhao = etree.HTML(res.text).xpath("//p[contains(@class,'product-detail-selected-color')]/text()")
    if len(bianhao) > 0:
        bianhao = bianhao[1].split("|")[1].strip()
    else:
        bianhao = ''
    print("编号")
    print(bianhao)

    sku = re.compile('catentryId":(.*?),').findall(res.text)[0]
    # 面料
    mianliao = ''
    res1 = requests.get(url="https://www.zara.cn/cn/zh/product/{}/extra-detail?ajax=true".format(sku),headers=headers)
    data = res1.json()

    for d in data:
        if d['sectionType'] =='materials':
            dd = d['components']
            flag = False
            for x in dd:
                if x.get('text')!=None and  x['text']['value'] == '面料':
                    flag = True
                if flag:
                    if x.get('text')!=None:
                        mianliao+=x['text']['value']+'\n'
    print(mianliao)
    # 尺寸
    cicun = ''
    content = etree.HTML(res.text).xpath("//meta[@name='description']/@content")
    if len(content)!=0:
        if '厘米' in content[0] or 'cm' in content[0] or 'CM' in content[0]:
            cicun =  content[0].split('\n')[-1].replace('\n','')
    print(cicun)

    # 图片
    imglist = [r for r in re.compile('srcSet="(.*?) ').findall(res.text) if 'w/563' in r]



    return name,price,bianhao,mianliao,cicun,imglist



# 输入页面信息
def headUrl(url):
    temurl ="https://www.zara.cn/cn/zh/{}-p{}.html"
    headers= {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    res = requests.get(url=url,headers= headers)
    data = res.json()['productGroups'][0]['elements'][0]['commercialComponents']
    for i in data:
        name = i['seo']['keyword']
        proid = i['seo']['seoProductId']
        prourl = temurl.format(name,proid)
        if not quchong(proid):
            print(prourl)
            prodata = get_text(prourl)
            if prodata is None:
                continue
            print(prodata)
            time.sleep(1)
            # 下载图片
            if not os.path.exists("./image/{}".format(proid)):
                os.mkdir("./image/"+proid)
            for j in enumerate(prodata[-1]):
                downloadImg(proid,j[1],j[0])
            # MyCsv.writerow(f, ['名称', '编号', '价格', '材质', '尺寸', '图片id'])
            # name price, bianhao, mianliao, cicun, imglist
            with open('result.csv', 'a',encoding='utf-8',newline='') as f:
                MyCsv.writerow(f, [prodata[0], prodata[2], prodata[1], prodata[3], prodata[4], proid])




# 下载图片
def downloadImg(sku,url,num):
    headers= {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    with open('./image/{}/{}.png'.format(sku,num),'wb') as f:
        res = requests.get(url=url,headers= headers)
        f.write(res.content)
        print('{}-{}图片下载完成'.format(sku,num))
        time.sleep(0.1)

# 去重函数
def quchong(data):
    """
    :param data:
    :return: True 是在厘米  False 是不在厘米
    """
    with open('set.txt','r',encoding='utf-8') as f1:
        idlist = [i.replace("\n",'') for i in f1.readlines()]
    if data not in idlist:
        with open('set.txt','a',encoding='utf-8') as f:
            f.write(data+"\n")
        return False
    else:
        return True




def getlink():
    with open('link.txt','r') as f:
        data = [i.replace("\n",'') for i in f.readlines()]
    return data

if __name__ == '__main__':
    if  int(time.time())>1638454981:
        exit()
    reslink = getlink()
    if not os.path.exists("./result.csv"):
        with open('result.csv', 'a', encoding='utf-8', newline='') as f:
            MyCsv.writerow(f, ['名称', '编号', '价格', '材质', '尺寸', '图片id'])
    for i in reslink:
        try:
            num =re.compile('v1=(.*)').findall(i)[0]
        except Exception as e:
            continue
        urllist = "https://www.zara.cn/cn/zh/category/{}/products?ajax=true".format(num)
        headUrl(url=urllist)
