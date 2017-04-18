import logging
import unittest
from resources.tenant_api import CCCTenant
import json
import requests


logging.basicConfig()
log = logging.getLogger()
log.setLevel('INFO')


class CCC(unittest.TestCase):

    apikey = None
 
    def testLogin(self):
        user = 'root'
        passwd = 'password'
        serverIp = '10.180.108.11'
        login_json = json.dumps({'username': user, 
                                 'password': passwd 
                                })
        insert_url = 'https://' + serverIp + ':8443/auth/login'
        headers = {'content-type':'application/json'}
        response = requests.put(insert_url, data=login_json, headers=headers, verify=False, timeout=60)
        log.info(response.status_code)
        self.assertEqual(200, response.status_code)
        CCC.apikey = response.json()['data']['apikey']
        log.info('Apikey is : ' + response.json()['data']['apikey'])
 
 
    def testAAA(self):
        args = {'server_ip': '10.180.108.11',
                'name': 'tenant_002',
                'email': 'testVizion@panzura.com',
                'info': 'insertNewTenantInfo',
                'password': 'password',
                'phone': '111-123-234',
                'policy': 'testPolicy',
                'status': '0'}
        log.info("fields is :  " + args['name'])
        
        insert_tenant_json = json.dumps({'name': args['name'], 
                                         'email': args['email'], 
                                         'info': args['info'], 
                                         'password': args['password'], 
                                         'phone': args['phone'],  
                                         'status': args['status']
                                         })
        insert_url = 'https://' + args['server_ip'] + ':8443/tenants?api_key=' + str(CCC.apikey)
        log.info(insert_url)
        headers = {'content-type':'application/json'}
        response = requests.post(insert_url, data=insert_tenant_json, headers=headers, verify=False, timeout=60)

#        print response.json()
        log.info(response)

        log.info(insert_tenant_json)
        log.info(response.status_code)
        self.assertEqual(response.status_code,200)
#        if response.status_code != 200:
#            print response.json()
#            return 1

        response_dict = response.json()
        print response_dict['status']

    def testCreateTenant(self):
        ccc_node = '10.180.108.11'
        testTenant = CCCTenant()
        args = {'server_ip': ccc_node,
                'name': 'tenant_002',
                'email': 'testVizion@panzura.com',
                'info': 'insertNewTenantInfo',
                'password': 'password',
                'phone': '111-123-234',
                'policy': 'testPolicy',
                'status': '0'}

        log.info("Try to insert a tenant to table")
        try:
            testTenant.insert_tenant(args)
        except Exception, e:
            log.info('receive error: ' + str(e))


if __name__ == "__main__":
    suite =unittest.TestSuite()
    suite.addTest(CCC("testLogin"))
    suite.addTest(CCC("testAAA"))
#    suite.addTest(CCC("testCreateTenant"))
    runner = unittest.TextTestRunner()
    runner.run(suite)