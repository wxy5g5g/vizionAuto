from resources.units.singletest import singletest
import unittest
from HTMLTestRunner import HTMLTestRunner
from pydoc import describe
import json
import requests
from resources.pages.tenant import TenantPage
from xml.dom import minidom
from resources.units.property import Property
from email import email


class testsuite(singletest):
    

    def testPrint(self):
        
     cccXmlPath = "../resources/properties/ccc.xml"
     dom = minidom.parse(cccXmlPath)
     root = dom.documentElement
     ccc = dom.getElementsByTagName('serverIP')
     serverip = ccc[0].firstChild.data
     self.logInfo(serverip)
     
    #test case-001: create a new tenant
    def newTenant(self):
        serverip = Property.getProperties('serverIP')
        args = {'server_ip': serverip,
                'name': 'tenant_001',
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
        tp.delete_tenant(apikeyValue, args)

    #test case-002: search a tenant 
    def getTenant(self):
        serverip = Property.getProperties('serverIP')
        args = {'server_ip': serverip,
                'name': 'tenant_002',
                'email': 'testVizion@panzura.com',
                'info': 'insertNewTenantInfo',
                'password': 'password',
                'phone': '111-123-234',
                'policy': 'testPolicy',
                'status': '0'}
        apikeyValue = singletest.apikey
        tp = TenantPage()
        (ok,message) = tp.insert_tenant(apikeyValue, args)
        self.assertEqual(ok,200, 'create new tenant failed, return code is : "' + str(ok) + '"')
        (ok,names) = tp.query_tenant(apikeyValue, args)
        self.assertIn(args['name'], names,'query tenant failed,the name you would like to query does not exist.')
        tp.delete_tenant(apikeyValue, args)
        
        
        #test case-003: modify a tenant 
    def editTenant(self):
        serverip = Property.getProperties('serverIP')
        args = {'server_ip': serverip,
                'name': 'tenant_003',
                'email': 'testVizion@panzura.com',
                'info': 'insertNewTenantInfo',
                'password': 'password',
                'phone': '111-123-234',
                'policy': 'testPolicy',
                'status': '0'}
        newPasswd = 'newPassword002'
        newPhone = '111-123.002'
        newEmail = 'test002@panzura.com'
        apikeyValue = singletest.apikey
        tp = TenantPage()
        tp.delete_tenant(apikeyValue, args)
        (ok,message) = tp.insert_tenant(apikeyValue, args)
        self.assertEqual(ok,200, 'create new tenant failed, return code is : "' + str(ok) + '"')
        args['password'] = newPasswd
        args['phone'] = newPhone
        args['email'] = newEmail
        (ok,message) = tp.update_tenant(apikeyValue, args)
        self.assertEqual(ok, 200,'update tenant failed,the reason is: ' + str(message))
        tp.delete_tenant(apikeyValue, args)
        
        #delete a tenant
    def deleteTenant(self):
        serverip = Property.getProperties('serverIP')
        args = {'server_ip': serverip,
            'name': 'tenant_004',
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
        (status, message) = tp.delete_tenant(apikeyValue, args)
        self.assertEqual(status, 1, message)
        
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(testsuite("newTenant"))
    suite.addTest(testsuite("getTenant"))
    suite.addTest(testsuite("editTenant"))
    suite.addTest(testsuite("deleteTenant"))
    
    fp = open('../resources/report/result.html', 'wb')
    runner = HTMLTestRunner(stream=fp,title = 'my test report',description='my Description')
    runner.run(suite)
    fp.close()