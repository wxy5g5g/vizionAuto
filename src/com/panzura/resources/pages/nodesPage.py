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
        query_url = 'https://' + args['server_ip'] + ':8443/nodes?api_key=' + args['api_key']

        headers = {'content-type':'application/json'}

        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        nodeList = []
        for item in response_dict:
            nodeList.append(item['hostip'])
        return (response.status_code,nodeList)

    def query_nodeId(self, args):
        query_url = 'https://' + args['server_ip'] + ':8443/nodes?api_key=' + args['api_key']

        headers = {'content-type':'application/json'}

        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        nodeIDs = []
        for item in response_dict:
            nodeIDs.append(item['id'])
        return (response.status_code,nodeIDs)

    def query_node_by_id(self, args):
        query_url = 'https://' + args['server_ip'] + ':8443/nodes/' + args['id'] + '?api_key=' + args['api_key']

        headers = {'content-type':'application/json'}

        response = requests.get(query_url, headers=headers, verify=False, timeout=60)

        response_dict = response.json()
        return (response.status_code, response_dict['hostip'])

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
        for item in response_dict:
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
        services = {'storagenode':response_dict['storagenode'],
                    'mdnode':response_dict['mdnode'],
                    'managementnode':response_dict['managementnode'],
                    'cephmonitor':response_dict['cephmonitoringnode'],
                    'cephrgwnode':response_dict['cephrgwnode']}
        return (response.status_code, services)
