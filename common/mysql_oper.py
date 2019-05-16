from pymysql import connect,cursors
from pymysql import OperationalError
import os
import configparser
rootDir=os.path.dirname(os.getcwd())
cf=configparser.ConfigParser()
cf.read(filenames=rootDir+'/conf/db_config.ini',encoding='utf-8')
host=cf.get('mysqlconf','host')
port=cf.get('mysqlconf','port')
user=cf.get('mysqlconf','user')
password=cf.get('mysqlconf','password')
dbname=cf.get('mysqlconf','db_name')

'''封装MySQL基本操作'''
class DB:
    def __init__(self):
        try:
            #连接数据库
            self.conn=connect(host=host,user=user,password=password,db=dbname,charset='utf8mb4',cursorclass=cursors.DictCursor)
        except OperationalError as e:
            print("MySQL 错误{n1:d}:{n2:s}".format(n1=e.args[0],n2=e.args[1]))

    #清除表数据
    def clear(self,table_name):
        pass

    #插入表数据
    def insert(self,table_name,table_data):
        pass
    #关闭数据库
    def close(self):
        self.conn.close()
if __name__=='__main__':
    db=DB()
    table_name=""
    db.clear(table_name)
    db.close()

