import os
import configparser
from pymongo import MongoClient

d = os.path.dirname(__file__)
parent_path = os.path.dirname(d)
file_path = parent_path + '/conf/db_config.ini'
cf = configparser.ConfigParser()
cf.read(filenames=file_path, encoding='utf-8')
host=cf.get('mongodbconf','host')
port=cf.get('mongodbconf','port')
user=cf.get('mongodbconf','user')
password=cf.get('mongodbconf','password')
dbname=cf.get('mongodbconf','db_name')
uri="mongodb://"+user+":"+"password"+"@"+host+":"+port+"/"+dbname
class MongoDB:
    def __init__(self,uri):
        self.client=MongoClient(uri)

    def query(self,collName,startDate,endDate):
        '''MongoDB查询指定集合中的数据'''
        collName=self.db[collName]
        pass

    def close(self):
        self.client.close()


a=MongoDB(uri)


