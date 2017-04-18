import logging
import unittest
from resources.tenant_api import CCCTenant
import json
import requests
from resources.pages.page import Page


class LoginPage(Page):
    
    def login(self):
        
        user = 'root'
        passwd = 'password'
        serverIp = '10.180.108.11'
        login_json = json.dumps({'username': user, 
                                 'password': passwd 
                                })
        insert_url = 'https://' + serverIp + ':8443/auth/login'
        headers = {'content-type':'application/json'}
        response = requests.put(insert_url, data=login_json, headers=headers, verify=False, timeout=60)
        
        
        
        login_json = json.dumps({'username': user, 
                                 'password': passwd 
                                })
        insert_url = 'https://' + serverIp + ':8443/auth/login'
        headers = {'content-type':'application/json'}
        response = requests.put(insert_url, data=login_json, headers=headers, verify=False, timeout=60)
        
        
        
        
        self.logInfo(user + "  " + passwd + '  ' + serverIp)
        self.logInfo(response.status_code)
        self.logInfo(response.json())
        apikey = response.json()['data']['apikey']
        return (response.status_code, apikey)
    
    
    def logout(self):
        self.logInfo("Need more steps here")
        