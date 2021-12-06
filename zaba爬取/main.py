# -!- coding: utf-8 -!-
import os
import time
import requests
import re
from lxml import etree
import configparser
from xlutils.copy import copy
import xlwt
import xlrd
import datetime

class Excel_write():
    def __init__(self,path):
        self.path=path
        self.ex=xlwt.Workbook()

        pass


    def add_sheet(self,name,data_list,col=-1):

        sheet_list=[]
        if type(name)==list:
            for i in name:
                sh=self.ex.add_sheet(i, cell_overwrite_ok=True)
                if col!=-1:
                    self.set_width(sh,len(data_list),col)
                self.write(sh,0,data_list)

                sheet_list.append(sh)

            return sheet_list
        else:
            sh = self.ex.add_sheet(name, cell_overwrite_ok=True)
            if col != -1:
                self.set_width(sh, len(data_list), col)
            self.writes(sh, 0, data_list)
            return  sh



    def write(self, sheet, hang, data, index):
        for i in zip(index, data):
            sheet.write(hang, i[0], i[1])


    def writes(self,sheet,hang,data):
        for i in range(0,len(data)):
            sheet.write(hang,i,data[i])


    def set_width(self,sh,long_num,width):
        for i in range(0,long_num):
            sh.col(i).width = 256 * width


    def save(self):
        self.ex.save(self.path)




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


# 读取配置
def readConfig():
    cf = configparser.ConfigParser()
    cf.read("config.ini",encoding='utf-8')
    imgpath = cf.items('config')
    data_dict = {}
    for i in imgpath:
        data_dict[i[0]] = i[1]
    return data_dict




def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")



# 输入页面信息
def headUrl(url):
    excel = Excel_write('result.xls')
    sheet = excel.add_sheet("demo",['名称','编号','价格','材质','尺寸','图片id','链接'],15)
    hang = 1


    temurl ="https://www.zara.cn/cn/zh/{}-p{}.html"
    headers= {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    res = requests.get(url=url,headers= headers)
    data = res.json()['productGroups'][0]['elements']

    for i in data:
        name = i['commercialComponents'][0]['seo']['keyword']
        proid = i['commercialComponents'][0]['seo']['seoProductId']
        prourl = temurl.format(name,proid)
        if not quchong(proid):
            print(prourl)
            prodata = get_text(prourl)
            if prodata is None:
                continue
            time.sleep(1)
            # 下载图片
            for j in enumerate(prodata[-1]):
                downloadImg(proid,prodata,j[1],j[0])
            excel.writes(sheet,hang,[prodata[0], prodata[2], prodata[1], prodata[3], prodata[4], proid,prourl])
            # write_excel_xls_append(path="result.xls", value=[[prodata[0], prodata[2], prodata[1], prodata[3], prodata[4], proid]])
    excel.save()




# 下载图片
def downloadImg(proid,obj,url,num):
    tem = '{}_{}_{}_{}_{}'.format(proid,obj[1].replace("¥",'').strip(),obj[3].replace("\n",''),obj[4].replace("/",'').replace("\\",'').replace('"','').replace("'",''),num)
    headers= {
        'cookie':'optimizelyEndUserId=oeu1637356690393r0.7057703069582593; '
                 '_abck=893741F99DB3854303ED009168895D2F~0~YAAQRQ1x3wJTFhd9AQAAawy8cAY789FhSRXX4vK5ic720CJdS7vy32Ld6TzjZ8wmMT5NCj/t7dMA17wbuWX4ak8h9oIArQ9LJNpEhoep76QKUxtf13eVoCn8vRK6D4wiCh4iTlj17mszH8O0YmA/ygOORPTTXJbz0DARnDrQn3ADzYFSK0HMa6dEkRQ2Kv0z8WfHLvyNz3dD4At+cDOKrAyiyeozPnBl5cNQCtNPKew1AuVfNHnNZT1f0aefrKwDRmJgYu2LSqNAcbJpn5Dz3sJWjjE4g375ewDcM0Rw39UvB4cY78Yv7KuepGMMZ6GSkE4gYJBGkE8kpopcHgt5N9PcdftGb85ZmttCxOxYX3VOUQdUthJvptt46cab0hEqksNKtfdn27eMALrFZruHNZbbMVrT~-1~-1~-1; _ga=GA1.2.2046539325.1637356694; RT="z=1&dm=zara.cn&si=27af5e6b-adba-44f8-908b-2d366b4077f9&ss=kwma8ihf&sl=7&tt=36d&bcn=%2F%2F684d0d4c.akstat.io%2F&ul=fkwo&hd=fkwy"; _ga_HCEXQGE0MW=GS1.1.1638287766.12.1.1638288492.0',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    if not os.path.exists('./image/'+data_dict['imgpath']):
        os.mkdir('./image/'+data_dict['imgpath'])
    with open('./image/{}/{}.jpg'.format(data_dict['imgpath'],tem),'wb') as f:
        res = requests.get(url=url,headers= headers)
        f.write(res.content)
        print(tem+'图片下载完成')
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





data_dict = readConfig()
if __name__ == '__main__':
    num =re.compile('v1=(.*)').findall(data_dict['link'])[0]
    urllist = "https://www.zara.cn/cn/zh/category/{}/products?ajax=true".format(num)
    headUrl(url=urllist)
