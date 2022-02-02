from projects.happainMysql.mySql import mysql




# 检测是否已经爬取
def movie_check(url):
    conn = mysql(localhost='127.0.0.1', username='root', password='123456', mydb='happain-scrapy')
    res = conn.execute_res("select id from movie_spider where url='{}'".format(url))
    conn.close()
    if len(res) == 0:
        return False
    else:
        return True


# 插入数据
def movie_insert(**kwargs):
    conn = mysql(localhost='127.0.0.1', username='root', password='123456', mydb='happain-scrapy')
    sql = "insert into movie_spider(title,url,flag,file_num) values ('{title}','{url}','{flag}',{file_num})".format(
        title=kwargs['title'],url=kwargs['url'],flag=kwargs['flag'],file_num=kwargs['file_num'])
    print(sql)
    result = conn.execute(sql)
    conn.close()
    return result

if __name__ == '__main__':
    movie_insert(title="aaa",url="ccc",flag='1',file_num=2)
