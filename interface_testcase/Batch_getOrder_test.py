import os,time
import unittest
import requests
import random
from common import encrypt_oper, csv_oper,log_oper


class BatchGetOrder(unittest.TestCase):
    '''批量获取注单信息'''

    def setUp(self):
        self.baseurl = encrypt_oper.getURL('interfaceurl', 'orderList')
        self.member = csv_oper.csvRead()
        self.agentName = self.member.get("agent")
        self.player = self.member.get("player1")
        self.deadline = ''
        self.tokenVal = encrypt_oper.sha1Encrypt(self.agentName)
        # 获取代理返回的安全码
        self.skey = encrypt_oper.getSecurityKey(agent=self.agentName, token=self.tokenVal)
        self.tokenVal = encrypt_oper.sha1Encrypt(self.skey + '|' + self.deadline + '|' + self.agentName)
        #记录日志格式
        self.FILEMODE="file_record"
        self.TERMINALMODE="terminal_record"
        self.teroutput=log_oper.logrecord(self.TERMINALMODE)
        self.fileoutput=log_oper.logrecord(self.FILEMODE)

    def test_get_order(self):
        '''验证获取有注单的玩家数据'''
        params = {'agent': self.agentName, 'username': self.player,'token': self.tokenVal,'deadline':''}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证获取有注单的玩家数据:" + self.result['text'])
        self.fileoutput.info("验证获取有注单的玩家数据:" + self.result['text'])

    def test_get_EmpytOrder(self):
        '''验证获取未下注的代理和玩家数据'''
        tokenVal = encrypt_oper.sha1Encrypt('auto_agent')
        skey = encrypt_oper.getSecurityKey(agent='auto_agent', token=tokenVal)
        tokenVal = encrypt_oper.sha1Encrypt(skey + '|' + self.deadline + '|' + 'auto_agent')
        params = {'agent': 'auto_agent', 'username': 'guyuanqiang', 'token': tokenVal,
                  'deadline': ''}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9009)
        self.assertEqual(self.result['text'], "Data is empty")
        self.teroutput.info("验证获取未下注的代理和玩家数据:" + self.result['text'])
        self.fileoutput.info("验证获取未下注的代理和玩家数据:" + self.result['text'])

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
