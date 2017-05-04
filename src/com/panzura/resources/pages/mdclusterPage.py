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


class CCCMdcluster(Page):

    def query_mdcluster_node(self, args):
        query_url = 'https://' + args['server_ip'] + ':8443/mdcluster/nodes?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        mdclusters = []
        for item in response_dict['data']:
            mdclusters.append(item['id'])
        self.logInfo('ids of mdcluster are as following: ')
        self.logInfo(mdclusters)
        return (response.status_code, mdclusters)

    def query_mdcluster_node_by_id(self, args):
        """ return (0, hostip) if query mdcluster successully"""
        query_url = 'https://' + args['server_ip'] + ':8443/mdcluster/nodes/' + args['id'] + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        self.logInfo('the host ip for id ' + args['id'] + ' is: ')
        self.logInfo(response_dict['data']['hostip'])
        return(response_dict['status'], response_dict['data']['hostip'])

    def delete_mdcluster_node_by_id(self, args):
        """ retrun (0,competed) if delete done"""
        query_url = 'https://' + args['server_ip'] + ':8443/mdcluster/nodes/' + args['id'] + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.delete(query_url, verify=False, timeout=60)
        response_dict = response.json()
        return (response_dict['status'],response_dict['message'])
			
    def post_mdcluster_node_by_id(self, args):
        """ retrun (0,hostip) if post successfully"""
        insert_url = 'https://' + args['server_ip'] + ':8443/mdcluster/nodes/' + args['id'] + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.post(insert_url,  verify=False, timeout=60)
        response_dict = response.json()
        return(response_dict['status'],response_dict['data']['hostip'])
