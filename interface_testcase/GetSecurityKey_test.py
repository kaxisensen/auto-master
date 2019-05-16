

import os,time
import unittest
import requests
import logging
from common import encrypt_oper, csv_oper,log_oper
class GetSecuryitKey(unittest.TestCase):
    '''获取securityKey'''

    def setUp(self):
        self.baseurl = encrypt_oper.getURL('interfaceurl', 'getkey')
        self.agentName = csv_oper.csvRead().get("agent")
        self.tokenVal = encrypt_oper.sha1Encrypt(self.agentName)
        #记录日志格式
        self.FILEMODE="file_record"
        self.TERMINALMODE="terminal_record"
        self.teroutput=log_oper.logrecord(self.TERMINALMODE)
        self.fileoutput=log_oper.logrecord(self.FILEMODE)

    def test_getSecurityKey(self):
        '''验证输入已存在的代理商时，调用接口获取正确的Key'''
        agentName = self.agentName
        token = self.tokenVal
        params = {'agent': self.agentName, 'token': self.tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证输入已存在的代理商时，调用接口获取正确的Key:" + self.result['text'])
        self.fileoutput.info("验证输入已存在的代理商时，调用接口获取正确的Key:" + self.result['text'])

    def test_non_existent_agent(self):
        '''验证输入不存在的代理商时调用接口'''
        agentName = "aabccdfdfsffssf"
        tokenVal = encrypt_oper.sha1Encrypt(agentName)
        params = {'agent': agentName, 'token': tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9004)
        self.assertEqual(self.result['text'], 'Invalid Agent')
        self.teroutput.info("验证输入不存在的代理商时调用接口:" + self.result['text'])
        self.fileoutput.info("验证输入不存在的代理商时调用接口:" + self.result['text'])

    def test_not_input_token(self):
        '''验证不输入token时调用接口调用接口'''
        agentName = self.agentName
        params = {'agent': agentName}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], 'Invalid arguments')
        self.teroutput.info("验证不输入token时调用接口调用接口:" + self.result['text'])
        self.fileoutput.info("验证不输入token时调用接口调用接口:" + self.result['text'])


    def test_not_input_agent(self):
        '''验证不输入代理时调用接口'''
        tokenVal = self.tokenVal
        params = {'token': tokenVal}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("验证不输入代理时调用接口:" + self.result['text'])
        self.fileoutput.info("验证不输入代理时调用接口:" + self.result['text'])


    def test_not_input_agentandtoken(self):
        '''不输入代理商和token时调用接口'''
        params = {'agent': '', 'token': ''}
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 9002)
        self.assertEqual(self.result['text'], "Invalid arguments")
        self.teroutput.info("不输入代理商和token时调用接口:" + self.result['text'])
        self.fileoutput.info("不输入代理商和token时调用接口:" + self.result['text'])


    # def test_system_maintenance(self):
    #     '''系统维护时调用securityKey'''
    #     pass
    #
    # def test_disable_agent(self):
    #     '''停用代理时调用securityKey'''
    #     pass
    #
    # def test_disable_white_list(self):
    #     '''停用代理的厅主白名单时调用securityKey'''
    #     pass

    def tearDown(self):
        print(self.result)


if __name__ == '__main__':
    unittest.main()




