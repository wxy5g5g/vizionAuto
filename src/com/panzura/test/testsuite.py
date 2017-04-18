from resources.units.singletest import singletest
import unittest
from HTMLTestRunner import HTMLTestRunner
from pydoc import describe
import json
import requests
from resources.pages.tenant import TenantPage


class testsuite(singletest):
    

    def testPrint(self):
        self.logInfo(singletest.apikey)
     
     
    def newTenant(self):
        args = {'server_ip': '10.180.108.11',
                'name': 'tenant_1234567',
                'email': 'testVizion@panzura.com',
                'info': 'insertNewTenantInfo',
                'password': 'password',
                'phone': '111-123-234',
                'policy': 'testPolicy',
                'status': '0'}
        apikeyValue = singletest.apikey
        tp = TenantPage()
        (ok,message) = tp.insert_tenant(apikeyValue, args)
        self.assertEqual(200, ok,'Response Code is ' + str(ok))
        self.assertEqual(message.lower() , 'complete', 'Response Body : "message" is :' + message)
        


     
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(testsuite("newTenant"))
    suite.addTest(testsuite("testPrint"))
    
    fp = open('../resources/report/result.html', 'wb')
    runner = HTMLTestRunner(stream=fp,title = 'my test report',description='my Description')
    runner.run(suite)
    fp.close()