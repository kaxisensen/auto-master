import time,sys,os
sys.path.append('./interface_testcase')
sys.path.append('./common')
from HTMLTestRunner import HTMLTestRunner
import unittest


#指定测试用例为当前文件夹下的interface_testcase目录
test_dir='./interface_testcase'
discover=unittest.defaultTestLoader.discover(test_dir,pattern='*_test.py')

if __name__=="__main__":
    #now=time.strftime("%Y%m%d")
    filename='./report/'+'leboauto_test'+'_result.html'
    rootDir = os.path.dirname(os.getcwd())
    reportFile = rootDir + '/report/'+filename
    reporter = os.path.exists(reportFile)
    if reporter:
        os.remove(reportFile)
    with open(filename,'wb') as fp:
        runner = HTMLTestRunner(stream=fp, title='LEBO接口自动化测试报告', description='主要测试与会员操作相关的接口:')
        runner.run(discover)
