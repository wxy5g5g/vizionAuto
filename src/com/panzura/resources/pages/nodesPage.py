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


class CCCNode(Page):

    def query_node(self, args):
        """return (200,allhostIP) if query successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/nodes?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        nodeList = []
        for item in response_dict['data']:
            nodeList.append(item['hostip'])
        return (response.status_code,nodeList)

    def query_nodeId(self, args):
        """retrun (200,allIdList) if query successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/nodes?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        nodeIDs = []
        for item in response_dict['data']:
            nodeIDs.append(item['id'])
        return (response.status_code,nodeIDs)

    def query_node_by_id(self, args):
        """retrun (200, hostip) if query successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/nodes/' + args['id'] + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        return (response.status_code, response_dict['data']['hostip'])

    def delete_node_by_id(self, args):
        query_url = 'https://' + args['server_ip'] + ':8443/nodes/' + args['id'] + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.delete(query_url, verify=False, timeout=60)
        return (response.status_code)

    def query_docker_by_id(self, args):
        query_url = 'https://' + args['server_ip'] + ':8443/nodes/' + args['id'] + '/dockers?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        dockerIDs = []
        for item in response_dict['data']:
            dockerIDs.append(item['subid'])
        self.logInfo("Get all dockers as following:")
        self.logInfo(dockerIDs)
        return (response.status_code, dockerIDs)


    def query_service_by_id(self, id, args):
        query_url = 'https://' + args['server_ip'] + ':8443/nodes/' + id + '/services?api_key=' + args['api_key']

        headers = {'content-type':'application/json'}
        print query_url
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)

        response_dict = response.json()
        services = {'mdnode':response_dict['mdnode'],
                    'managementdocker':response_dict['managementdocker']}
        return (response.status_code, services)
