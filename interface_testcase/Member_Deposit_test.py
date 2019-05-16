import os,time
import unittest
import requests
import random
from common import encrypt_oper, csv_oper,log_oper


class MemberDeposit(unittest.TestCase):
    '''会员充值操作'''

    def setUp(self):
        self.baseurl = encrypt_oper.getURL('interfaceurl', 'deposit')
        self.member = csv_oper.csvRead()
        self.agentName = self.member.get("agent")
        self.player = self.member.get("player1")
        self.amount = str(random.randint(10, 100))
        self.tokenVal = encrypt_oper.sha1Encrypt(self.agentName)
        # 获取代理返回的安全码
        self.skey = encrypt_oper.getSecurityKey(agent=self.agentName, token=self.tokenVal)
        self.tokenVal = encrypt_oper.sha1Encrypt(
            self.skey + '|' + self.player + '|' + self.amount + '|' + self.agentName)
        #记录日志格式
        self.FILEMODE="file_record"
        self.TERMINALMODE="terminal_record"
        self.teroutput=log_oper.logrecord(self.TERMINALMODE)
        self.fileoutput=log_oper.logrecord(self.FILEMODE)


    def test_Member_Deposit(self):
        '''验证会员正常充值操作'''
        params = {'agent': self.agentName, 'username': self.player, 'amount': self.amount, 'token': self.tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证会员正常充值操作:" + self.result['text'])
        self.fileoutput.info("验证会员正常充值操作:" + self.result['text'])


    def test_negative_Deposit(self):
        '''验证给会员充入负数'''
        amount = '-1'
        tokenVal = encrypt_oper.sha1Encrypt(self.skey + '|' + self.player + '|' + amount + '|' + self.agentName)
        params = {'agent': self.agentName, 'username': self.player, 'amount': amount, 'token': self.tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证给会员充入负数:" + self.result['text'])
        self.fileoutput.info("验证给会员充入负数:" + self.result['text'])


    def test_not_input(self):
        '''验证充值参数不输入内容'''
        params = {'agent': '', 'username': '', 'amount': '', 'token': ''}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证充值参数不输入内容:" + self.result['text'])
        self.fileoutput.info("验证充值参数不输入内容:" + self.result['text'])


    def test_larger_Deposit(self):
        '''验证超过充值的最大范围'''
        amount = '1000000000'
        tokenVal = encrypt_oper.sha1Encrypt(self.skey + '|' + self.player + '|' + amount + '|' + self.agentName)
        params = {'agent': self.agentName, 'username': self.player, 'amount': amount, 'token': self.tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证超过充值的最大范围:" + self.result['text'])
        self.fileoutput.info("验证超过充值的最大范围:" + self.result['text'])


    # def test_system_maintenance(self):
    #     '''系统维护时调用充值接口'''
    #     pass
    #
    # def test_locked_agent(self):
    #     '''锁定厅主或代理充值接口'''
    #     pass
    #
    # def test_locked_user(self):
    #     '''用户账号被锁定或停用'''
    #     pass
    # def test_whilte_list_disabled(self):
    #     '''验证厅主从白名单中置为不可用时，会员存取款'''
    #需求已更改为不存在的会员调用登录接口时就自动注册
    def test_non_exists_user(self):
        '''验证为不存在的会员充值'''
        player = 'test1'
        tokenVal = encrypt_oper.sha1Encrypt(self.skey + '|' + player + '|' + self.amount + '|' + self.agentName)
        params = {'agent': self.agentName, 'username': player, 'amount': self.amount, 'token': tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证为不存在的会员充值:" + self.result['text'])
        self.fileoutput.info("验证为不存在的会员充值:" + self.result['text'])


    def tearDown(self):
        print(self.result)


if __name__ == "__main__":
    unittest.main()

