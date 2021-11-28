# -!- coding: utf-8 -!-
import time

import requests
import re
from lxml import etree


# 单个链接详情页
def get_text(url):
    headers= {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    res = requests.get(url=url,
                       headers= headers)
    res.encoding='utf-8'
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
    imglist = etree.HTML(res.text).xpath("//li[@class='product-detail-images__image-wrapper']/button/div/div/picture/img/@src")
    print(imglist)
    return price,bianhao,mianliao,cicun,imglist



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
        print(prourl)
        prodata = get_text(prourl)
        print(prodata)
        time.sleep(1)


    pass
if __name__ == '__main__':
    urllist = "https://www.zara.cn/cn/zh/category/1886892/products?ajax=true"
    headUrl(url=urllist)
    pass
