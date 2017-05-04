from resources.units.singletest import singletest
import unittest
from HTMLTestRunner import HTMLTestRunner
from pydoc import describe
import json
import requests
from resources.pages.tenantPage import TenantPage
from resources.pages.groupPage import CCCGroup
from resources.pages.s3userPage import CCCS3user
from resources.pages.s3serverPage import S3Server
from resources.pages.nodesPage import CCCNode
from resources.pages.mdclusterPage import CCCMdcluster
from resources.pages.storagesPage import CCCStorages
import time
from xml.dom import minidom
from resources.units.property import Property
from email import email





class testsuite(singletest):
    accessid = ""
    secretKey = ""

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
        self.logInfo('access info :' + message[0] + message[1])
        testsuite.accessid = str(message[0])
        testsuite.secretKey = str(message[1])
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
        
        #list bucket
    def listBucket(self):
        self.logInfo("########  test cases : list bucket #########")
        serverip  = Property.getProperties("s3serverIP")
        self.logInfo("host is : " + serverip)
        args = {'server_ip': serverip,
                'accessKey': testsuite.accessid,
                'secretKey': testsuite.secretKey
                }
       
        s3s = S3Server()
        s3s.connect(args)
#        s3s.create_bucket(args)
        bucketsNames = s3s.list_bucket()
        self.logInfo(bucketsNames)
#        self.assertIn(args['bucketName'], bucketsNames, "Cannot get the bucket name in s3 server")
        
        #query all nodes out
    def queryNodes(self):
        self.logInfo("####### test Case: 005_query all nodes ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        
        np = CCCNode()
        (ok,nodelist) = np.query_node(args)
        self.logInfo(nodelist)
        self.assertEqual(ok, 200, nodelist)
        
        #query node by id
    def queryNodesById(self):
        self.logInfo("####### test Case: 006_query all nodes by ID ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        np = CCCNode()
        (ok, ids) = np.query_nodeId(args)
        idInfo = {'id': ids[2]} # try to get node3 id
        args.update(idInfo)
        (ok, hostip) = np.query_node_by_id(args)
        self.logInfo(hostip)
        self.assertEqual(ok,200, hostip)
    
        #query docker by id
    def queryDockerByid(self):
        self.logInfo("####### test Case: 007_query all dockers by ID ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        np = CCCNode()
        (ok, ids) = np.query_nodeId(args)
        idInfo = {'id': ids[0]} # try to get node1 id
        args.update(idInfo)
        (ok, dockers) = np.query_docker_by_id(args)
        self.assertEqual(ok,200, dockers)

        #query services on each node
    def queryServicesByid(self):
        self.logInfo("####### test Case: 008_query all service by ID ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        np = CCCNode()
        (ok, ids) = np.query_nodeId(args)
        idInfo = {'id1': ids[0],
                  'id2': ids[1],
                  'id3': ids[2],
                  'id4': ids[3]}
        args.update(idInfo)
        (ok, servers) = np.query_service_by_id(args['id1'], args)
        self.assertEqual(ok, 200, servers)
        self.assertEqual(servers['storagenode'], 'true', "storagenode on node1 should be true")
        self.assertEqual(servers['mdnode'], 'true', "mdnode  on node1 should be true")
        self.assertEqual(servers['managementnode'], 'true', "managementnode  on node1 should be true")
        self.assertEqual(servers['cephmonitoringnode'], 'false', "cephmonitoringnode  on node1 should be false")
        self.assertEqual(servers['cephrgwnode'], 'false', "cephrgwnode  on node1 should be false")
        
        (ok, servers) = np.query_service_by_id(args['id2'], args)
        self.assertEqual(ok, 200, servers)
        self.assertEqual(servers['storagenode'], 'true', "storagenode on node2 should be true")
        self.assertEqual(servers['mdnode'], 'true', "mdnode  on node2 should be true")
        self.assertEqual(servers['managementnode'], 'false', "managementnode  on node2 should be false")
        self.assertEqual(servers['cephmonitoringnode'], 'true', "cephmonitoringnode  on node2 should be true")
        self.assertEqual(servers['cephrgwnode'], 'false', "cephrgwnode  on node2 should be false")
               
        (ok, servers) = np.query_service_by_id(args['id3'], args)
        self.assertEqual(ok, 200, servers)
        self.assertEqual(servers['storagenode'], 'true', "storagenode on node3 should be true")
        self.assertEqual(servers['mdnode'], 'false', "mdnode  on node3 should be false")
        self.assertEqual(servers['managementnode'], 'false', "managementnode  on node3 should be false")
        self.assertEqual(servers['cephmonitoringnode'], 'false', "cephmonitoringnode  on node3 should be false")
        self.assertEqual(servers['cephrgwnode'], 'true', "cephrgwnode  on node3 should be true")
        
        (ok, servers) = np.query_service_by_id(args['id4'], args)
        self.assertEqual(ok, 200, servers)
        self.assertEqual(servers['storagenode'], 'true', "storagenode on node4 should be true")
        self.assertEqual(servers['mdnode'], 'true', "mdnode  on node4 should be true")
        self.assertEqual(servers['managementnode'], 'false', "managementnode  on node4 should be false")
        self.assertEqual(servers['cephmonitoringnode'], 'false', "cephmonitoringnode  on node4 should be false")
        self.assertEqual(servers['cephrgwnode'], 'false', "cephrgwnode  on node4 should be false")
    
        #query all mdcluster node id
    def queryMdclusterNode(self):
        self.logInfo("####### test Case: 009_query all mdcluster ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        mp = CCCMdcluster()
        (ok, nodeIds) = mp.query_mdcluster_node(args)
        self.assertEqual(ok,200, 'get nodeID failed')
        
        #query mdcluster by id
    def queryMdclusterNodeById(self):
        self.logInfo("####### test Case: 010_query mdcluster by id ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        mp = CCCMdcluster()
        (ok, nodeIds) = mp.query_mdcluster_node(args)
        nodeid = {'id': nodeIds[0]}# try to get the mdcluster by id 1
        args.update(nodeid)
        (ok, hostip) = mp.query_mdcluster_node_by_id(args)
        self.assertEqual(ok,0, hostip)
        
        #delete md by node id
    def deleteMdclusterNodeById(self):
        self.logInfo("####### test Case: 011_Delete a mdcluster by id ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        mp = CCCMdcluster()
        (ok, nodeIds) = mp.query_mdcluster_node(args)
        nodeid = {'id': nodeIds[1]}# try to get the mdcluster by id 2
        args.update(nodeid)
        (ok, message)= mp.delete_mdcluster_node_by_id(args)
        self.assertEqual(ok, 0, message)
        (ok,message) = mp.query_mdcluster_node_by_id(args)
        self.assertEqual(ok,1, "md still exists, did not be delete successfull")
    
        #create a new mdcluster by id
    def postNewMdclusterById(self):
        self.logInfo("####### test Case: 012_Create a new mdcluster by id, this case depense on 011 ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        newId = {'id':'fcb4e58c-2ee7-11e7-b106-005056ae67c7'}
        args.update(newId)
        mp = CCCMdcluster()
        (ok,hostip) = mp.post_mdcluster_node_by_id(args)
        self.assertEqual(ok,0, 'hostip is : ' + str(hostip))
        
        #querry storages
    def queryStorages(self):
        self.logInfo("####### test Case: 013_Query storages ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        sp = CCCStorages()
        (ok, idxs) = sp.query_storages(args)
        self.assertEqual(ok,0,"get all storage failed")
    
        #Create a new storage
    def createNewAndDeleteStorage(self):
        self.logInfo("####### test Case: 014_Create a new storages ### test Case: 015_Delete a new storages ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        sp = CCCStorages()
        (ok, idxs) = sp.query_storages(args)#get the count of idxs before creating new one
        storageInfo = sp.query_first_storages(args)
        storageInfo['name'] = 'new_ceph_local_' + str(time.time())
        args.update(storageInfo)
        self.logInfo( args)
        (ok,message) = sp.post_storages(args)
        self.assertEqual(ok,0,message)
        (ok, idxsNew) = sp.query_storages(args)
        if(len(idxsNew) <= len(idxs)):
            flag = False
        else: flag = True
        self.assertTrue(flag, "Cannot create new storage")
        # find the new id that just was created
        for idx in idxsNew:
            if idx not in idxs:
                newID = idx
        (ok,message) = sp.delete_storages_by_idx(newID, args) 
        self.assertEqual(ok,0, message)      
       
    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    """tenant section"""
#    suite.addTest(testsuite("newTenant"))
#    suite.addTest(testsuite("createNewGroup"))
#    suite.addTest(testsuite("createNewS3user"))
  
    suite.addTest(testsuite("queryNodes"))
    suite.addTest(testsuite("queryNodesById"))
    suite.addTest(testsuite("queryDockerByid"))
    suite.addTest(testsuite("createNewAndDeleteStorage"))
    
    fp = open('../resources/report/result.html', 'wb')
    runner = HTMLTestRunner(stream=fp,title = 'my test report',description='my Description')
    runner.run(suite)
    fp.close()