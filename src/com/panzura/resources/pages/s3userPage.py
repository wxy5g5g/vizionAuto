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

class CCCS3user(Page):

    def query_s3user(self, apikey, args):
        query_url = 'https://' + args['server_ip'] + ':8443/s3users/' + args['name'] + '?api_key=' + str(apikey)
        headers = {'content-type':'application/json'}

        response = requests.get(query_url, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()

        print response_dict['name']



    def insert_s3user(self, args):
        """ will return (200, "complete") if insert new s3 user successfully"""
        insert_url = 'https://' + args['server_ip'] + ':8443/s3users' + '?api_key=' + str(args['apikey'])
        insert_s3user_json = json.dumps({'name': args['name'], 
                                         'group': [args['group']], 
                                         'info': 'info', 
                                         'password': "testpassword", 
                                         'tenant':args['tenant']
                                         }) 

        headers = {'content-type':'application/json'}
        self.logInfo("The url is : " + insert_url)
        response = requests.post(insert_url, data=insert_s3user_json, headers=headers, verify=False, timeout=60)

        response_dict = response.json()
        accessInfo = [response_dict['data']['access']['id'],response_dict['data']['access']['secret']]
        self.logInfo("access id is :" + accessInfo[0])
        self.logInfo("access secret is :" + accessInfo[1])
        return(response.status_code, accessInfo)
    

    def insert_access(self, args):
        """ will return (0, "complete") if add access successfully"""
        insert_url = 'https://' + args['server_ip'] + ':8443/s3users/' + args['name'] + '/s3access' + '?api_key=' + str(args['apikey']) 
        self.logInfo("The url is : " + insert_url)
        headers = {'content-type':'application/json'}
        response = requests.put(insert_url, headers=headers, verify=False, timeout=60)
        self.logInfo(response.json)
        response_dict = response.json()
        return(response_dict['status'],response_dict['message'])


    def delete_s3user(self, args):
        """  Will return (0, "complete") if delete successfully """
        delete_url = 'https://' + args['server_ip'] + ':8443/s3users/' + args['name'] + '?api_key=' + str(args['apikey'])
        self.logInfo("The url is : " + delete_url)
        headers = {'Accept':'application/json'}
        response = requests.delete(delete_url, headers=headers, verify=False, timeout=60)

        response_dict = response.json()
        return (response_dict['status'], response_dict['message'])
