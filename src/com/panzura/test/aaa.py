from resources.units.singletest import singletest
import unittest
from HTMLTestRunner import HTMLTestRunner
from pydoc import describe

class AAA(singletest):
    
    def pprint(self):
        self.logInfo( "set a value for father :")
        singletest.apikey = "AAAAAAAAAAA"
        self.assertTrue(False, "test Case failed")

    def testPrint(self):
        self.logInfo(singletest.apikey)
     
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AAA("pprint"))
    suite.addTest(AAA("testPrint"))
    
    fp = open('../resources/report/result.html', 'wb')
    runner = HTMLTestRunner(stream=fp,title = 'my test report',description='my Description')
    runner.run(suite)
    fp.close()