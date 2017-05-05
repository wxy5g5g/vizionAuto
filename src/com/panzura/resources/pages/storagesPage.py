#!/usr/bin/env python
##############################################################################
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


class CCCStorages(Page):

    def query_storages(self, args):
        query_url = 'https://' + args['server_ip'] + ':8443/storages?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        idxs = []
        for item in response_dict['data']:
            idxs.append(item['idx'])
        self.logInfo("Total has stroage is : " + str(len(idxs)))
        return(response_dict['status'], idxs)
    
    def query_first_storages(self, args):
        query_url = 'https://' + args['server_ip'] + ':8443/storages?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        storageInfo = {'idx':response_dict['data'][0]['idx'],
                       'type':response_dict['data'][0]['connectiontype'],
                       'hostip':response_dict['data'][0]['host'],
                       'name':response_dict['data'][0]['name'],
                       'secret':response_dict['data'][0]['password'],
                       'port':response_dict['data'][0]['port'],
                       'status':response_dict['data'][0]['status'],
                       'storagetype':response_dict['data'][0]['storagetype'],
                       'target':response_dict['data'][0]['target'],
                       'access':response_dict['data'][0]['user'],
                       'vendortype':response_dict['data'][0]['vendortype']}
        self.logInfo(storageInfo)
        return(storageInfo)

    def post_storages(self, args):
        """ return (0,complete) if post successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/storages/' + '?api_key=' + args['api_key']
        insert_storage_json = json.dumps({"connectiontype": "HTTP",
                                          "host": args['hostip'],       
                                          "name":args['name'],                    
                                          "passwd": args['secret'],
                                          "port": args['port'],
                                          "storagetype": 'SSD',
                                          "target": args['target'],
                                          "user": args['access'],
                                          "vendortype": 'CEPH_RGW',
                                          "info": "a new storage",
                                          "status": 0
                                       })
        self.logInfo(insert_storage_json)
        headers = {'content-type':'application/json'}
        response = requests.post(query_url, data=insert_storage_json, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        return (response_dict['status'],response_dict['message'])

    def delete_storages_by_idx(self, idx , args):
        """ retrun (0,complete) if delete successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/storages/' + str(idx) + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.delete(query_url, verify=False, timeout=60)
        response_dict = response.json()
        return(response_dict['status'], response_dict['message'])
