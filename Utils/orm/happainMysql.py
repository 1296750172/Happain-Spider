# -!- coding: utf-8 -!-
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import traceback

class happainMysql():

    def __init__(self, username, password, host, db, port):
        try:
            engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{db}')
            # 获取连接
            self.conn = engine.connect()
            # 操作增删改查抽象
            self.session = sessionmaker(bind=engine)()
        except Exception as e:
            print(e)
            print(traceback.print_exc())
            print("mysql数据库连接异常")


    # 释放资源
    def __del__(self):
        self.conn.close()


    # 执行增删改
    def execute(self, sql):
        try:
            res = self.conn.execute(sql)
            # 插入后返回的id
            num = res.lastrowid
        except Exception as e:
            print(e)
            print(traceback.print_exc())
            print("操作数据库失败")
            return None
        return num

    # 执行查询操作
    def execute_query(self,sql):
        try:
            res = self.conn.execute(sql)
        except Exception as e:
            print(e)
            print(traceback.print_exc())
            print("查询数据库失败")
            return None

        return list(res)


    # orm操作
    def query(self):
        pass

# Base = declarative_base()
# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     username = Column(String(50))
#     password = Column(String(50))
class User():
    def __init__(self):
        self.username = '';
        self.password = ''

if __name__ == '__main__':
    mysql = happainMysql('root', '123456', '127.0.0.1', 'test', 3306)
    # mysql.execute_query("select * from user")
    print(dir(User))

    pass
