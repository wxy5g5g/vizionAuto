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
from imaplib import Response_code


class CCCS3services(Page):

    def query_s3services(self, args):
        """ Return (200,servicesList) if query successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/s3services?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        serviceList = []# this is a 'id' and 'subid' list
        for item in response_dict:
            service={'sid': item['id'],
                    'ssubid': item['subid']}
            serviceList.append(service)
        self.logInfo('Total has ' + str(len(serviceList)) + ', all services are :')
        self.logInfo(serviceList)
        return(response.status_code, serviceList)
    
    def query_s3servicesIdByHostIp(self, args):
        """ Return (200,[id,subid]) if query successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/s3services?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        idList = []# this is all 'id' list
        hostDict = {}
        count = -1
        for item in response_dict: #get the id and subid base on the hostip
            self.logInfo(item['hostip'])
            self.logInfo(args['ip'])
            count +=1
            if args['ip']==str(item['hostip']):
                self.logInfo('$$$$$$$$$$$$$$$$$$$$$$$$$')
                break
        hostDict = item[count]
        self.logInfo(hostDict)
        idList.append(hostDict['id'])
        idList.append(hostDict['subid'])
        self.logInfo('id and subid  for host ip ' + str(args['ip']) + ' are :')
        self.logInfo(idList)
        return(response.status_code, idList)
    
    def query_s3servicesHostIp(self, args):
        """ Return (200,hostList) if query successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/s3services?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        hostList = []# this is a 'hostip' list
        for item in response_dict:
            service=item['hostip']
            hostList.append(service)
        self.logInfo('Total has ' + str(len(hostList)) + ', all host ip are :')
        self.logInfo(hostList)
        return(response.status_code, hostList)

    def query_s3services_by_id_subid(self, args):
        """ return (200,hostip) if query successfully """
        query_url = 'https://' + args['server_ip'] + ':8443/s3services/' + args['id'] + '/' +  args['subid'] + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.get(query_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        return(response.status_code,response_dict['hostip'])

    def delete_s3services_by_id_subid(self, args):
        """ return (0, complete) if delete successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/s3services/' + args['id'] + '/' +  args['subid'] + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.delete(query_url, verify=False, timeout=60)
        response_dict = response.json()
        return(response_dict['status'], response_dict['message'])
			
    def post_s3services_by_id_ip(self, args):
        """return (0,complete) if post successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/s3services/' + args['id'] + '/' +  args['ip']  + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.post(query_url, verify=False, timeout=60)
        response_dict = response.json()
        return(response_dict['status'], response_dict['message'])

    def start_s3services_by_id_subid(self, args):
        """return (0,complete) if start successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/s3services/' + args['id'] + '/' +  args['subid']  + '/start?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.put(query_url, verify=False, timeout=60)
        response_dict = response.json()
        return(response.status_code, response_dict['message'])

    def stop_s3services_by_id_subid(self, args):
        """return (0,complete) if stop successfully"""
        query_url = 'https://' + args['server_ip'] + ':8443/s3services/' + args['id'] + '/' +  args['subid']  + '/stop?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.put(query_url, verify=False, timeout=60)
        response_dict = response.json()
        return(response.status_code, response_dict['message'])

    def failover_s3services_by_id_subid_newid(self, args):
        query_url = 'https://' + args['server_ip'] + ':8443/s3services/' + args['id'] + '/' +  args['subid']  + '/failover/'+ args['newid'] + '?api_key=' + args['api_key']
        headers = {'content-type':'application/json'}
        response = requests.put(query_url, verify=False, timeout=60)
        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1
        response_dict = response.json()
        print response_dict['status']
