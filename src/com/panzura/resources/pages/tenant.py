#!/usr/bin/env python

import json
import requests
import os
import fnmatch
import logging
import time
import argparse
import sys
import uuid
from resources.pages.page import Page


class TenantPage(Page):

    def query_tenant(self, apikey, args):
        query_url = 'https://' + args['server_ip'] + ':8443/tenants' + '?api_key=' + str(apikey)
        headers = {'content-type':'application/json'}

        response = requests.get(query_url, verify=False, timeout=60)

        self.logInfo("Response Body is as following :")
#        self.logInfo(response.json())
        response_dict = response.json()
        tenantNames = []
        for item in response_dict['data']:           
            tenantNames.append(str(item['name']))
            
        self.logInfo(tenantNames)
        return (response.status_code,tenantNames)


    def insert_tenant(self, apikey, args):
        insert_url = 'https://' + args['server_ip'] + ':8443/tenants' + '?api_key=' + str(apikey)
        insert_tenant_json = json.dumps({'name': args['name'], 
                                         'email': args['email'],  
                                         'info': args['info'], 
                                         'password': args['password'], 
                                         'phone': args['phone'], 
                                         'policy': args['policy'], 
                                         'status': args['status'] 
                                         }) 
        
        headers = {'content-type':'application/json'}
        response = requests.post(insert_url, data=insert_tenant_json, headers=headers, verify=False, timeout=60)

        self.logInfo("Response Body is as following :")
        self.logInfo(response.json())
        queryTenantMeg = response.json()['message']
        self.logInfo("The message field in Response Body is : " + queryTenantMeg)
        
        return (response.status_code,queryTenantMeg)
    
    
    def update_tenant(self, apikey, args):
        insert_url = 'https://' + args['server_ip'] + ':8443/tenants' + '?api_key=' + str(apikey)
        insert_tenant_json = json.dumps({'name': args['name'], 
                                         'email': args['email'], 
                                         'group': [args['group']], 
                                         'info': args['info'], 
                                         'password': args['password'], 
                                         'phone': args['phone'], 
                                         'policy': args['policy'], 
                                         'status': args['status'] 
                                         }) 

        headers = {'content-type':'application/json'}

        response = requests.put(insert_url, data=insert_tenant_json, headers=headers, verify=False, timeout=60)

        self.logInfo("Response Body is as following :")
        self.logInfo(response.json())
        response_dict = response.json()
        updatedTenantMeg= response_dict['message']
        self.logInfo("The message field in Response Body is : " + updatedTenantMeg)
        
        return(response.status_code, updatedTenantMeg)
        

    def delete_tenant(self, apikey, args):
        delete_url = 'https://' + args['server_ip'] + ':8443/tenants/' + args['name'] + '?api_key=' + str(apikey)
        headers = {'content-type':'application/json'}

        response = requests.delete(delete_url, verify=False, timeout=60)

        self.logInfo("Response Body is as following :")
        self.logInfo(response.json())
        response_dict = response.json()
    
        returnStatus= response_dict['status']
        if returnStatus == 1:
            response.status_code = -1
            self.logInfo("Tenant doesn't exist for name: " + '"' + args['name'] + '"')        
        return response.status_code
