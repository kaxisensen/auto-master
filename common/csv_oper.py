import configparser
import os,sys
import csv, random
from common import log_oper
import logging
logger = logging.getLogger(os.path.basename(__file__))

# 从CSV文件中随机取出一组数据
def csvRead():
    d = os.path.dirname(__file__)
    parent_path = os.path.dirname(d)
    file_path = parent_path + '/conf/db_config.ini'
    cf = configparser.ConfigParser()
    cf.read(filenames=file_path, encoding='utf-8')
    csvfile = parent_path + cf.get('csvconf', 'csvfile')
    result = []
    with open(file=csvfile, encoding='utf-8', mode='r') as f:
        for row in csv.DictReader(f, dialect='unix'):
            result.append(row)
    rndnum = random.randint(0, len(result)-1)
    msg = "调用了生成securityKey函数"
    logger.info(msg)
    return result[rndnum]
