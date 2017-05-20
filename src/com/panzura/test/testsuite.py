from resources.units.singletest import singletest
import unittest
from HTMLTestRunner import HTMLTestRunner
import xmlrunner
from pydoc import describe
import json
import requests
from resources.pages.tenantPage import TenantPage
from resources.pages.groupPage import CCCGroup
from resources.pages.s3userPage import CCCS3user
#from resources.pages.s3Page import S3Server
from resources.pages.nodesPage import CCCNode
from resources.pages.mdclusterPage import CCCMdcluster
from resources.pages.storagesPage import CCCStorages
from resources.pages.s3servicesPage import CCCS3services
import time
from xml.dom import minidom
from resources.units.property import Property
from email import email
from boto.dynamodb.condition import NULL
from resources.pages import groupPage





class testsuite(singletest):
    accessid = ""
    secretKey = ""
    
    def setUp(self):
        self.log(4*'\n')
        
    #test case-001: create a new tenant
    def newTenant(self):
        self.log("####### test Case: 004_create a new tenant ######")
        serverip = Property.getProperties('serverIP')
        myTenant = Property.getProperties('testTenant')
        myGroup = Property.getProperties('testGroup')
        gp = CCCGroup()
        arg = {'server_ip': serverip,
            'name': myGroup, 
            'tenant': myTenant}
        apikeyValue = singletest.apikey
        (ok, message) = gp.delete_group(apikeyValue, arg)
        arg['name'] = 'default'
        (ok, message) = gp.delete_group(apikeyValue, arg)# delete group named 'default'
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
        tp.delete_tenant(apikeyValue, args)
        (ok,message) = tp.insert_tenant(apikeyValue, args)
        self.assertEqual(200, ok,'Response Code is ' + str(ok))
        self.assertEqual(message.lower() , myTenant, 'Response Body : "message" is :' + message)
        tp.delete_tenant(apikeyValue, args)


    #test case-002: search a tenant 
    def getTenant(self):
        self.log("####### test Case: 022_search a tenant ######")
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
        self.log("####### test Case: 000_modify a tenant ######")
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
        self.log("####### test Case: 001_delete a tenant ######")
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
        self.log("####### test Case: 002_create a new group ######")
        serverip= Property.getProperties('serverIP')
        myTenant = Property.getProperties('testTenant')
        myGroup = Property.getProperties('testGroup')
        args = {'server_ip': serverip,
                'name': myTenant,
                'email': 'testVizion@panzura.com',
                'info': 'insertNewTenantInfo',
                'password': 'password',
                'phone': '111-123-234',
                'policy': 'testPolicy',
                'status': '0',
                'tenant': myTenant}
        apikeyValue = singletest.apikey
        tp = TenantPage()
        (status, message) = tp.delete_tenant(apikeyValue, args)
        (ok,message) = tp.insert_tenant(apikeyValue, args)
        gp = CCCGroup()
        args['name'] = myGroup
        gp.delete_group(apikeyValue, args)
        (ok, message) = gp.insert_group(apikeyValue, args)
        self.assertEqual(ok,0,message)
        
        #create a new s3 user
    def createNewS3user(self):
        self.log("####### test Case: 003_create a new s3 user ######")
        serverip = Property.getProperties('serverIP')
        myTenant = Property.getProperties('testTenant')
        myGroup = Property.getProperties('testGroup')
        myUserName = Property.getProperties('tests3User')
        args = {'server_ip': serverip,
            'name': myUserName, 
            'group': myGroup, 
            'tenant':myTenant,
            'apikey': singletest.apikey}
        s3p = CCCS3user()
        s3p.delete_s3user(args)
        (ok, message) = s3p.insert_s3user(args)
        self.logInfo('access info :' + message[0] + message[1])
        testsuite.accessid = str(message[0])
        testsuite.secretKey = str(message[1])
        try:
            self.assertEqual(ok,200,message)
        finally:
            s3p.delete_s3user(args)
        
        #query all nodes out
    def queryNodes(self):
        self.log("####### test Case: 005_query all nodes ######")
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
        self.log("####### test Case: 006_query node by ID ######")
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
        self.log("####### test Case: 007_query all dockers by ID ######")
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
        self.log("####### test Case: 008_query all service by ID ######")
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
        self.assertTrue(servers['mdnode'], "mdnode  on node1 should be true" )
        self.assertTrue(servers['managementdocker'], "managementnode  on node1 should be true")
        
        (ok, servers) = np.query_service_by_id(args['id2'], args)
        self.assertEqual(ok, 200, servers)
        self.assertTrue(servers['mdnode'], "mdnode  on node2 should be true" )
        self.assertFalse(servers['managementdocker'], "managementnode  on node2 should be false")
               
        (ok, servers) = np.query_service_by_id(args['id3'], args)
        self.assertEqual(ok, 200, servers)
        self.assertFalse(servers['mdnode'], "mdnode  on node3 should be false")
        self.assertFalse(servers['managementdocker'], "managementnode  on node3 should be false")
        
        (ok, servers) = np.query_service_by_id(args['id4'], args)
        self.assertEqual(ok, 200, servers)
        self.assertTrue(servers['mdnode'], "mdnode  on node4 should be true")
        self.assertFalse(servers['managementdocker'], "managementnode  on node4 should be false")

        #query all mdcluster node id
    def queryMdclusterNode(self):
        self.log("####### test Case: 009_query all mdcluster ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        mp = CCCMdcluster()
        (ok, nodeIds) = mp.query_mdcluster_node(args)
        self.assertEqual(ok,200, 'get nodeID failed')
        
        #query mdcluster by id
    def queryMdclusterNodeById(self):
        self.log("####### test Case: 010_query mdcluster by id ######")
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
        self.log("####### test Case: 011_Delete a mdcluster by id ######")
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
        self.assertEqual(ok,0, "md still exists, did not be delete successfull")
    
        #create a new mdcluster by id
    def postNewMdclusterById(self):
        self.log("####### test Case: 012_Create a new mdcluster by id, this case depense on 011 ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        np = CCCNode()
        (ok, ids) = np.query_nodeId(args)
        newId = {'id':ids[-1]}# the the last node to post new mdcluster
        args.update(newId)
        mp = CCCMdcluster()
        (ok,hostip) = mp.post_mdcluster_node_by_id(args)
        self.assertEqual(ok,0, 'hostip is : ' + str(hostip))
        
        #querry storages
    def queryStorages(self):
        self.log("####### test Case: 013_Query storages ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        sp = CCCStorages()
        (ok, idxs) = sp.query_storages(args)
        self.assertEqual(ok,0,"get all storage failed")
    
        #Create a new storage
    def createNewAndDeleteStorage(self):
        self.log("####### test Case: 014_Create a new storages ### test Case: 015_Delete a new storages ######")
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
        self.assertTrue(len(idxsNew) > len(idxs), "Cannot create new storage successfully")
        # find the new id that just was created, then try to delete it
        for idx in idxsNew:
            if idx not in idxs:
                newID = idx
        (ok,message) = sp.delete_storages_by_idx(newID, args) 
        self.assertEqual(ok,0, message)      
       
        #query all s3 services
    def queryS3services(self):
        self.log("####### test Case: 016_Query all s3 services ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key':apikeyValue}
        s3sP = CCCS3services()
        (ok, services) = s3sP.query_s3services(args)
        self.assertEqual(ok, 200, " query all services failed!")
    
        #Create a new S3 service
    def createNewService(self):
        self.log("####### test Case: 017_Create a new s3 services ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key': apikeyValue,
                'ip': '10.180.108.1'}    
        np = CCCNode()
        (ok,ids) = np.query_nodeId(args)
        nodeid = {'id': ids[3]}#select node4 and try to start s3 on it
        args.update(nodeid)
        s3sp = CCCS3services()
        (ok,message) = s3sp.post_s3services_by_id_ip(args)
        self.assertEqual(ok, 0, message)
        self.logInfo("Sleep 5 seconds to wait new service added")
        time.sleep(5)
        (ok,hostsIp) = s3sp.query_s3servicesHostIp(args)
        self.assertTrue([args['ip']] in hostsIp, "Cannot find the host ip which just created, post action failed.")
        
        #delete a new S3 service
    def deleteServiceByIdSubid(self):
        self.log("####### test Case: 018_Delete a new s3 services ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key': apikeyValue,
                'ip': '10.180.108.2'}    
        np = CCCNode()
        (ok,ids) = np.query_nodeId(args)
        nodeid = {'id': ids[3]}#select node4 and try to start s3 on it
        args.update(nodeid)
        s3sp = CCCS3services()
        (ok,message) = s3sp.post_s3services_by_id_ip(args)
        self.assertEqual(ok, 0, message)
        (ok,ids) = s3sp.query_s3services(args)
        self.assertEqual(ok,200, "get ids base on hostip failed.")
        idAndSubid = {'id': ids[-1]['sid'],
                      'subid': ids[-1]['ssubid']}
        args.update(idAndSubid)
        (ok, message) = s3sp.delete_s3services_by_id_subid(args)
        self.assertEqual(ok, 0, message)
         
        #query s3services by id subid
    def queryS3servicesByIdSubid(self):
        self.log("####### test Case: 019_Create a new s3 services ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key': apikeyValue}   
            
        s3sp = CCCS3services()
        (ok, services) = s3sp.query_s3services(args)
        serviceids = {'id': services[0]['sid'],#select the first service to do query
                  'subid': services[0]['ssubid']} 
        args.update(serviceids)
        (ok, hostip) =  s3sp.query_s3services_by_id_subid(args)
        self.logInfo(hostip)
        self.assertTrue('null'!=str(hostip).lower(), "Query service by 'id ' and 'subid' failed")
        
        #start s3services by id subid
    def startS3servicesByIdSubid(self):
        self.log("####### test Case: 020_Start a new s3 services ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key': apikeyValue}   
            
        s3sp = CCCS3services()
        (ok, services) = s3sp.query_s3services(args)
        serviceids = {'id': services[0]['sid'],#select the first service to do start
                  'subid': services[0]['ssubid']} 
        args.update(serviceids)
        (ok, message) =  s3sp.start_s3services_by_id_subid(args)
        self.assertEqual(ok, 200, message)    
        
        #stop s3services by id subid
    def stopS3servicesByIdSubid(self):
        self.log("####### test Case: 021_Stop a new s3 services ######")
        cccServerIP = Property.getProperties('serverIP')
        apikeyValue = singletest.apikey
        args = {'server_ip': cccServerIP,
                'api_key': apikeyValue}   
            
        s3sp = CCCS3services()
        (ok, services) = s3sp.query_s3services(args)
        serviceids = {'id': services[0]['sid'],#select the first service to do stop
                  'subid': services[0]['ssubid']} 
        args.update(serviceids)
        (ok, message) =  s3sp.stop_s3services_by_id_subid(args)
        self.assertEqual(ok, 200, message)       
       
       

        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    """suite section"""

    suite.addTest(testsuite("newTenant"))
    suite.addTest(testsuite("getTenant"))
    suite.addTest(testsuite("editTenant"))
#    suite.addTest(testsuite("deleteTenant"))
    suite.addTest(testsuite("createNewGroup"))
    suite.addTest(testsuite("createNewS3user"))
    suite.addTest(testsuite("queryNodes"))
    suite.addTest(testsuite("queryNodesById"))
    suite.addTest(testsuite("queryDockerByid"))
    suite.addTest(testsuite("queryServicesByid"))
    suite.addTest(testsuite("queryMdclusterNode"))
    suite.addTest(testsuite("queryMdclusterNodeById"))
#    suite.addTest(testsuite("deleteMdclusterNodeById"))
    suite.addTest(testsuite("postNewMdclusterById"))
    suite.addTest(testsuite("queryStorages"))
    suite.addTest(testsuite("createNewAndDeleteStorage"))
    suite.addTest(testsuite("queryS3services"))
    suite.addTest(testsuite("createNewService"))
    suite.addTest(testsuite("deleteServiceByIdSubid"))
    suite.addTest(testsuite("queryS3servicesByIdSubid"))
    suite.addTest(testsuite("startS3servicesByIdSubid"))
    suite.addTest(testsuite("stopS3servicesByIdSubid"))

    now = time.strftime("%Y-%m-%d %H_%M_%S")
#    fileName = "../resources/report/" + now + '_VizionTestResult.html'
#    fileName = "/opt/workspace/ccc_api_test/src/com/panzura/resources/report/" + now + '_VizionTestResult.html'
    fileName = "/opt/workspace/CCC_api_test_demo/src/com/panzura/resources/report/"
    
#    fp = open(fileName, 'wb')
    runner = HTMLTestRunner(stream=fileName,title = 'Vizion rest API test report at ' + now,description='sanity test')
    runner = xmlrunner.XMLTestRunner(output=fileName )
    runner.run(suite)
#    fp.close()