# -!- coding: utf-8 -!-
import redis
from projects.happainMysql.mySql import  mysql

# 创建连接池
Pool = redis.ConnectionPool(host='127.0.0.1',password="", port=6379, max_connections=32,db=1)



class MyRedis():
    conn = None
    @staticmethod
    def instances():
        MyRedis.conn = redis.Redis(connection_pool=Pool, decode_responses=True,db=1)
        pass

    # 检测集合中是否存在数据
    @staticmethod
    def check_data(key,value):
        if  MyRedis.conn is None:
            MyRedis.instances()
        if MyRedis.conn.sismember(key,value):
            return True
        else:
            MyRedis.conn.sadd(key,value)
            return False
if __name__ == '__main__':
    conn=mysql(localhost='127.0.0.1',username='root',password='123456',mydb='happain-scrapy')
    res =conn.execute_res("select url from zmero_vedio")
    for i in res:
        print(i[0])
        MyRedis.check_data("zmero_spider", i[0])
