import hashlib,time
import requests,random
import os, configparser, json
from common import csv_oper

d = os.path.dirname(__file__)
parent_path = os.path.dirname(d)
SECOND=1
serialOrder = 'SN' + str(random.randrange(1000, 100000000)) + ''.join(
random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIGKLMNOPQRSTUVWXYZ', 19))

# 为指定的字符串使用SHA1加密
def sha1Encrypt(encryptStr):
    sha1hash = hashlib.sha1()
    sha1hash.update(encryptStr.encode('utf-8'))
    return sha1hash.hexdigest()

# 获取代理的SecurityKey
def getSecurityKey(**kwargs):
    time.sleep(SECOND)
    try:
        file_path = parent_path + '/conf/db_config.ini'
        cf = configparser.ConfigParser()
        cf.read(filenames=file_path, encoding='utf-8')
        getkeyURL = cf.get('interfaceurl', 'getkey')
        r = requests.post(getkeyURL, data=kwargs,timeout=20)
        content = r.json()
        content = content.get('result')
        return content.get('security_key')
    except (AttributeError,TypeError):
        print("获取SecurityKey接口时，请求超时未能返回SecurityKey")



#获取配置文件中接口的URL
def getURL(key,value):
    file_path = parent_path + '/conf/db_config.ini'
    cf = configparser.ConfigParser()
    cf.read(filenames=file_path, encoding='utf-8')
    return cf.get(key,value)


#获取存取款的单号
def getOrder(option):
        member = csv_oper.csvRead()
        agentName = member.get("agent")
        player = member.get("player1")
        amount = '1'
        tokenVal = sha1Encrypt(agentName)
        skey = getSecurityKey(agent=agentName, token=tokenVal)
        tokenVal = sha1Encrypt(skey + '|' + player + '|' + amount + '|' + agentName)
        params = {'agent': agentName, 'username': player, 'amount': amount, 'token': tokenVal}
        if option == "deposit":
            baseurl = getURL('interfaceurl', 'deposit')
            r=requests.post(url=baseurl,data=params,timeout=20)
            order=r.json()
            order=order.get('result').get('order_sn')
            tokenVal=sha1Encrypt(skey+'|'+order+'|'+agentName)
            return {'agent':agentName,'username':player,'token':tokenVal,'serial':order}
        elif option=='withdrawal':
            baseurl = getURL('interfaceurl', 'withDrawal')
            r=requests.post(url=baseurl,data=params,timeout=20)
            order=r.json()
            order=order.get('result').get('order_sn')
            tokenVal = sha1Encrypt(skey + '|' + order + '|' + agentName)
            return {'agent':agentName,'username':player,'token':tokenVal,'serial':order}
        else:
            return "parameter error!"




