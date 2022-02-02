# -!- coding: utf-8 -!-


# 获取延时数据
import os
import random
import re
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder
from lxml import etree



# 延时
import requests


def getTime():
    with open('config.txt','r') as f:
        data = f.readlines()[0].split("=")[1]
    return data

def getDelay():
    with open('config.txt','r') as f:
        data = f.readlines()[1].split("=")[1]
    return data

# 随机获取图片
def getImages():
    image = os.listdir("./images")
    img = random.choice(image)
    return os.path.join(".\images",img)


# 随机选择文章
def getArticle(city):
    citylist = {'北京': '1', '上海': '2', '深圳': '6', '广州': '5', '杭州': '26', '长沙': '158', '成都': '281', '重庆': '4', '南昌': '194', '西安': '271', '厦门': '56', '福州': '55',
                '天津': '3', '沈阳': '205', '南京': '181', '武汉': '145', '郑州': '115', '合肥': '38', '宁波': '28', '苏州': '190', '昆明': '323'}
    text = ''
    for i in citylist.items():
        if i[1] == city:
            text = i[0]
    if not os.path.exists("articles/{}".format(text)):
        print("不存在{}目录".format(text))
        return None
    article = os.listdir("articles/{}".format(text))
    if len(article) ==0:
        print("{}城市目录下没有文件".format(text))
        return None
    a = random.choice(article)
    return os.path.join("articles/{}".format(text), a)



# 检测字符串是否合格
def checkContent(content):
    headers= {'host':'www.yebzj.com','content-type':'application/x-www-form-urlencoded','x-requested-with':'XMLHttpRequest',
              'cookie':cookies,'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    data ={'value':content}
    res =  requests.post(url="https://www.yebzj.com/javascript.php?part=chk_badwords&catid=1554",headers=headers,data=data,verify=False)
    weijin = re.compile('<b>(.*?)</b>').findall(res.text)
    if len(weijin) >0:
        return weijin
    return None


# 随机选择一个文件 返回正确文本
def getArticleRight(city):
    path = getArticle(city)
    if path is None:
        return None,None
    with open(path,'r') as f:
        content = f.read()
    a = etree.HTML(content).xpath("//div")[0].xpath("string(.)")
    h3 = etree.HTML(content).xpath("//div/h3/text()")[0]
    value = checkContent(a)
    if value is not None:
        for i in value:
            content = content.replace(i,'')
        content = etree.HTML(content).xpath("//div")[0].xpath("string(.)")
    os.remove(path)
    return h3,content





# 发送请求
def send(title,content,imagepath,city,area):
    m = MultipartEncoder(
        fields={
            "act":'dopost',
            "ismember":'1',
            'id': '',
              # 需要去页面找值
            'mixcode':'c4edc6ff0a33f5d716b8634c2c2f6426',
            'lat':'',
            'lng':'',
            'catid': '1554',
            # 城市
            'cityid': str(city),
            'areaid':str(area),
            'streetid':'',
            'endtime':'0',
              # 标题
            'title':title,
            'mappoint': '',
              # 公司
            'extra[company]':'首席商务KTV招聘',
            'extra[job]':'1,7,9,20',
            'extra[salary]':'10',
            'extra[sex_demand]':'3',
            'extra[fuli]':'1,2,3,4,5,8',
            'content':content,
            # 图片
            'mymps_img_0':(
                ('1.jpg', open(imagepath,'rb'), 'image/jpg')
            ),
            'contact_who':'阿信',
            'tel':'13177853190',
            'qq':'1608314873',
            'weixin':'wyzp6688'
        }

    )
    headers = {'Host': 'www.yebzj.com', 'Cookie': cookies,
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    headers['Content-Type'] = m.content_type
    res = requests.post(url="https://www.yebzj.com/ph.php?action=input",data=m,headers=headers,verify=False)
    if '发布成功' in res.text:
        print("发布成功")
    else:
        print("发布失败")



def getCityArea(city):
    res = requests.post(url="https://www.yebzj.com/include/selectwhere.php?action=getarea&parentid={}".format(city),verify=False,
                  headers={'cookie':cookies},
                  )
    city = re.compile(r"value=\\'(.*?)\\'").findall(res.text)[-1]
    return city


# 登陆
def login(username,password) :
    m = MultipartEncoder(
        fields={
            'mod':'login',
            'action':'dopost',
            'url':'https://www.yebzj.com/ph.php?action=post&amp;catid=1554&amp;cityid=0',
            'userid':username,
            'userpwd':password,
            'memory':'on',
            'log_submit':'立即登录'
        }

    )
    headers = {'Host': 'www.yebzj.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    headers['Content-Type'] = m.content_type
    res = requests.post(url="https://www.yebzj.com/mr.php",data=m,headers=headers,verify=False)
    d = "{}={};"
    tem = ''
    for i in res.cookies:
        tem +=d.format(i.name,i.value)
    return tem
# 从文件获取账号密码
def getUser():
    with open('user.txt','r') as f:
        data = [i.replace('\n','').split("-----") for i in  f.readlines()]
    return data

# 得到cookies
def getCookies():
    for i in userlist:
        cookies = login(i[0], i[1])
        yield cookies

global cookies
userlist = getUser()

if __name__ == '__main__':


    timenum = getTime()
    delay = int(getDelay())
    print("延时{}秒后启动".format(timenum))
    time.sleep(int(timenum))
    print("开始启动")


    citylist = {'北京': '1', '上海': '2', '深圳': '6', '广州': '5', '杭州': '26', '长沙': '158', '成都': '281', '重庆': '4', '南昌': '194', '西安': '271', '厦门': '56', '福州': '55',
                '天津': '3', '沈阳': '205', '南京': '181', '武汉': '145', '郑州': '115', '合肥': '38', '宁波': '28', '苏州': '190', '昆明': '323'}



    # 30个
    num = 0
    cc = getCookies()
    cookies = next(cc)
    flag = True
    while True:
        for i in citylist.items():
            print("当前发布{}城市".format(i[0]))
            area = getCityArea(i[1])
            # 获取正确的文章内容和标题
            h3,content = getArticleRight(i[1])
            if h3 is None:
                time.sleep(0.5)
                continue
            # 随机选择图片

        
            img = getImages()
            # 发布
            send(h3,content,img,i[1],area)
            num+=1
            if num>=30:
                try:
                    cookies = next(cc)
                except:
                    flag = False
                    break
                num=0
            time.sleep(delay)
        if flag == False:
            break
    input()
