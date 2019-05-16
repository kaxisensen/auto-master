import os,time
import unittest
import requests
import random
from common import encrypt_oper, csv_oper,log_oper


class MemberStatus(unittest.TestCase):
    '''获取会员信息'''

    def setUp(self):
        self.baseurl = encrypt_oper.getURL('interfaceurl', 'userStatus')
        self.member = csv_oper.csvRead()
        self.agentName = self.member.get("agent")
        self.player = self.member.get("player1")
        self.tokenVal = encrypt_oper.sha1Encrypt(self.agentName)
        # 获取代理返回的安全码
        self.skey = encrypt_oper.getSecurityKey(agent=self.agentName, token=self.tokenVal)
        self.tokenVal = encrypt_oper.sha1Encrypt(self.skey + '|' + self.player + '|' + self.agentName)
        #记录日志格式
        self.FILEMODE="file_record"
        self.TERMINALMODE="terminal_record"
        self.teroutput=log_oper.logrecord(self.TERMINALMODE)
        self.fileoutput=log_oper.logrecord(self.FILEMODE)


    def test_Member_OnLine(self):
        '''验证会员在线时获取会员状态'''
        params = {'agent': self.agentName, 'username': self.player, 'token': self.tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证会员在线时获取会员状态:" + self.result['text'])
        self.fileoutput.info("验证会员在线时获取会员状态:" + self.result['text'])


    def test_Member_OffLine(self):
        '''验证会员离线时获取会员状态'''
        agentName = 'GUANGXIZIZHUHUAGONG_'
        player = 'pengyunfei'
        tokenVal = encrypt_oper.sha1Encrypt(agentName)
        # 获取代理返回的安全码
        skey = encrypt_oper.getSecurityKey(agent=agentName, token=tokenVal)
        tokenVal = encrypt_oper.sha1Encrypt(skey + '|' + player + '|' + agentName)
        params = {'agent': agentName, 'username': player, 'token': tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证会员离线时获取会员状态:" + self.result['text'])
        self.fileoutput.info("验证会员离线时获取会员状态:" + self.result['text'])

    #会员不存在需求已更改为调用登录接口时，不存在的会员自动注册为会员
    def test_Member_NotExists(self):
        '''验证会员不存在'''
        agentName = 'GUANGXIZIZHUHUAGONG_'
        player = 'test5'
        tokenVal = encrypt_oper.sha1Encrypt(agentName)
        # 获取代理返回的安全码
        skey = encrypt_oper.getSecurityKey(agent=agentName, token=tokenVal)
        tokenVal = encrypt_oper.sha1Encrypt(skey + '|' + player + '|' + agentName)
        params = {'agent': agentName, 'username': player, 'token': tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证会员不存在:" + self.result['text'])
        self.fileoutput.info("验证会员不存在:" + self.result['text'])


    # def test_system_maintenance(self):
    #     '''验证系统维护时获取会员状态'''
    #     pass
    #
    # def test_user_locked(self):
    #     '''验证用户锁定时获取会员状态'''
    #     pass
    #
    # def test_user_locked(self):
    #     '''验证用户锁定时获取会员状态'''
    #     pass
    #
    # def test_agent_disabled(self):
    #     '''验证代理商停用时获取会员状态'''
    #     pass
    #
    # def test_whitelist_disabled(self):
    #     '''验证厅主在白名单不可用时查看会员信息'''
    #     pass

    def tearDown(self):
        print(self.result)


if __name__ == '__main__':
    unittest.main()

