import unittest
import time
from HTMLTestRunner import HTMLTestRunner


test_dir = './'
pattern = 'test*.py'
discover = unittest.defaultTestLoader.discover(test_dir, pattern)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    fileName = "../resources/report/" + now + '_VizionTestResult.html'
    fp = open(fileName, 'wb')
    runner = HTMLTestRunner(stream=fp,title = 'Vizion rest API test report at ' + now,description='sanity test')
    runner.run(discover)
    fp.close()