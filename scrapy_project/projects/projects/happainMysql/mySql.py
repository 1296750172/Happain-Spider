import time

import pymysql
from projects.happainTranslate.main import translate

class mysql(object):
    __localhost=""
    __username=""
    __password=""
    __my_db=""
    __charset=""
    __con=None
    __cursor=None
    # 初始化数据库
    def __init__(self,localhost,username,password,mydb,charset="utf8"):
        self.__localhost=localhost
        self.__username=username
        self.__password=password
        self.__my_db=mydb
        self.__charset=charset
        print("数据库初始化成功")
        self.connect()
    #连接数据库
    def connect(self):
        try:

            self.__con=pymysql.Connect(self.__localhost,self.__username,self.__password,self.__my_db,charset=self.__charset)
            self.__cursor=self.__con.cursor()
            print("数据库连接成功")
        except Exception as e:
            print("数据库连接错误"+e)
    # 执行数据库语句
    def execute(self,sql):
        try:
            self.__con.ping(reconnect=True)
            self.__cursor.execute(sql)
            self.__con.commit()
            return self.__cursor.lastrowid
        except Exception as e:
            # self.__con.rollback()
            print("执行语句错误"+e)
            return False

    # 执行数据库语句 返回结果集
    def execute_res(self,sql):
        try:
            self.__con.ping(reconnect=True)
            self.__cursor.execute(sql)
            result=self.__cursor.fetchall()
            # 返回值为所有数据条的list
            # 每个list里面包含字段的元素
            return result
        except Exception as e:
            print("查询语句错误"+e)
            return None

    # 关闭数据库
    def close(self):
        try:
            self.__con.close()
            print("关闭数据库连接")
        except Exception as e:
            print("数据库关闭失败"+e)



if __name__ == '__main__':
    conn=mysql(localhost='127.0.0.1',username='root',password='123456',mydb='happain-scrapy')
    data = conn.execute_res("select `name` from zmero_performer")
    for i in data:
        na = translate(i[0], src='jp', tar="zh")
        print(na)
        print(i[0])
        conn.execute("update  zmero_performer set name_zh ='{}' where `name` ='{}'".format(na,i[0]))
        time.sleep(0.1)


