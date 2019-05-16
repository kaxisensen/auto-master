import os,time
import unittest
import requests
from common import encrypt_oper,log_oper


class MemberTransferStatus(unittest.TestCase):
    '''获取会员存取款状态查询'''

    def setUp(self):
        self.baseurl = encrypt_oper.getURL('interfaceurl', 'transferLog')
        #记录日志格式
        self.FILEMODE="file_record"
        self.TERMINALMODE="terminal_record"
        self.teroutput=log_oper.logrecord(self.TERMINALMODE)
        self.fileoutput=log_oper.logrecord(self.FILEMODE)

    def test_Member_deposit_status(self):
        '''验证正常获取会员存款状态'''
        status=encrypt_oper.getOrder('deposit')
        params = {'agent': status.get('agent'),'username': status.get('username'), 'token': status.get('token'),'serial':status.get('serial') }
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.FILEMODE="file_record"
        self.TERMINALMODE="terminal_record"
        self.teroutput=log_oper.logrecord(self.TERMINALMODE)
        self.fileoutput=log_oper.logrecord(self.FILEMODE)



    def test_Member_withdrawal_status(self):
        '''验证正常获取会员取款状态'''
        status=encrypt_oper.getOrder('withdrawal')
        params = {'username': status.get('username'),'agent': status.get('agent'),'serial':status.get('serial'),'token': status.get('token') }
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['text'], "Success")
        self.teroutput.info("验证正常获取会员取款状态:" + self.result['text'])
        self.fileoutput.info("验证正常获取会员取款状态:" + self.result['text'])


    def test_Member_withdrawal_notexists(self):
        '''验证输入不存在的序列号后查看取款状态'''
        #status=encrypt_oper.getOrder('withdrawal')
        #params = {'agent':status.get('agent'),'username': status.get('username'), 'token': status.get('token'),'serial':'LBC29771270951207' }
        params = {'agent':'dlebo01','username': 'tqlcr', 'token': 'd61d6ab3108f74c1716a858bafc35eb870fc8267','serial':'LC328225653476316' }
        r = requests.post(url=self.baseurl, data=params)
        self.result = r.json()
        self.assertEqual(self.result['code'], 1008)
        self.assertEqual(self.result['text'], "Serial not exist")
        self.teroutput.info("验证输入不存在的序列号后查看取款状态:" + self.result['text'])
        self.fileoutput.info("验证输入不存在的序列号后查看取款状态:" + self.result['text'])


    # def test_system_maintenance(self):
    #     '''验证系统维护时获取会员存取款状态'''
    #     pass
    #
    # def test_user_locked(self):
    #     '''验证会员处于停用或冻结状态时查看取款状态'''
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
    #     '''验证白名单中厅主处于不可用状态时查看取款状态'''
    #     pass

    def tearDown(self):
        print(self.result)


if __name__ == '__main__':
    unittest.main()

