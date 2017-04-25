from resources.units.singletest import singletest
import unittest
from HTMLTestRunner import HTMLTestRunner
from pydoc import describe
import json
import requests
from resources.pages.tenantPage import TenantPage
from resources.pages.groupPage import CCCGroup
from resources.pages.s3userPage import CCCS3user
from xml.dom import minidom
from resources.units.property import Property
from email import email
from resources.pages.s3userPage import CCCS3user


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
        myTenant = Property.getProperties('testTenant')
        args = {'server_ip': serverip,
                'name': myTenant,
                'email': 'testVizion@panzura.com',
                'info': 'insertNewTenantInfo',
                'password': 'password',
                'phone': '111-123-234',
                'policy': 'testPolicy',
                'status': '0'}
        apikeyValue = singletest.apikey
        tp = TenantPage()
#        tp.delete_tenant(apikeyValue, args)
        (ok,message) = tp.insert_tenant(apikeyValue, args)
        self.assertEqual(200, ok,'Response Code is ' + str(ok))
        self.assertEqual(message.lower() , 'complete', 'Response Body : "message" is :' + message)


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
        self.assertEqual(status, 0, message)
        
        #create a new group
    def createNewGroup(self):
        serverip= Property.getProperties('serverIP')
        myTenant = Property.getProperties('testTenant')
        myGroup = Property.getProperties('testGroup')
        args = {'server_ip': serverip,
            'name': myGroup, 
            'tenant': myTenant}
        apikeyValue = singletest.apikey
        gp = CCCGroup()
        (ok, message) = gp.insert_group(apikeyValue, args)
        self.assertEqual(ok,0,message)
        
        #create a new s3 user
    def createNewS3user(self):
        serverip = Property.getProperties('serverIP')
        myTenant = Property.getProperties('testTenant')
        myGroup = Property.getProperties('testGroup')
        myUserName = Property.getProperties('tests3User')
        args = {'server_ip': serverip,
            'name': myUserName, 
            'group': myGroup, 
            'tenant':myTenant}
        apikeyValue = singletest.apikey
        s3p = CCCS3user()
        (ok, message) = s3p.insert_s3user(apikeyValue, args)
        self.assertEqual(ok,200,message)
        
        #Add access for s3 user
    def addUserAccess(self):  
        serverip = Property.getProperties("serverIP")
        myUserName = Property.getProperties('tests3User')
        args = {'server_ip': serverip,
                'name': myUserName
                }
        apikeyValue = singletest.apikey
        s3p = CCCS3user()
        (ok, message) = s3p.insert_access(apikeyValue, args)
        self.assertEqual(ok, 0, message)
        
        
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    """tenant section"""
#    suite.addTest(testsuite("newTenant"))
#    suite.addTest(testsuite("createNewGroup"))
#    suite.addTest(testsuite("createNewS3user"))
    suite.addTest(testsuite("addUserAccess"))
    
    fp = open('../resources/report/result.html', 'wb')
    runner = HTMLTestRunner(stream=fp,title = 'my test report',description='my Description')
    runner.run(suite)
    fp.close()