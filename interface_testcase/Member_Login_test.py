import os,time
import unittest
import requests
from common import encrypt_oper, csv_oper,log_oper


class MemberLogin(unittest.TestCase):
    '''会员登录'''

    def setUp(self):
        self.baseurl = encrypt_oper.getURL('interfaceurl', 'authorization')
        self.member=csv_oper.csvRead()
        self.agentName = self.member.get("agent")
        self.player = self.member.get("player1")
        # 登录类型
        self.login_type = '1'
        # 试玩账号类型
        self.account_type = '2'
        self.tokenVal = encrypt_oper.sha1Encrypt(self.agentName)
        # 获取代理返回的安全码
        self.skey = encrypt_oper.getSecurityKey(agent=self.agentName, token=self.tokenVal)
        # 正式玩家加密串
        self.playertokenVal = encrypt_oper.sha1Encrypt(
            self.skey + '|' + self.player + '|' + self.agentName + '|' + self.login_type)
        # 试玩玩家加密串
        self.testtokenVal = encrypt_oper.sha1Encrypt(
            self.skey + '|' + self.account_type + '|' + self.agentName + '|' + self.login_type)
        #记录日志格式
        self.FILEMODE="file_record"
        self.TERMINALMODE="terminal_record"
        self.teroutput=log_oper.logrecord(self.TERMINALMODE)
        self.fileoutput=log_oper.logrecord(self.FILEMODE)
    def test_player_login(self):
        '''验证正式玩家登录'''
        params = {'agent': self.agentName, 'login_type': self.login_type, 'username': self.player,
                  'token': self.playertokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证正式玩家登录:" + self.result['text'])
        self.fileoutput.info("验证正式玩家登录:" + self.result['text'])


    def test_demo_login(self):
        '''验证试玩玩家登录'''
        params = {'agent': self.agentName, 'login_type': self.login_type, 'username': self.player,
                  'token': self.testtokenVal, 'account_type': self.account_type}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证试玩玩家登录:" + self.result['text'])
        self.fileoutput.info("验证试玩玩家登录:" + self.result['text'])


    def test_not_input(self):
        '''验证不传递任何参数'''
        params = {'agent': '', 'login_type': '', 'username': '', 'token': '', 'account_type': ''}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证不传递任何参数:" + self.result['text'])
        self.fileoutput.info("验证不传递任何参数:" + self.result['text'])


    def test_non_exists_agent(self):
        '''验证输入不存在的代理'''
        agent = "aaddfddff"
        tokenVal = encrypt_oper.sha1Encrypt(agent)
        skey = encrypt_oper.sha1Encrypt(agent+'|'+tokenVal)
        token = encrypt_oper.sha1Encrypt(skey + '|' + self.player + '|' + agent + '|' + self.login_type)
        params = {'agent': agent, 'login_type': self.login_type, 'username': self.player, 'token': token}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9004)
        self.assertEqual(self.result['text'], "Invalid Agent")
        self.teroutput.info("验证输入不存在的代理:" + self.result['text'])
        self.fileoutput.info("验证输入不存在的代理:" + self.result['text'])


    def test_non_exists_acctype(self):
        '''验证输入不存在的账号类型'''
        login_type = '3'
        token = self.playertokenVal
        params = {'agent': self.agentName, 'login_type': login_type, 'username': self.player, 'token': token}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证输入不存在的账号类型:" + self.result['text'])
        self.fileoutput.info("验证输入不存在的账号类型:" + self.result['text'])


    def test_toolong_account(self):
        '''验证输入超长的用户名称'''
        username = 'zhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyouzhangyiyou'
        token = encrypt_oper.sha1Encrypt(self.skey + '|' + username + '|' + self.agentName + '|' + self.login_type)
        params = {'agent': self.agentName, 'login_type': self.login_type, 'username': username, 'token': token}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证输入超长的用户名称:" + self.result['text'])
        self.fileoutput.info("验证输入超长的用户名称:" + self.result['text'])


    def test_non_exists_loginype(self):
        '''验证输入不存在的登录类型'''
        login_type = '3'
        token = encrypt_oper.sha1Encrypt(self.skey + '|' + self.player + '|' + self.agentName + '|' + login_type)
        params = {'agent': self.agentName, 'login_type': login_type, 'username': self.player, 'token': token}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证输入不存在的登录类型:" + self.result['text'])
        self.fileoutput.info("验证输入不存在的登录类型:" + self.result['text'])


    def test_logintype_by_h5(self):
        '''验证登录类型为H5'''
        login_type = '2'
        token = encrypt_oper.sha1Encrypt(self.skey + '|' + self.player + '|' + self.agentName + '|' + login_type)
        params = {'agent': self.agentName, 'login_type': login_type, 'username': self.player, 'token': token}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证登录类型为H5:" + self.result['text'])
        self.fileoutput.info("验证登录类型为H5:" + self.result['text'])


    # def test_disabled_IP(self):
    #     '''验证验证禁用IP地址后的登录操作'''
    #     pass
    #
    # def test_member_disabled(self):
    #     '''验证用户被冻结或停用后的登录操作'''
    #     pass
    #
    # def test_system_maintenance(self):
    #     '''验证系统维护时会员登录操作'''
    #     pass
    #
    # def test_deny_IP(self):
    #     '''验证IP地址不允许时的登录'''
    #     pass
    #
    def tearDown(self):
        print(self.result)

if __name__ == "__main__":
    unittest.main()
