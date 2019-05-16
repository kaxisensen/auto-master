import os,time
import unittest
import requests
import random
from common import encrypt_oper, csv_oper,log_oper


class New_MemberWithDrawal(unittest.TestCase):
    '''会员取款操作'''

    def setUp(self):
        self.baseurl = encrypt_oper.getURL('interfaceurl', 'new_withDrawal')
        self.member = csv_oper.csvRead()
        self.agentName = self.member.get("agent")
        self.player = self.member.get("player1")
        self.amount = str(random.randint(1, 10))
        self.order_number = encrypt_oper.serialOrder
        self.tokenVal = encrypt_oper.sha1Encrypt(self.agentName)
        # 获取代理返回的安全码
        self.skey = encrypt_oper.getSecurityKey(agent=self.agentName, token=self.tokenVal)
        self.tokenVal = encrypt_oper.sha1Encrypt(
            self.skey + '|' + self.player + '|' + self.amount + '|'+self.order_number+'|' + self.agentName)
        self.FILEMODE="file_record"
        self.TERMINALMODE="terminal_record"
        self.teroutput=log_oper.logrecord(self.TERMINALMODE)
        self.fileoutput=log_oper.logrecord(self.FILEMODE)



    def test_Member_withDrawal(self):
        '''验证会员正常取款操作'''
        params = {'agent': self.agentName, 'username': self.player, 'amount': self.amount, 'token': self.tokenVal,
                  'order_number': self.order_number}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证会员正常取款操作:" + self.result['text'])
        self.fileoutput.info("验证会员正常取款操作:" + self.result['text'])


    def test_negative_withDrawal(self):
        '''验证会员取款时输入负数'''
        amount = '-1'
        self.tokenVal = encrypt_oper.sha1Encrypt(self.skey + '|' + self.player + '|' + amount + '|'+ self.order_number+'|' + self.agentName)
        params = {'agent': self.agentName, 'username': self.player, 'amount': amount, 'token': self.tokenVal,
                  'order_number': self.order_number}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证会员取款时输入负数:" + self.result['text'])
        self.fileoutput.info("验证会员取款时输入负数:" + self.result['text'])


    def test_noinput_withDrawal(self):
        '''验证取款时不输入取款金额'''
        amount = ''
        self.tokenVal = encrypt_oper.sha1Encrypt(self.skey + '|' + self.player + '|' + amount + '|'+self.order_number+'|' + self.agentName)
        params = {'agent': self.agentName, 'username': self.player, 'amount': amount, 'token': self.tokenVal,
                  'order_number': self.order_number}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证取款时不输入取款金额:" + self.result['text'])
        self.fileoutput.info("验证取款时不输入取款金额:" + self.result['text'])


    def test_Exceed_balance(self):
        '''验证取款时超过最大余额'''
        amount = '1000000000'
        self.tokenVal = encrypt_oper.sha1Encrypt(
            self.skey + '|' + self.player + '|' + amount + '|'+self.order_number+'|' + self.agentName)
        params = {'agent': self.agentName, 'username': self.player, 'amount': amount, 'order_number': self.order_number,'token': self.tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 3001)
        self.assertEqual(self.result['text'], "Insufficient balance")
        self.teroutput.info("验证取款时超过最大余额:" + self.result['text'])
        self.fileoutput.info("验证取款时超过最大余额:" + self.result['text'])


    def test_user_not_exists(self):
        '''验证为不存在的用户取款'''
        player = ''.join(random.sample('abcdefghigklmnopqrstuvwxyz_0123456789',6))
        self.tokenVal = encrypt_oper.sha1Encrypt(self.skey + '|' + player + '|' + self.amount + '|'+self.order_number+'|' + self.agentName)
        params = {'agent': self.agentName, 'username': player, 'amount': self.amount, 'token': self.tokenVal,
                  'order_number': self.order_number}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 1007)
        self.assertEqual(self.result['text'], "User not exist")
        self.teroutput.info("验证为不存在的用户取款:" + self.result['text'])
        self.fileoutput.info("验证为不存在的用户取款:" + self.result['text'])
    #
    #
    # def test_system_maintenance(self):
    #     '''验证系统维护时调用取款接口'''
    #     pass
    #
    # def test_agent_locked(self):
    #     '''验证锁定厅主或代理充值接口'''
    #     pass
    #
    # def test_user_locked(self):
    #     '''验证用户账号被锁定或停用'''
    #     pass
    #
    # def test_user_locked(self):
    #     '''验证用户账号被锁定或停用'''
    #     pass
    #
    # def test_whitelist_disabled(self):
    #     '''验证将厅主从白名单中设置为不可用后获取会员取款'''
    #     pass

    def tearDown(self):
        print(self.result)


if __name__ == '__main__':
    unittest.main()

