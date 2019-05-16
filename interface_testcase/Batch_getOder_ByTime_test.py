import os,time
import unittest
import requests
import random
from common import encrypt_oper, csv_oper,log_oper
from datetime import datetime,date,timedelta
class BatchGetOrderByTime(unittest.TestCase):
    '''根据时间段批量获取注单信息'''
    def setUp(self):
        _currtime = datetime.now()
        _currenttime=datetime.strftime(_currtime, '%Y-%m-%d %H:%M:%S')
        _expireTime=datetime.strftime(_currtime - timedelta(days=5), '%Y-%m-%d %H:%M:%S')
        self.baseurl = encrypt_oper.getURL('interfaceurl', 'getDateList')
        self.member = csv_oper.csvRead()
        self.agentName = self.member.get("agent")
        self.player = self.member.get("player1")
        self.endTime=_currenttime
        self.startTime=_expireTime
        self.tokenVal = encrypt_oper.sha1Encrypt(self.agentName)
        # 获取代理返回的安全码
        self.skey = encrypt_oper.getSecurityKey(agent=self.agentName, token=self.tokenVal)
        self.tokenVal = encrypt_oper.sha1Encrypt(self.skey + '|' + self.startTime+'|'+self.endTime + '|' + self.agentName)
        #记录日志格式
        self.FILEMODE="file_record"
        self.TERMINALMODE="terminal_record"
        self.teroutput=log_oper.logrecord(self.TERMINALMODE)
        self.fileoutput=log_oper.logrecord(self.FILEMODE)
    def test_get_order(self):
        '''验证获取有注单的玩家数据'''
        tokenVal = encrypt_oper.sha1Encrypt('chenxiuhua')
        skey = encrypt_oper.getSecurityKey(agent='chenxiuhua', token=tokenVal)
        tokenVal = encrypt_oper.sha1Encrypt(skey + '|' + '2018-07-10 13:32:21'+'|'+'2018-07-16 13:32:27' + '|' + 'chenxiuhua')
        params = {'username': 'pangchunyi','agent': 'chenxiuhua', 'start_date':'2018-07-10 13:32:21','end_date':'2018-07-16 13:32:27','token': tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证获取有注单的玩家数据:" + self.result['text'])
        self.fileoutput.info("验证获取有注单的玩家数据:" + self.result['text'])

    def test_get_no_order(self):
        '''验证获取未下注的代理和玩家数据'''
        agentName = 'auto_agent'
        player = 'guyuanqiang'
        tokenVal = encrypt_oper.sha1Encrypt(agentName)
        # 获取代理返回的安全码
        skey = encrypt_oper.getSecurityKey(agent=agentName, token=tokenVal)
        tokenVal = encrypt_oper.sha1Encrypt(skey + '|' + self.startTime+'|'+self.endTime + '|' + agentName)
        params = {'username': player,'agent': agentName, 'start_date':self.startTime,'end_date':self.endTime,'token': tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9009)
        self.assertEqual(self.result['text'], "Data is empty")
        self.teroutput.info("验证获取未下注的代理和玩家数据:" + self.result['text'])
        self.fileoutput.info("验证获取未下注的代理和玩家数据:" + self.result['text'])

    def test_morethan7_get_order(self):
        '''验证选择跨度大于7天的日期查询注单信息'''
        tokenVal = encrypt_oper.sha1Encrypt('chenxiuhua')
        skey = encrypt_oper.getSecurityKey(agent='chenxiuhua', token=tokenVal)
        tokenVal = encrypt_oper.sha1Encrypt(skey + '|' + '2018-07-10 00:00:00'+'|'+'2018-07-19 00:00:00' + '|' + 'chenxiuhua')
        params = {'username': 'pangchunyi','agent': 'chenxiuhua', 'start_date':'2018-07-10 00:00:00','end_date':'2018-07-19 00:00:00','token': tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 2001)
        self.assertEqual(self.result['text'], "The time span is too big")
        self.teroutput.info("验证选择跨度大于7天的日期查询注单信息:" + self.result['text'])
        self.fileoutput.info("验证选择跨度大于7天的日期查询注单信息:" + self.result['text'])

    # def test_system_maintenance(self):
    #     '''验证系统维护时调用取款接口'''
    #     pass

    # def test_whitelist_disabled(self):
    #     '''验证将厅主从白名单中设置为不可用后获取会员取款'''
    #     pass

    def tearDown(self):
        print(self.result)


if __name__ == '__main__':
    unittest.main()

