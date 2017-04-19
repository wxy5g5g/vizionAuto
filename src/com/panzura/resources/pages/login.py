import logging
import unittest
import json
import requests
from resources.pages.page import Page
import exceptions
from resources.units.property import Property



class LoginPage(Page):
    
    def login(self):
        
        user = Property.getProperties('loginUser')
        passwd = Property.getProperties('loginPasswd')
        serverIp = Property.getProperties('serverIP')
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
        
        self.logInfo(response.status_code)
        apikey = response.json()['data']['apikey']
        self.logInfo("*****apikey***** for login is : " + apikey)
        return (response.status_code, apikey)
    
    
    def logout(self):
        self.logInfo("Need more steps here")
        