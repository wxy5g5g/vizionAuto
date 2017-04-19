from resources.units.singletest import singletest
import unittest
from HTMLTestRunner import HTMLTestRunner
from pydoc import describe
import json
import requests
from resources.pages.tenant import TenantPage
from xml.dom import minidom
from resources.units.property import Property


class testsuite(singletest):
    

    def testPrint(self):
        
     cccXmlPath = "../resources/properties/ccc.xml"
     dom = minidom.parse(cccXmlPath)
     root = dom.documentElement
     ccc = dom.getElementsByTagName('serverIP')
     serverip = ccc[0].firstChild.data
     self.logInfo(serverip)
     
    def newTenant(self):
        serverip = Property.getProperties('serverIP')
        args = {'server_ip': serverip,
                'name': 'tenant_AAATTT',
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
#    suite.addTest(testsuite("testPrint"))
    
    fp = open('../resources/report/result.html', 'wb')
    runner = HTMLTestRunner(stream=fp,title = 'my test report',description='my Description')
    runner.run(suite)
    fp.close()