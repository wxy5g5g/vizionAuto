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


class CCCGroup(Page):

    def query_group(self, apikey, args):
        """ Need modify """
        query_url = 'https://' + args['server_ip'] + ':8443/groups/' + args['tenant'] + '?api_key=' + str(apikey)
        headers = {'content-type':'application/json'}

        response = requests.get(query_url, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()

        print response_dict['name']
        for item in response_dict['group']:
            print item



    def insert_group(self, apikey, args):
        """ return (0, "complete") if insert group successfully""" 
        insert_url = 'https://' + args['server_ip'] + ':8443/groups' + '?api_key=' + str(apikey)
        insert_group_json = json.dumps({'name': args['name'], 
                                         'tenant': args['tenant'], 
                                         'info': args['info'], 
                                         'policy' : {
                                                     'policies': [
                                                                   {
                                                                   'type': 0,
                                                                   'tenant': 'string',
                                                                   'name': 'string'
                                                                   }
                                                                 ]
                                                     }
                                        }) 

        headers = {'content-type':'application/json'}

        response = requests.post(insert_url, data=insert_group_json, headers=headers, verify=False, timeout=60)

        response_dict = response.json()
        return (response_dict['status'],response_dict['message'])


    def update_group(self, apikey, args):
        insert_url = 'https://' + args['server_ip'] + ':8443/groups' + '?api_key=' + str(apikey)
        insert_group_json = json.dumps({'name': args['name'], 
                                         'tenant': args['tenant'], 
                                         'info': args['info'], 
                                         'policy': args['policy'] 
                                         }) 

        headers = {'content-type':'application/json'}

        response = requests.put(insert_url, data=insert_group_json, headers=headers, verify=False, timeout=60)

        print response.json()
        if response.status_code != 200:
            print response.json()
            return 1

        response_dict = response.json()
        print response_dict['status']

    def delete_group(self, apikey, args):
        """  Will return (0, "complete") if delete successfully """
        delete_url = 'https://' + args['server_ip'] + ':8443/groups/' + args['tenant'] + '/' + args['name'] + '?api_key=' + str(apikey)
        self.logInfo(delete_url)
        headers = {'Accept':'application/json'}

        response = requests.delete(delete_url, headers=headers, verify=False, timeout=60)
        response_dict = response.json()
        return (response_dict['status'], response_dict['message'])
